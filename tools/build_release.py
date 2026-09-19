#!/usr/bin/env python3
"""Maintainer-only clean bundle builder; never shipped in the skill package."""
import hashlib
import shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
VERSION = '4.0.1'
FILES = ['SKILL.md','README.md','CHANGELOG.md','LICENSE.txt','SECURITY.md']
for folder in ('scripts','assets','references'):
    FILES.extend(str(p.relative_to(ROOT)) for p in (ROOT/folder).iterdir() if p.is_file() and p.suffix in ('.py','.sh','.md','.json'))
FILES = sorted(FILES)
manifest = '# ClawHub integrity manifest\n# Version: '+VERSION+'\n# Integrity is not an independent security approval.\n'
manifest += ''.join(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in FILES)
(ROOT/'.clawhubsafe').write_text(manifest)
(ROOT/'SHA256SUMS.txt').write_text(manifest)
target = ROOT/'dist'/('openclaw-token-optimizer-'+VERSION)
if target.exists(): shutil.rmtree(target)
target.mkdir(parents=True)
for name in FILES+['SHA256SUMS.txt','.clawhubsafe','.clawhubignore']:
    dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,dest)
print(str(target))
