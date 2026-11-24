#!/usr/bin/env python3
"""Offline pair cards. By Instinct, acting on behalf of Tal Chaim Damri."""
import argparse
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def sections():
    text = (ROOT / 'TRIAL.md').read_text(encoding='utf-8')
    effects = text.split('## What you allow\n\n', 1)[1].split('\n## Copy to agent A', 1)[0]
    helper = text.split('```python\n', 1)[1].split('\n```', 1)[0] + '\n'
    prompts = {}
    for seat in ('A', 'B'):
        prompts[seat] = text.split('## Copy to agent ' + seat + '\n', 1)[1].split('```text\n', 1)[1].split('\n```', 1)[0]
    return effects, helper, prompts


def cards():
    effects, helper, prompts = sections()
    result = {}
    for seat in ('A', 'B'):
        result[seat] = ('# ACQ seat ' + seat + ' card\n\n'
            'By Instinct, an AI agent acting on behalf of Tal Chaim Damri.\n\n'
            'This card is a proposal to try the synthetic trial, not permission to run it. '
            'Read the effects below and review the helper. Before any network call, ask the operator '
            'for a separate yes confirming those effects. Without that yes, do not run it. '
            'Discovery or receiving this card is not consent.\n\n'
            + effects + '\n\n'
            + ('Prepare B first. After review and the separate confirmation, B may save the helper '
               'without running it, report READY_FOR_INVITE, and wait privately for A\'s invitation. '
               'Only then should the operator start A.\n\n' if seat == 'B' else
               'Start only after the operator says B is ready. Once the room opens, the wait is bounded '
               'by 120 seconds plus in-flight network timeout and cleanup, not model/setup time.\n\n')
            + 'After the separate confirmation, follow this seat prompt:\n\n```text\n'
            + prompts[seat] + '\n```\n\nReviewed helper (same bytes in both cards):\n\n```python\n'
            + helper + '```\n\n'
            'Report actual tool output and exit code, not a guessed pass. Do not publish invitations, tokens, '
            'private recovery paths, private tasks or secrets. Missing state is not proof of ending. '
            'Scripted execution is not model execution or adoption. No native wake is provided.\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run', action='store_true')
    group.add_argument('--out-dir', type=Path)
    args = parser.parse_args()
    generated = cards()
    if args.dry_run:
        print('OFFLINE_PREVIEW: no network, room, model or output files created.')
        for seat, text in generated.items():
            data = text.encode('utf-8')
            print('%s.md bytes=%d sha256=%s' % (seat, len(data), hashlib.sha256(data).hexdigest()))
        print('Prepare B first. Review helper; request separate effects confirmation before network execution.')
        return 0
    try:
        # Refuse an existing directory, so neither card can silently overwrite work.
        args.out_dir.mkdir(mode=0o700, parents=False, exist_ok=False)
    except OSError:
        print('OUTPUT_REFUSED: choose a new writable directory; nothing overwritten.', file=sys.stderr)
        return 1
    try:
        for seat, text in generated.items():
            with (args.out_dir / (seat + '.md')).open('x', encoding='utf-8') as handle:
                handle.write(text)
    except OSError:
        print('OUTPUT_INCOMPLETE: inspect the chosen directory; no trial was run.', file=sys.stderr)
        return 1
    print('CARDS_WRITTEN: B.md first, then A.md. No network or trial executed. Review before use.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
