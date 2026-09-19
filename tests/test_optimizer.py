import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from optimizer_core import audit, budget, context_report, route
import optimizer

CAT = {'models': [{'key': 'vendor/fast', 'available': True, 'input': 'text', 'contextWindow': 8000},
                  {'key': 'vendor/smart', 'available': True, 'input': 'text+image', 'contextWindow': 32000, 'supportsTools': True}]}
STATUS = {'allowed': ['vendor/fast', 'vendor/smart'], 'auth': {'missingProvidersInUse': []}}
POLICY = {'tiers': {'routine': ['vendor/fast', 'vendor/smart']}}

class CoreTests(unittest.TestCase):
    def test_preference_and_capability(self):
        self.assertEqual(route(CAT, STATUS, POLICY, 'routine')['candidate'], 'vendor/fast')
        self.assertEqual(route(CAT, STATUS, POLICY, 'routine', image=True)['candidate'], 'vendor/smart')
        self.assertEqual(route(CAT, STATUS, POLICY, 'routine', tools=True)['candidate'], 'vendor/smart')
        self.assertIsNone(route(CAT, STATUS, POLICY, 'routine', context=40000)['candidate'])
    def test_route_issues_block(self):
        status = dict(STATUS, auth={'modelRouteIssues':[{'model':'vendor/fast'}]})
        self.assertIsNone(route(CAT, status, POLICY, 'routine')['candidate'])
    def test_nonfinite_cost_rejected(self):
        for value in (float('nan'),float('inf'),-1,True):
            with self.assertRaises(ValueError): budget({'costUSD':value})
    def test_unknown_does_not_become_available(self):
        self.assertIsNone(route({'models':[{'key':'vendor/fast','available':None}]}, STATUS, POLICY, 'routine')['candidate'])
        self.assertIsNone(route(CAT, {}, POLICY, 'routine')['candidate'])
    def test_auth_missing(self):
        self.assertIsNone(route(CAT, {'allowed':STATUS['allowed'],'auth':{'missingProvidersInUse':['vendor']}}, POLICY, 'routine')['candidate'])
    def test_missing_usage_not_zero(self):
        self.assertIsNone(budget()['costUSD'])
        self.assertEqual(budget()['status'], 'unknown')
        self.assertEqual(budget({'costUSD':2,'complete':False})['status'], 'incomplete')
        self.assertEqual(budget({'costUSD':6,'complete':False},5)['status'], 'exceeded')
    def test_context_duplicate(self):
        result = context_report({'a':'hello','b':'hello'})
        self.assertEqual(result['files'][1]['duplicateOf'], 'a')
    def test_audit_does_not_output_private_fields(self):
        secret = 'PRIVATE_SENTINEL_NOT_FOR_REPORT'
        cfg = {'token':secret,'agents':{'defaults':{'model':'vendor/missing'},'entries':{}}}
        jobs = [{'enabled':True,'payload':{'kind':'agentTurn','message':secret},'name':secret,'schedule':{'everyMs':60000}}]
        result = audit(CAT, STATUS, cfg, jobs)
        self.assertNotIn(secret, json.dumps(result))
        codes = {x['code'] for x in result['findings']}
        self.assertTrue({'model_absent','frequent_agent_job','automation_timeout'} <= codes)
    def test_disabled_and_command_jobs_not_flagged(self):
        jobs=[{'enabled':False,'payload':{'kind':'agentTurn'}},{'payload':{'kind':'command'}}]
        self.assertFalse(any(x['code'].startswith('automation') for x in audit(CAT,STATUS,{},jobs)['findings']))
    def test_override(self):
        cfg={'agents':{'defaults':{'model':'vendor/fast'}}}
        self.assertIn('session_override',[x['code'] for x in audit(CAT,STATUS,cfg,[],[{'agentId':'a','model':'vendor/smart'}])['findings']])
    def test_native_no_shell_or_probe(self):
        with patch('optimizer.subprocess.run') as run:
            run.return_value.returncode=0
            run.return_value.stdout='{}'
            optimizer.native(['models','status','--json'])
            args, kwargs=run.call_args
            self.assertEqual(args[0],['openclaw','models','status','--json'])
            self.assertNotIn('shell',kwargs)
            self.assertEqual(kwargs['timeout'],45)
    def test_invalid_json_error_does_not_echo_input(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json';p.write_text('SECRET_SENTINEL')
            out=io.StringIO()
            with patch('sys.argv',['optimizer','audit','--config',str(p)]),contextlib.redirect_stderr(out):
                self.assertEqual(optimizer.main(),2)
            self.assertNotIn('SECRET_SENTINEL',out.getvalue())
    def test_read_only_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'config.json';p.write_text('{}')
            before=p.read_bytes()
            r=subprocess.run([sys.executable,str(Path(optimizer.__file__)),'audit','--config',str(p),'--json'],capture_output=True,text=True)
            self.assertEqual(r.returncode,0)
            self.assertEqual(p.read_bytes(),before)
            self.assertEqual(list(Path(d).iterdir()),[p])
            self.assertFalse(json.loads(r.stdout)['coverage']['catalog'])

if __name__=='__main__':unittest.main()
