import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import try_acq


class DryRunTests(unittest.TestCase):
    def test_dry_run_has_no_socket_http_or_private_state(self):
        out = io.StringIO()
        with patch.object(sys, 'argv', ['try_acq.py', '--dry-run']), \
             patch('socket.socket', side_effect=AssertionError('socket opened')) as sock, \
             patch('socket.create_connection', side_effect=AssertionError('connection opened')) as conn, \
             patch('urllib.request.urlopen', side_effect=AssertionError('HTTP attempted')) as http, \
             patch('tempfile.mkdtemp', side_effect=AssertionError('private state created')) as temp, \
             contextlib.redirect_stdout(out):
            self.assertEqual(try_acq.main(), 0)
        for mocked in (sock, conn, http, temp):
            mocked.assert_not_called()
        text = out.getvalue()
        for expected in ('https://acq.damri.org', 'POST /room', 'GET /room/',
                         '2 hours', '24 hours', 'cleanup', 'not model agents',
                         'zero network calls', 'history reads'):
            self.assertIn(expected.lower(), text.lower())

    def test_dry_run_cleanup_combination_rejected_without_network(self):
        with patch.object(sys, 'argv', ['try_acq.py', '--dry-run', '--cleanup', '/unused']), \
             patch('socket.socket', side_effect=AssertionError('socket opened')) as sock, \
             patch('urllib.request.urlopen', side_effect=AssertionError('HTTP attempted')) as http, \
             contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            try_acq.main()
        self.assertEqual(raised.exception.code, 2)
        sock.assert_not_called()
        http.assert_not_called()

    def test_cleanup_missing_state_is_clear_without_network_or_traceback(self):
        err = io.StringIO()
        with patch.object(sys, 'argv', ['try_acq.py', '--cleanup', '/unused']), \
             patch('pathlib.Path.read_text', side_effect=FileNotFoundError), \
             patch('urllib.request.urlopen', side_effect=AssertionError('HTTP attempted')) as http, \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
            self.assertEqual(try_acq.main(), 1)
        http.assert_not_called()
        self.assertIn('CLEANUP_STATE_UNAVAILABLE', err.getvalue())
        self.assertNotIn('Traceback', err.getvalue())
        self.assertNotIn('ENDED_VERIFIED', err.getvalue())
