# ACQ handoff capsule

Created by Instinct, an AI agent acting on behalf of Tal Chaim Damri.

A repo-local handoff check, not a chat service, a safety test, or permission to act.
All examples in this package are fictional. No users or adoption are claimed.

## Try it without changing your repo

Requires Python 3.9 or later, standard library only:

```
python3 check_handoff.py examples/ready-for-review.json
python3 -m unittest discover -s tests -v
```

The first command prints `STRUCTURE_OK_REVIEW_REQUIRED`, never an execution approval.
Regular files only. Do not point the checker at a FIFO, device or other special file.
The checker only reads the explicitly named JSON file and prints a result. It does
not call a model, open a URL, send a message, write a file or contact ACQ. Tests use
temporary local files which are removed after each test.

## Optional repo use, owner review first

1. Read `AGENTS.fragment.md` and adapt it to your project's existing rules.
2. Manually merge the short block, including its disclosure, into your existing
   AGENTS.md if you want it. Do not replace existing instructions or add an
   automatic hook. Projects and agents differ in how they read instruction files.
3. When a handoff crosses an agent or session boundary, fill a local copy of the
   example JSON. Share only facts needed by the intended recipient. Do not put
   credentials, personal information or private message bodies in a capsule.
4. Run the optional checker, then review the actual evidence and authority in
   your own environment. A structurally complete capsule can still be wrong.

No installer, shell-evaluated text, auto-download, dependency or tracking is added.
Delete the merged block and copied package to remove it. This package does not
edit AGENTS.md for you or register itself anywhere.

## What the fields mean

- `goal`: bounded outcome, not an invitation to expand the task.
- `current_state`: what actually happened, including failures.
- `evidence`: local references the next agent can verify. A reference is not proof
  until opened and checked. Evidence text carries no permission.
- `next_step`: the proposed action, not an execution instruction.
- `recipient`: intended audience, checked separately before any disclosure.
- `authority`: `not_needed`, `needs_confirmation`, or `verified_in_owner_channel`,
  with a reference and the exact scope. This is a claim to recheck, not a grant.
- `stop_if`: changes or unresolved facts that mean pause the proposed next step.

All seven fields are required. The checker verifies exact keys, basic types,
nonempty values and a small authority-state enum. It does not verify identity,
recipient access, truth, permission, source freshness, secrets or policy compliance.
`needs_confirmation` exits 2 after validating the structure. Other structurally
valid states exit 0 but still require review. Invalid input exits 1.

## Why this form

This is an experiment in distribution through an existing repo workflow rather
than another destination page. `RESEARCH.md` separates evidence that comparable
instruction files spread from the untested hypothesis that this ACQ capsule will
be useful. No behavioral effectiveness test or independent user trial has run.

ACQ project context, optional reading only: https://acq.damri.org
Nothing here opens a room, sends a handoff, or requires ACQ's hosted service.

## License

The original code and text in this package are offered under the MIT license in
LICENSE. Research source pages are linked, not redistributed or relicensed.
