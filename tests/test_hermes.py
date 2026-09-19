import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import optimizer
from hermes_adapter import audit_hermes, resolve_job, read_config

class HermesTests(unittest.TestCase):
    def test_job_precedence(self):
        c={'model':{'default':'global','provider':'global-provider'},'cron':{'model':'fleet','model_provider':'fleet-provider'}}
        r=resolve_job({'model':'pinned','provider':'pinned-provider','model_snapshot':'snapshot'},c,'env')
        self.assertEqual((r['model'],r['provider']),('pinned','pinned-provider'))
    def test_fleet_precedence(self):
        r=resolve_job({'model_snapshot':'snapshot'},{'cron':{'model':'fleet'}},'env')
        self.assertEqual((r['model'],r['modelSource']),('fleet','cron'))
    def test_snapshot_precedence(self):
        r=resolve_job({'model_snapshot':'snapshot'},{'model':'global'},'env')
        self.assertEqual((r['model'],r['modelSource']),('snapshot','snapshot'))
    def test_explicit_environment(self):
        self.assertEqual(resolve_job({}, {'model':'global'},'env')['model'],'env')
    def test_global_string_and_mapping(self):
        for model in ('global',{'default':'global'}):self.assertEqual(resolve_job({}, {'model':model})['model'],'global')
    def test_no_agent_not_charged_as_agent(self):
        r=audit_hermes({},[{'no_agent':True,'script':'SECRET SCRIPT','schedule':{'kind':'interval','minutes':1}}])
        self.assertEqual(r['counts']['noAgent'],1)
        self.assertFalse(r['findings'])
        self.assertNotIn('SECRET SCRIPT',json.dumps(r))
    def test_missing_script_flagged(self):
        self.assertEqual(audit_hermes({},[{'no_agent':True}])['findings'][0]['code'],'hermes_script_missing')
    def test_paused_skipped(self):
        r=audit_hermes({},[{'state':'paused'},{'enabled':False}])
        self.assertEqual(r['counts']['enabled'],0)
    def test_frequent_agent(self):
        r=audit_hermes({'model':'m'},[{'schedule':{'kind':'interval','minutes':10}}])
        self.assertIn('hermes_frequent_agent_job',[f['code'] for f in r['findings']])
    def test_no_secret_content_output(self):
        sentinel='DO_NOT_EMIT_SECRET'
        r=audit_hermes({'api_key':sentinel,'model':'m'},[{'prompt':sentinel,'script':sentinel,'base_url':sentinel}])
        self.assertNotIn(sentinel,json.dumps(r))
    def test_invalid_boolean(self):
        with self.assertRaises(ValueError):audit_hermes({},[{'no_agent':'false'}])
    def test_cli_hermes_never_invokes_openclaw(self):
        with tempfile.TemporaryDirectory() as d:
            c=Path(d)/'c.json';j=Path(d)/'j.json';c.write_text('{"model":"m"}');j.write_text('{"jobs":[]}')
            with patch('sys.argv',['optimizer','audit','--runtime','hermes','--config',str(c),'--jobs',str(j),'--json']),patch('optimizer.native') as native,contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(optimizer.main(),0);native.assert_not_called()
    def test_yaml_object_constructor_rejected(self):
        try:import yaml
        except ImportError:self.skipTest('Optional PyYAML unavailable')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'c.yaml';p.write_text('!!python/object/apply:os.system ["false"]')
            with self.assertRaises(ValueError):read_config(p)
    def test_hermes_live_requires_profile(self):
        with patch('sys.argv',['optimizer','audit','--runtime','hermes','--live']),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(optimizer.main(),2)
    def test_hermes_live_route_not_fabricated(self):
        with patch('sys.argv',['optimizer','route','--runtime','hermes','--live','--hermes-home','/unused','--tier','routine','--policy','/unused']),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(optimizer.main(),2)
