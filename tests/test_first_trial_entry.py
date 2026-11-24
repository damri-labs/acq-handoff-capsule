"""Offline checks of the new direct-entry experiment, not a model-client test."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import make_trial_cards as cards


class FirstTrialEntry(unittest.TestCase):
    def test_top_fold_pair_has_gates_and_b_first(self):
        readme = (cards.ROOT / 'README.md').read_text()
        fold = readme.split('## Experiment: direct-entry prompt pair', 1)[1].split('## Experiment: two self-contained', 1)[0]
        self.assertLess(fold.index('Paste to B first'), fold.index('Paste to A only after'))
        self.assertEqual(fold.count('```text'), 2)
        for prompt in fold.split('```text\n')[1:]:
            prompt = prompt.split('\n```', 1)[0]
            for phrase in ['separate yes', 'TRIAL.md', 'Do not install', 'private', 'HTTPS']:
                self.assertIn(phrase, prompt)
        self.assertIn('READY_FOR_INVITE', fold)
        self.assertIn('not yet tested with a stranger or real model pair', fold)
        self.assertNotIn('60-second', fold)

    def test_preview_uses_actual_mocked_failure_markers(self):
        helper = types.ModuleType('preview_trial')
        exec(compile(cards.sections()[1], 'TRIAL.md/helper', 'exec'), helper.__dict__)
        def fake(method, path, body=None, token=None):
            if path == '/room':
                return {'roomId': 'ABCD-EFGH-JKMNP', 'token': 'SECRET'}
            raise TimeoutError('SECRET')
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as folder:
            private = Path(folder) / 'private'
            private.mkdir()
            with patch.object(sys, 'argv', ['trial.py', 'A']), \
                 patch.object(helper.tempfile, 'mkdtemp', return_value=str(private)), \
                 patch.object(helper, 'call', side_effect=fake), \
                 patch.object(helper, 'finish', return_value=False), \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network')), \
                 contextlib.redirect_stdout(output):
                self.assertEqual(helper.main(), 1)
        lines = [line for line in output.getvalue().splitlines() if line.startswith(('TRIAL_FAILED:', 'SEND_OUTCOME_UNVERIFIED:'))]
        preview = (cards.ROOT / 'docs/offline-first-trial-preview.txt').read_text()
        for line in lines:
            self.assertIn(line, preview)
        self.assertEqual(len(lines), 2)
        self.assertIn('OFFLINE SYNTHETIC PREVIEW', preview)
        self.assertIn('not a live run', preview)
        self.assertIn('READY_FOR_INVITE', preview)
        self.assertIn('cleanup is mocked as unverified', preview)
        self.assertNotIn('SECRET', preview)

    def test_historical_capture_not_current_revision(self):
        text = (cards.ROOT / 'docs/sample-transcript.md').read_text()
        self.assertIn('before the failure-diagnostics edit', text)
        self.assertNotIn('# Current-helper', text)
