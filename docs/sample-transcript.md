# Historical synthetic sample transcript

By Instinct, an AI agent acting on behalf of Tal Chaim Damri.

Date: 2026-11-24, Asia/Jerusalem (capture 2026-11-24T00:32:20.997647+00:00 UTC). Synthetic scripted two-process run, not a model run. No adoption claim.

This capture is from before the failure-diagnostics edit. Its timings do not
validate the current helper revision. For the current failure-marker format, see
[the offline preview](offline-first-trial-preview.txt).

The helper was extracted unchanged from main TRIAL.md at the time of capture. SHA256 of extracted trial.py bytes: `0ec88e818c32d5622fb2275cb8e7e868eea5f7e95cdb9d9dff3c611f5d9e35e6`. Both exit codes were 0; overall elapsed 2.013 seconds. This excludes setup/reading/model work.

Outputs below are verbatim except labeled omissions of invitation/private recovery-path lines. No seat token is printed by the helper.

## Seat A

```text
Instinct, acting on behalf of Tal Chaim Damri. Scripted seat A
[private recovery-path line omitted]
[invitation line omitted]
CORRELATED_PONG_RECEIVED_VIA_ROOM.
ENDED_VERIFIED; local private state removed.
Measured seat seconds: 1.971; excludes setup/reading/model work.
```

## Seat B

```text
Instinct, acting on behalf of Tal Chaim Damri. Scripted seat B
[private recovery-path line omitted]
PING_RECEIVED; PONG_SENT_VIA_ROOM.
ENDED_VERIFIED; local private state removed.
Measured seat seconds: 1.611; excludes setup/reading/model work.
```

## Offline preview of separate scripted recovery helper

Command: `python3 try_acq.py --dry-run`. Exit 0. This is not the two-process helper above. Preview captured from the merged PR13 version of try_acq.py, before PR14 cleanup validation. SHA256 of those historical bytes: `32d90c89c04e2db382d3aa3ee23b827e647e877b47aa93357352c55a3532fdda`.

```text
DRY_RUN: zero network calls; no room, files or private state created.
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
By Instinct, an AI agent acting on behalf of Tal Chaim Damri.
```

## Scope of this evidence

This capture shows a successful synthetic ping/pong and verified ending, and the offline preview output. It does not commit evidence of prior interruption, unreachable-relay or timeout rehearsals, prove real-client skill triggering, authenticate model execution, or prove literal 120-second no-peer behavior. Those earlier local rehearsals remain labeled not committed in the technical write-up.

During capture preparation, an invitation-line parsing mistake left a first scripted room without B until the runner was stopped. Its saved-state cleanup was then run and reported ENDED_VERIFIED before the successful fresh run above. No credentials or invitation are included here.
