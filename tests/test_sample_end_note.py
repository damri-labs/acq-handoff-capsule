"""Sample-note and runbook-marker checks. By Instinct for Tal Chaim Damri."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MARKER = 'ENDED_VERIFIED; local private state removed.'
NOTE = '[Editorial note, not captured output: New sends are closed and local recovery state was removed. Relay history deletion was NOT checked.]'


class SampleEndNoteTests(unittest.TestCase):
    def test_note_follows_each_unchanged_marker(self):
        sample = (ROOT / 'docs/sample-transcript.md').read_text()
        self.assertEqual(sample.count(MARKER), 2)
        self.assertEqual(sample.count(MARKER + '\n' + NOTE), 2)
        self.assertIn('historical output lines below are unchanged', sample)

    def test_runbook_parser_accepts_annotated_sample(self):
        sample = (ROOT / 'docs/sample-transcript.md').read_text()
        outputs = re.findall(r'```text\n(.*?)\n```', sample, re.S)[:2]
        checker = (ROOT / 'RUNBOOK.md').read_text().split("python3 - <<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
        with tempfile.TemporaryDirectory() as temp:
            for seat, output in zip('AB', outputs):
                Path(temp, seat + '.output.txt').write_text(output)
            result = subprocess.run([sys.executable, '-c', checker], cwd=temp,
                                    text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('OUTPUT_MARKERS_PASS_REVIEW_REQUIRED', result.stdout)
        self.assertIn('Markers do not prove model identity', result.stdout)
