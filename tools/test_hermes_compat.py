#!/usr/bin/env python3
"""Maintainer integration test. Executes pinned Hermes storage code in a temp profile.
Never shipped. Never launches the scheduler, a script or an inference request.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from hermes_adapter import HERMES_SOURCE
p=argparse.ArgumentParser();p.add_argument('--source',required=True);a=p.parse_args()
source=Path(a.source).resolve()
sha=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
if sha!=HERMES_SOURCE:raise SystemExit('Hermes checkout differs from tested pin')
with tempfile.TemporaryDirectory(prefix='optimizer-hermes-') as directory:
    home=Path(directory)
    (home/'config.yaml').write_text('model:\n  default: global-model\n  provider: global-provider\n')
    (home/'.env').write_text('SECRET_SENTINEL=NEVER_READ_OR_OUTPUT\n')
    env={'PATH':os.environ['PATH'],'HERMES_HOME':directory,'PYTHONPATH':str(source),'PYTHONDONTWRITEBYTECODE':'1'}
    code='''from cron.jobs import parse_schedule, save_jobs
save_jobs([
 {'enabled':True,'no_agent':True,'script':'never-executed.py','schedule':parse_schedule('every 5m')},
 {'enabled':True,'model':'pinned','schedule':parse_schedule('every 15m')},
 {'enabled':True,'model_snapshot':'snapshot','schedule':parse_schedule('every 2h')},
 {'enabled':False,'schedule':parse_schedule('every 5m')}
])'''
    subprocess.run([sys.executable,'-c',code],env=env,cwd=source,check=True,capture_output=True)
    def digest():return {str(f.relative_to(home)):hashlib.sha256(f.read_bytes()).hexdigest() for f in home.rglob('*') if f.is_file()}
    before=digest()
    r=subprocess.run([sys.executable,str(ROOT/'scripts/optimizer.py'),'audit','--runtime','hermes','--live','--hermes-home',directory,'--json'],env=env,capture_output=True,text=True,check=True)
    result=json.loads(r.stdout)
    assert before==digest(), 'Profile modified'
    assert result['counts']=={'total':4,'enabled':3,'noAgent':1}
    assert result['automations'][1]['resolution']['model']=='pinned'
    assert result['automations'][2]['resolution']['model']=='snapshot'
    assert 'NEVER_READ_OR_OUTPUT' not in r.stdout
    print(json.dumps({'sourceCommit':sha,'nativeStoreRoundtrip':True,'profileUnchanged':True,'counts':result['counts'],'schedulerStarted':False,'inferencePerformed':False}))
