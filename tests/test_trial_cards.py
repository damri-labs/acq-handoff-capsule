import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import make_trial_cards as cards


class CardTests(unittest.TestCase):
    def test_embedded_helper_identical_and_gate_present(self):
        expected = cards.sections()[1]
        for card in cards.cards().values():
            actual = card.split('```python\n', 1)[1].split('\n```', 1)[0] + '\n'
            self.assertEqual(actual, expected)
            self.assertIn('separate yes', card)
            self.assertIn('not consent', card)
            self.assertIn('The relay can read text', card)
        self.assertIn('Only after B reports READY_FOR_INVITE should the operator start A', cards.cards()['B'])
        self.assertIn('operator passes privately to B', cards.cards()['B'])
        self.assertIn('120-second wait starts when A opens its room', cards.cards()['A'])
        self.assertIn('pass the invitation promptly', cards.cards()['A'])

    def test_dry_run_no_network_or_writes(self):
        source = (cards.ROOT / 'TRIAL.md').read_text()
        with patch('pathlib.Path.read_text', return_value=source), \
             patch.object(sys, 'argv', ['make_trial_cards.py', '--dry-run']), \
             patch('socket.socket', side_effect=AssertionError('socket')) as sock, \
             patch('pathlib.Path.mkdir', side_effect=AssertionError('mkdir')) as mkdir, \
             patch('pathlib.Path.open', side_effect=AssertionError('write')) as opened, \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cards.main(), 0)
        sock.assert_not_called()
        mkdir.assert_not_called()
        opened.assert_not_called()

    def test_generation_and_existing_directory_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'cards'
            with patch.object(sys, 'argv', ['make_trial_cards.py', '--out-dir', str(target)]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cards.main(), 0)
            for seat, text in cards.cards().items():
                self.assertEqual((target / (seat + '.md')).read_text(), text)
            before = (target / 'A.md').read_bytes()
            with patch.object(sys, 'argv', ['make_trial_cards.py', '--out-dir', str(target)]), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(cards.main(), 1)
            self.assertEqual((target / 'A.md').read_bytes(), before)

    def test_runbook_matches_separate_confirmation_and_readiness_order(self):
        text = (cards.ROOT / 'RUNBOOK.md').read_text(encoding='utf-8')
        self.assertLess(text.index('Give B `trial-cards/B.md`'), text.index('give A `trial-cards/A.md`'))
        self.assertLess(text.index('READY_FOR_INVITE'), text.index('give A `trial-cards/A.md`'))
        self.assertIn('own separate effects confirmation', text)
        self.assertIn('same separate effects confirmations', text)
        self.assertIn("starts when its room opens", text)
        self.assertIn('offline preparation only, not permission', text)

    def test_readme_flow_and_png_present(self):
        text = (cards.ROOT / 'README.md').read_text(encoding='utf-8')
        flow = text.split('## B-first sequence', 1)[1].split('## No-install', 1)[0]
        self.assertIn('Text equivalent:', flow)
        self.assertLess(flow.index('READY_FOR_INVITE'), flow.index('INVITE_UIN'))
        for word in ['separate yes', '120-second wait starts at room opening', 'No native wake', 'relay can read text', 'Missing state is not proof']:
            self.assertIn(word, flow)
        self.assertTrue((cards.ROOT / 'docs/1-two-seat-flow.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
