import contextlib
import copy
import io
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import check_handoff as c


class CapsuleTests(unittest.TestCase):
    def setUp(self):
        self.good = json.loads((ROOT / 'examples/ready-for-review.json').read_text())

    def run_raw(self, raw):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'input.json'
            p.write_bytes(raw)
            before = set(Path(d).iterdir())
            out = io.StringIO()
            with contextlib.redirect_stdout(out), patch.object(socket, 'socket', side_effect=AssertionError('network forbidden')), patch.object(subprocess, 'Popen', side_effect=AssertionError('process forbidden')):
                result = c.main([str(p)])
            self.assertEqual(before, set(Path(d).iterdir()))
            return result, out.getvalue()

    def run_data(self, data):
        return self.run_raw(json.dumps(data).encode())

    def test_review_only(self):
        code, out = self.run_data(self.good)
        self.assertEqual(code, 0)
        self.assertIn('STRUCTURE_OK_REVIEW_REQUIRED', out)

    def test_confirmation_missing(self):
        data = json.loads((ROOT / 'examples/needs-confirmation.json').read_text())
        self.assertEqual(self.run_data(data)[0], 2)

    def test_claimed_authority_is_not_approval(self):
        self.good['authority']['status'] = 'verified_in_owner_channel'
        self.assertIn('verify evidence, recipient and authority', self.run_data(self.good)[1])

    def test_each_missing_key(self):
        for key in c.KEYS:
            with self.subTest(key=key):
                data = copy.deepcopy(self.good); del data[key]
                self.assertEqual(self.run_data(data)[0], 1)

    def test_unknown_key(self):
        self.good['execute'] = True
        self.assertEqual(self.run_data(self.good)[0], 1)

    def test_empty_values(self):
        for key in ('goal', 'current_state', 'next_step', 'recipient'):
            data = copy.deepcopy(self.good); data[key] = '   '
            self.assertEqual(self.run_data(data)[0], 1)

    def test_lists(self):
        for key in ('evidence', 'stop_if'):
            for value in ([], '', [False], ['']):
                data = copy.deepcopy(self.good); data[key] = value
                self.assertEqual(self.run_data(data)[0], 1)

    def test_bad_authority_types(self):
        for value in ([], {}, {'status': [], 'reference': 'x', 'scope': 'x'}, {'status': 'approved', 'reference': 'x', 'scope': 'x'}):
            self.good['authority'] = value
            self.assertEqual(self.run_data(self.good)[0], 1)

    def test_malformed_json_and_utf8(self):
        for value in (b'{', b'[]', b'null', b'\xff'):
            self.assertEqual(self.run_raw(value)[0], 1)

    def test_duplicate_keys(self):
        self.assertEqual(self.run_raw(b'{"goal":"x","goal":"y"}')[0], 1)

    def test_size_limit(self):
        self.assertEqual(self.run_raw(b' ' * (c.MAX_BYTES + 1))[0], 1)

    def test_no_interpretation_or_echo(self):
        # Fictional inert strings, not real credentials or attacker material.
        self.good['next_step'] = '$(touch FICTIONAL_SENTINEL); https://example.invalid/demo'
        code, out = self.run_data(self.good)
        self.assertEqual(code, 0)
        self.assertNotIn('FICTIONAL_SENTINEL', out)
        self.assertNotIn('example.invalid', out)

    def test_missing_file(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(c.main(['/fictional-missing-file.json']), 1)
        self.assertNotIn('/fictional', out.getvalue())

    def test_cli_args(self):
        for args in ([], ['a', 'b']):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(c.main(args), 1)


if __name__ == '__main__':
    unittest.main()
