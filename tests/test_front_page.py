"""Offline prose checks, no usability or model-performance claim."""
import ast
import re
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class FrontPage(unittest.TestCase):
    def test_headings_and_no_time_promise(self):
        text = (ROOT / 'README.md').read_text()
        self.assertIn('## Run the local checker (no network)', text)
        self.assertIn('## Run the scripted ACQ recovery example (real HTTPS, optional)', text)
        self.assertNotRegex(text.lower(), r'about\s+60\s+seconds|60-second')
        self.assertLess(text.index('## Run the local checker'), text.index('## Experiment:'))
        opening = text.split('## Run the local checker', 1)[0]
        for phrase in ['ACQ relay', 'not tested with real users or a real model pair', 'No wake or orchestration', 'No adoption claimed', 'If both sessions are Claude Code, built-in session messaging may fit better', 'Start here', 'TRIAL.md']:
            self.assertIn(phrase, opening)

    def test_security_guidance(self):
        text = (ROOT / 'SECURITY.md').read_text()
        for phrase in ['invitations', 'tokens', 'private tasks', 'secrets', 'issues', 'end the room', 'delete the comment']:
            self.assertIn(phrase, text)
        self.assertNotRegex(text.lower(), r'within\s+\d+\s+(hours|days)|guaranteed response')

    def test_pair_prompt_spacing(self):
        text = ast.get_docstring(ast.parse((ROOT / 'examples/pair_review.py').read_text()))
        for phrase in ['most 90 seconds', 'to 5 minutes', 'only 13 uppercase', 'grouped 4-4-5', 'total 5 minutes', 'paper 375, clips 500, corrected total 875']:
            self.assertIn(phrase, text)

    def test_changed_prose_has_no_glued_digit_words(self):
        texts = [(ROOT / n).read_text() for n in ['README.md', 'SECURITY.md']]
        texts.append(ast.get_docstring(ast.parse((ROOT / 'examples/pair_review.py').read_text())))
        for text in texts:
            text = re.sub(r'```.*?```|`[^`]*`|https?://\S+', '', text, flags=re.S)
            text = re.sub(r'\b[0-9a-f]{40}\b', '', text)
            # Existing command names and illustrative invitation are identifiers.
            text = re.sub(r'\bpython3\b|\bK4TZ-9M0X-3PW7Q\b', '', text)
            self.assertIsNone(re.search(r'[A-Za-z]\d|\d[A-Za-z]', text))
