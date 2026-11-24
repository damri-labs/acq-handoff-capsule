"""Offline tests of the exact helper copied into documents and cards."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import urllib.error
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import make_trial_cards as cards


class EmbeddedFailures(unittest.TestCase):
    def helper(self):
        module = types.ModuleType('embedded_trial')
        exec(compile(cards.sections()[1], 'TRIAL.md/helper', 'exec'), module.__dict__)
        return module

    def run_failure(self, role, failure, error):
        helper = self.helper()
        sends = []
        def fake(method, path, body=None, token=None):
            if path == '/room' or path.endswith('/join'):
                if failure == 'open':
                    raise error
                if failure == 'response':
                    return {}
                return {'roomId': 'ABCD-EFGH-JKMNP', 'token': 'SENTINEL'}
            if method == 'POST':
                sends.append(body)
                if failure == 'send':
                    raise error
                return {}
            if failure == 'receive':
                raise error
            return {'messages': [{'text': 'ACQ_PING:' + 'a' * 32}], 'cursor': 1}
        output = io.StringIO()
        args = ['trial.py', role] + (['ABCD-EFGH-JKMNP'] if role == 'B' else [])
        with tempfile.TemporaryDirectory() as folder:
            private = Path(folder) / 'private'
            private.mkdir()
            with patch.object(sys, 'argv', args), \
                 patch.object(helper.tempfile, 'mkdtemp', return_value=str(private)), \
                 patch.object(helper, 'call', side_effect=fake), \
                 patch.object(helper, 'finish', return_value=False) as finish, \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network')), \
                 contextlib.redirect_stdout(output):
                self.assertEqual(helper.main(), 1)
            finish.assert_called_once()
            self.assertTrue((private / 'state.json').exists())
        visible = output.getvalue()
        self.assertNotIn('SENTINEL', visible)
        self.assertNotIn('SECRET_URL', visible)
        self.assertNotIn('Traceback', visible)
        self.assertLessEqual(len(sends), 1)
        return visible

    def test_failure_stages_and_redaction(self):
        for role in ('A', 'B'):
            for failure, stage in [('open', 'create' if role == 'A' else 'join'),
                                   ('response', 'create-response' if role == 'A' else 'join-response'),
                                   ('send', 'send'), ('receive', 'receive')]:
                with self.subTest(role=role, stage=stage):
                    output = self.run_failure(role, failure, TimeoutError('SENTINEL SECRET_URL'))
                    self.assertIn('TRIAL_FAILED: stage=' + stage, output)
                    if failure != 'response':
                        self.assertIn('TimeoutError', output)
                    if failure == 'send':
                        self.assertIn('SEND_OUTCOME_UNVERIFIED', output)
                    else:
                        self.assertNotIn('SEND_OUTCOME_UNVERIFIED', output)

    def test_http_status_class_and_no_retry(self):
        for role, failure, code in [('B', 'open', 410), ('B', 'open', 409),
                                    ('A', 'send', 500), ('B', 'send', 500)]:
            with self.subTest(role=role, code=code):
                error = urllib.error.HTTPError('SECRET_URL', code, 'SENTINEL', {}, None)
                output = self.run_failure(role, failure, error)
                self.assertIn('HTTP=' + str(code), output)
                self.assertIn('HTTPError', output)

    def test_hebrew_and_cards_same_helper(self):
        expected = cards.sections()[1]
        hebrew = (cards.ROOT / 'TRIAL.he.md').read_text()
        self.assertEqual(hebrew.split('```python\n', 1)[1].split('\n```', 1)[0] + '\n', expected)
        reference = (cards.ROOT / '.agents/skills/acq-two-seat-trial/references/TRIAL.md').read_text()
        self.assertEqual(reference.split('```python\n', 1)[1].split('\n```', 1)[0] + '\n', expected)
        for text in cards.cards().values():
            self.assertEqual(text.split('```python\n', 1)[1].split('\n```', 1)[0] + '\n', expected)
        self.assertNotIn('str(error)', expected)

    def test_successful_seats_still_pass(self):
        for role in ('A', 'B'):
            with self.subTest(role=role), tempfile.TemporaryDirectory() as folder:
                helper = self.helper()
                private = Path(folder) / 'private'
                private.mkdir()
                nonce = ['a' * 32]
                def fake(method, path, body=None, token=None):
                    if path == '/room' or path.endswith('/join'):
                        return {'roomId': 'ABCD-EFGH-JKMNP', 'token': 'SENTINEL'}
                    if method == 'POST':
                        nonce[0] = body['cid']
                        return {}
                    prefix = 'ACQ_PONG:' if role == 'A' else 'ACQ_PING:'
                    return {'messages': [{'text': prefix + nonce[0]}], 'cursor': 1, 'ended': True}
                args = ['trial.py', role] + (['ABCD-EFGH-JKMNP'] if role == 'B' else [])
                with patch.object(sys, 'argv', args), \
                     patch.object(helper.tempfile, 'mkdtemp', return_value=str(private)), \
                     patch.object(helper, 'call', side_effect=fake), \
                     patch.object(helper, 'finish', return_value=True), \
                     patch('urllib.request.urlopen', side_effect=AssertionError('network')), \
                     contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(helper.main(), 0)
