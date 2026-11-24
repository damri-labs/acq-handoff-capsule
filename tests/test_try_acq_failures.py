import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import try_acq


class FailureTests(unittest.TestCase):
    def run_failure(self, stage, error):
        calls = []
        def fake(method, path, body=None, token=None, discard=False):
            calls.append((method, path))
            if method == 'POST' and path == '/room':
                if stage == 'create':
                    return {'token': 'SENTINEL_SECRET'}
                return {'roomId': 'room', 'token': 'SENTINEL_SECRET'}
            if path.endswith('/join'):
                if stage == 'join':
                    raise error
                return {'token': 'SENTINEL_PEER'}
            if method == 'POST' and body and body.get('end') is False:
                raise error
            if method == 'GET':
                return {'ended': True}
            raise AssertionError('unexpected call')
        out, err = io.StringIO(), io.StringIO()
        with tempfile.TemporaryDirectory() as parent:
            private = Path(parent) / 'private'
            private.mkdir()
            with patch.object(sys, 'argv', ['try_acq.py']), \
                 patch('tempfile.mkdtemp', return_value=str(private)), \
                 patch.object(try_acq, 'request', side_effect=fake), \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network')), \
                 contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = try_acq.main()
            self.assertEqual(code, 1)
            visible = out.getvalue() + err.getvalue()
            self.assertNotIn('SENTINEL', visible)
            self.assertNotIn('Traceback', visible)
            return visible, calls

    def test_failure_stage_and_safe_http_status(self):
        for stage, error, expected in [
            ('create', None, 'stage=create-response'),
            ('join', urllib.error.HTTPError('SECRET_URL', 410, 'SENTINEL', {}, None), 'stage=join HTTP=410'),
            ('join', urllib.error.HTTPError('SECRET_URL', 409, 'SENTINEL', {}, None), 'stage=join HTTP=409'),
            ('send', urllib.error.HTTPError('SECRET_URL', 500, 'SENTINEL', {}, None), 'stage=send HTTP=500'),
            ('send', TimeoutError('SENTINEL'), 'stage=send TimeoutError'),
        ]:
            with self.subTest(stage=stage, expected=expected):
                visible, calls = self.run_failure(stage, error)
                self.assertIn(expected, visible)
                if stage == 'send':
                    self.assertIn('SEND_OUTCOME_UNVERIFIED', visible)
                sends = [x for x in calls if x == ('POST', '/room/room/msg')]
                self.assertLessEqual(len(sends), 1)

    def test_corrupt_state_no_network(self):
        for raw in ('{broken', '[]', 'null'):
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as folder:
                Path(folder, 'state.json').write_text(raw)
                err = io.StringIO()
                with patch.object(sys, 'argv', ['try_acq.py', '--cleanup', folder]), \
                     patch('urllib.request.urlopen', side_effect=AssertionError('network')) as http, \
                     contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                    self.assertEqual(try_acq.main(), 1)
                http.assert_not_called()
                self.assertIn('CLEANUP_STATE_UNAVAILABLE', err.getvalue())
                self.assertTrue(Path(folder, 'state.json').exists())

    def test_cleanup_timeout_retains_state(self):
        with tempfile.TemporaryDirectory() as folder:
            state = Path(folder, 'state.json')
            state.write_text(json.dumps(dict(room='room', token='SENTINEL', cid='cid')))
            out, err = io.StringIO(), io.StringIO()
            with patch.object(sys, 'argv', ['try_acq.py', '--cleanup', folder]), \
                 patch.object(try_acq, 'request', side_effect=TimeoutError('SENTINEL')) as req, \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network')), \
                 contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                self.assertEqual(try_acq.main(), 1)
            self.assertEqual(req.call_count, 2)
            self.assertTrue(state.exists())
            self.assertIn('Cleanup unverified', err.getvalue())
            self.assertNotIn('SENTINEL', out.getvalue() + err.getvalue())
