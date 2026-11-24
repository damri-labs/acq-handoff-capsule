# Fictional estimate handoff

Adapted structure from https://skills.handover.sh/templates/HANDOFF.md.
Headings are retained; wording below is original fictional exercise content.
By Instinct, acting on behalf of Tal Chaim Damri.

## Goal
Add a quantity limit of 20. No edits before checking the checkout.

## Current state
The estimate multiplies quantity by 100 cents. Written at commit `0c8f9e1dc93ab38a9069638cb57f75bd0ab75351`.
The limit is not implemented. Nothing has been tested for this change.

## Decisions
Keep the integer-cent interface; do not change the per-item rate.

## Evidence
Inspect estimate.py and Git history in the supplied exercise checkout.

## Next action
Receiving agent: inspect the checkout, then propose how to add the limit.

## Open risks and questions
Confirm which checkout the note describes before using its claims.

## Relevant artifacts
estimate.py, Git HEAD and the written-at commit above.
