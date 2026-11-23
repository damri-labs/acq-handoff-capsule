#!/usr/bin/env python3
"""ACQ capsule shape checker. Instinct on behalf of Tal Chaim Damri.
No networking, execution, writes, identity verification or permission decision.
"""
import json
from pathlib import Path
import sys

MAX_BYTES = 65536
KEYS = {'goal', 'current_state', 'evidence', 'next_step', 'recipient', 'authority', 'stop_if'}
AUTH_KEYS = {'status', 'reference', 'scope'}
AUTH_STATES = {'not_needed', 'needs_confirmation', 'verified_in_owner_channel'}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate_key')
        result[key] = value
    return result


def validate(data):
    if not isinstance(data, dict) or set(data) != KEYS:
        raise ValueError('wrong_top_level_keys')
    for key in ('goal', 'current_state', 'next_step', 'recipient'):
        if not nonempty(data[key]):
            raise ValueError('missing_text_' + key)
    for key in ('evidence', 'stop_if'):
        if not isinstance(data[key], list) or not data[key] or not all(nonempty(x) for x in data[key]):
            raise ValueError('invalid_list_' + key)
    authority = data['authority']
    if not isinstance(authority, dict) or set(authority) != AUTH_KEYS:
        raise ValueError('wrong_authority_keys')
    if not isinstance(authority['status'], str) or authority['status'] not in AUTH_STATES:
        raise ValueError('invalid_authority_status')
    if not all(nonempty(authority[x]) for x in ('reference', 'scope')):
        raise ValueError('missing_authority_reference_or_scope')
    return authority['status']


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print('INVALID: expected one explicit JSON file path')
        return 1
    try:
        with Path(args[0]).open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('file_too_large')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=reject_duplicate_keys)
        status = validate(data)
    except (OSError, ValueError, RecursionError):
        # Never echo file contents, paths, exception payloads or attacker-controlled text.
        print('INVALID: shape, encoding, size or file read error')
        return 1
    if status == 'needs_confirmation':
        print('STRUCTURE_OK_CONFIRMATION_MISSING: do not execute the proposed next step')
        return 2
    print('STRUCTURE_OK_REVIEW_REQUIRED: verify evidence, recipient and authority before any action')
    return 0


if __name__ == '__main__':
    sys.exit(main())
