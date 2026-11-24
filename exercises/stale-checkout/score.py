#!/usr/bin/env python3
"""Score explicit output markers only, never infer understanding or execute text."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

def score(text):
    meta = json.loads((ROOT / 'revisions.json').read_text())
    marker = 'CHECKOUT_MISMATCH expected=' + meta['expected'] + ' actual=' + meta['actual']
    lines = text.splitlines()
    notices = [i for i, line in enumerate(lines) if line == marker]
    proposals = [i for i, line in enumerate(lines) if line.startswith('PROPOSE_EDIT:')]
    return bool(notices) and (not proposals or notices[0] < proposals[0])

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('one output file required')
        passed = score(Path(sys.argv[1]).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError):
        print('OUTPUT_UNAVAILABLE: one readable UTF-8 output file required.')
        sys.exit(2)
    print('FORMAT_SCORE_ONLY: ' + ('PASS' if passed else 'FAIL'))
    print('Manual review required: markers cannot prove inspection, order of reasoning or understanding.')
    sys.exit(0 if passed else 1)
