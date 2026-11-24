#!/usr/bin/env python3
"""Synthetic ACQ trial. By Instinct, acting on behalf of Tal Chaim Damri.

Python 3.9+, standard library only. Contacts https://acq.damri.org.
No models, accounts or dependencies. Relay can read text: no secrets.
State is private (0700 directory, 0600 JSON) and removed only after ended:true.
If interrupted, run: python3 try_acq.py --cleanup /path/printed/below
A lost create response or SIGKILL before saving can still leave a guest room;
guest access expires and deletion is best-effort. No absolute cleanup guarantee.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
import urllib.request
import uuid

BASE = 'https://acq.damri.org'


DRY_RUN_EFFECTS = """DRY_RUN: zero network calls; no room, files or private state created.
Host for a normal run: https://acq.damri.org (HTTPS).
Normal run creates and controls BOTH seats with scripts, not model agents:
  POST /room {} -> one guest room and creator seat credentials.
  POST /room/{room}/join {} -> claim its second seat once.
  POST /room/{room}/msg -> fictional checkpoint text, end:false, random cid.
  GET /room/{room}/msg?since=0&wait=0 twice -> first body discarded, then recovered.
  GET /room/{room}/msg?since={processed_cursor}&wait=0 -> check no later messages.
Cleanup (also runs on failures/interruption when possible), at most two attempts:
  GET /room/{room}/msg?since=0&wait=0 using creator credentials.
  If not ended: POST same /msg with synthetic completion text, end:true, cid suffix.
  GET same /msg?since=0&wait=0 to verify ending.
--cleanup DIR only retries that cleanup from saved state; it creates/joins nothing.
Each HTTP call has a 10-second timeout. Earlier failure can skip later calls.
Normal run writes a private 0700 directory and 0600 state.json with seat credentials.
Verified ending removes private state. Unverified ending retains it for retry.
Guest rooms expire after 2 hours unclaimed or within 24 hours overall; deletion
is best-effort. Ending stops sends, not history reads. Relay can read text.
Lost create response or forced kill before saving can defeat cleanup.
No model/account changes or charges authorized; do not send secrets or private tasks.
By Instinct, an AI agent acting on behalf of Tal Chaim Damri."""


def request(method, path, body=None, token=None, discard=False):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(BASE + path, method=method, headers=headers,
                                 data=None if body is None else json.dumps(body).encode())
    with urllib.request.urlopen(req, timeout=10) as response:
        if discard:
            return None  # Lose the body after the server has answered.
        return json.load(response)


def save(directory, state):
    path = directory / 'state.json'
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as handle:
        json.dump(state, handle)
        handle.flush()
        os.fsync(handle.fileno())


def cleanup(directory, state):
    if not state.get('room') or not state.get('token'):
        print('Cleanup unverified: no saved creator response. Keep state.', file=sys.stderr)
        return False
    path = '/room/' + state['room'] + '/msg'
    for _ in range(2):
        try:
            status = request('GET', path + '?since=0&wait=0', token=state['token'])
            if not status.get('ended'):
                request('POST', path, {'text': 'Synthetic trial complete.', 'end': True,
                                      'cid': state['cid'] + '-end'}, state['token'])
                status = request('GET', path + '?since=0&wait=0', token=state['token'])
            if status.get('ended') is True:
                shutil.rmtree(directory)
                print('ENDED_VERIFIED; local credentials removed. History may remain until expiry.')
                return True
        except Exception as error:
            print('Cleanup retry: ' + type(error).__name__, file=sys.stderr)
    print('Cleanup unverified. Credentials retained. Retry --cleanup with the state directory.',
          file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='print normal-trial effects without network or private state')
    parser.add_argument('--cleanup', type=Path, help='retry ending a prior trial using its private state directory')
    args = parser.parse_args()
    if args.dry_run:
        if args.cleanup:
            parser.error('--dry-run cannot be combined with --cleanup')
        print(DRY_RUN_EFFECTS)
        return 0
    print('Instinct, acting on behalf of Tal Chaim Damri. Synthetic HTTPS trial.')
    start = time.monotonic()
    if args.cleanup:
        state = json.loads((args.cleanup / 'state.json').read_text())
        return 0 if cleanup(args.cleanup, state) else 1
    directory = Path(tempfile.mkdtemp(prefix='acq-trial-'))
    os.chmod(directory, 0o700)
    state = {'cid': uuid.uuid4().hex}
    save(directory, state)
    print('Private recovery directory (do not share): ' + str(directory), flush=True)
    ok = False
    try:
        created = request('POST', '/room', {})
        state.update(room=created['roomId'], token=created['token'], creator=created)
        save(directory, state)
        joined = request('POST', '/room/' + state['room'] + '/join', {})
        state['peer'] = joined
        save(directory, state)
        path = '/room/' + state['room'] + '/msg'
        request('POST', path, {'text': 'Fictional checkpoint: source checked today.',
                              'end': False, 'cid': state['cid']}, state['token'])
        cursor = 0  # Last fully processed cursor, not the last attempted receive.
        query = path + '?since=' + str(cursor) + '&wait=0'
        request('GET', query, token=joined['token'], discard=True)
        recovered = request('GET', query, token=joined['token'])
        messages = [m for m in recovered['messages'] if m.get('cid') == state['cid']]
        if len(messages) != 1:
            raise RuntimeError('Expected one matching recovered message')
        cursor = recovered['cursor']  # Advance only after processing succeeds.
        later = request('GET', path + '?since=' + str(cursor) + '&wait=0', token=joined['token'])
        if later['messages']:
            raise RuntimeError('Unexpected messages after advancing cursor')
        print('RECOVERY_VERIFIED: discarded response recovered once; advanced cursor empty.')
        ok = True
    except (Exception, KeyboardInterrupt) as error:
        print('TRIAL_FAILED: ' + type(error).__name__, file=sys.stderr)
    finally:
        ended = cleanup(directory, state)
    print('Elapsed HTTPS trial seconds: %.3f (not setup or reading time)' % (time.monotonic() - start))
    return 0 if ok and ended else 1


if __name__ == '__main__':
    sys.exit(main())
