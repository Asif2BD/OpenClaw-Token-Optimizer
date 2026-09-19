import hashlib
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReleaseTests(unittest.TestCase):
    def test_version_consistent(self):
        self.assertIn('version: 4.0.0',(ROOT/'SKILL.md').read_text())
        self.assertIn('version-4.0.0-',(ROOT/'README.md').read_text())
        self.assertIn('## v4.0.0',(ROOT/'CHANGELOG.md').read_text())
        self.assertIn('# Version: 4.0.0',(ROOT/'.clawhubsafe').read_text())
    def test_manifest_and_secrets(self):
        for line in (ROOT/'.clawhubsafe').read_text().splitlines():
            if line.startswith('#'):continue
            digest,name=line.split('  ',1)
            data=(ROOT/name).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),digest,name)
            text=data.decode()
            for pattern in [r'gh[pousr]_[A-Za-z0-9]{30,}',r'sk-ant-[A-Za-z0-9_-]{20,}',r'-----BEGIN .*PRIVATE KEY-----',r'/root/\.openclaw',r'46\.225\.104\.65']:
                self.assertIsNone(re.search(pattern,text),name)
    def test_license(self):
        self.assertTrue((ROOT/'LICENSE').read_text().startswith('MIT License'))
        self.assertNotIn('Apache',(ROOT/'README.md').read_text())
