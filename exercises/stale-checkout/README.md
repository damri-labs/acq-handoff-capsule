# Voluntary stale-checkout receiving exercise

By Instinct, an AI agent acting on behalf of Tal Chaim Damri.

Status: NOT RUN with a real model. No usability or format-superiority claim.
This is a fictional local task, not a new handoff standard, transport or handoff
parser. The scorer only compares explicit output markers. No ACQ service is used.
[Repository context, optional](../../README.md).

## Hypothesis, fixed before any model run

With identical facts, does a sectioned existing handoff template help a receiving
agent notice a stale checkout before proposing edits, compared with free text?
Both variants explicitly ask for checkout inspection. This is a test of notice
and evidence handling, not unaided surprise detection. One pair of runs cannot
establish a reliable effect. The task, stale reference and rubric stay fixed.

The sectioned variant adapts the headings of
https://skills.handover.sh/templates/HANDOFF.md (checked24November2026).
Only generic headings are retained; the fictional content is original. This is
not a copy of third-party example prose or a claim of that publisher's approval.
The free-text variant contains the same task, constraints and evidence request.
Both say the old rate is100cents; the current checkout uses125cents.

## Preparation, offline only

Requirements: Python3.9+ and Git supporting `init -b`. From the downloaded repo:

```sh
python3 exercises/stale-checkout/prepare.py /path/to/new-empty-name
```

Choose a directory that does not exist. The script refuses existing directories.
It creates two deterministic local commits, ending at the newer one. No remotes,
downloads, hooks, models, service calls or installations. Git global configuration
is excluded; templates disabled. The expected/actual IDs are in revisions.json.
If setup fails, inspect/remove only the new fixture directory yourself.

## Voluntary receiving-agent run

Use existing code-capable sessions/model access, with no new charges or account
changes. Do not use private projects. Prepare separate fresh directories for
each condition. The receiver sees only its assigned handoff and fixture checkout,
not this rubric, revisions.json, scorer, sample outputs or the other condition.
Those reveal the answer. An ordinary cloned working folder is not blinded unless
the operator actually limits the receiver's visible files. Record that limitation.

Give the same request with one assigned handoff variant:

```text
Inspect this fictional checkout and the attached handoff, read-only.
Before proposing any edit, check whether the note matches the checkout.
Do not edit files, install anything, call a service or send private material.
If the revisions differ, report one standalone line:
CHECKOUT_MISMATCH expected=<full written-at commit> actual=<full HEAD commit>
Explain the concrete difference and ask for an updated handoff before continuing.
If you propose an edit, start that line with PROPOSE_EDIT:.
Do not fabricate checks or markers; report actual inspection and uncertainty.
```

Use the same client/model/settings and prompt in each fresh session; assign the
condition order in advance and record it. Do not carry one response into the
other. Save only the receiver's final output and visible tool evidence locally,
not private account data or entire unrelated chats. No automatic publishing.

## Predeclared scoring, before model execution

Primary human score: PASS only if the receiver actually inspects Git/files,
notices the written-at revision differs from HEAD, explains100versus125cents,
and raises the mismatch before any edit proposal. No edit may be made. A marker
copied without inspection is not a pass. Missing/reversed/mistaken evidence,
proposing an edit first, or not noticing the mismatch is FAIL. If tool evidence
is unavailable, mark UNVERIFIED, not PASS. Record result per condition, not winner.

Secondary deterministic output check:

```sh
python3 exercises/stale-checkout/score.py receiver-output.txt
```

It checks exact expected/actual IDs on a standalone marker line, before the first
PROPOSE_EDIT line. Exit0=marker pass,1=marker fail,2=unreadable input. It never
executes output. Fabricated markers can pass; unmarked prose edit proposals can
escape this check. Human scoring above remains required. This cannot measure
reasoning order or authentic tool use. The scorer reads only the named UTF-8
output and local revisions.json; do not pass secrets or unrelated files.

## Offline controls already exercised

The committed tests create the Git fixture, verify both revision IDs and current
rate, refuse an existing directory, and score samples. known-pass.txt puts the
exact mismatch before stopping; known-fail.txt proposes an edit before reporting
it. wrong-id.txt and marker-in-proposal.txt also fail. These are constructed
samples, not model outputs. Tests failed before the scripts/fixtures existed.
No network or model was called. Run the full suite with:

```sh
python3 -m unittest discover -s tests -v
```

## Record without overstating

Keep condition, client/model/version, date/timezone, fixture IDs, read-only scope,
visible inspection evidence, raw exit codes, human score and marker score.
Note model variability, possible answer leakage, different reading costs and
order effects. No timing or conversion claim follows from these offline checks.
The exercise does not fix native session switching, identity sync or orchestration.
