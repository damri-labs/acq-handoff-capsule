"""Deterministic exercise checks, not evidence of model performance."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'exercises/stale-checkout'

class StaleCheckout(unittest.TestCase):
    def test_sample_scores(self):
        script = ROOT / 'score.py'
        for name, code in [('known-pass.txt', 0), ('known-fail.txt', 1), ('wrong-id.txt', 1), ('marker-in-proposal.txt', 1)]:
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(script), str(ROOT / 'samples' / name)], capture_output=True, text=True)
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertIn('FORMAT_SCORE_ONLY', result.stdout)

    def test_setup_stale_commit_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'fixture'
            result = subprocess.run([sys.executable, str(ROOT / 'prepare.py'), str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            meta = json.loads((ROOT / 'revisions.json').read_text())
            git = lambda *args: subprocess.check_output(['git', '-C', str(target), *args], text=True).strip()
            self.assertEqual(git('rev-parse', 'HEAD'), meta['actual'])
            self.assertEqual(git('rev-parse', 'HEAD^'), meta['expected'])
            self.assertNotEqual(meta['actual'], meta['expected'])
            self.assertIn('125', (target / 'estimate.py').read_text())
            again = subprocess.run([sys.executable, str(ROOT / 'prepare.py'), str(target)], capture_output=True, text=True)
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual(git('rev-parse', 'HEAD'), meta['actual'])

    def test_variants_share_same_task_and_stale_reference(self):
        meta = json.loads((ROOT / 'revisions.json').read_text())
        for name in ['template-handoff.md', 'free-text-handoff.md']:
            text = (ROOT / name).read_text()
            self.assertIn(meta['expected'], text)
            self.assertNotIn(meta['actual'], text)
            self.assertIn('Add a quantity limit of 20', text)
            self.assertIn('No edits before checking the checkout', text)
