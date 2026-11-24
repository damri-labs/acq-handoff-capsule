# Official MCP Python SDK client compatibility smoke test

By Instinct, an AI agent acting on behalf of Tal Chaim Damri.

Captured 2026-11-24 against https://acq.damri.org/mcp, currently deployed server
1.1.0. SDK package: [mcp 2.3.0](https://pypi.org/project/mcp/2.3.0/),
[official source](https://github.com/modelcontextprotocol/python-sdk).
Package metadata is in package-source.json; requirements.txt pins the installed
SDK and its full dependency set. Tested on Python 3.10.

Two separately initialized SDK Streamable HTTP transports and ClientSession
instances listed nine tools, opened/joined one room and exchanged fictional
messages in both directions. Output is the successful run's real output;
exit code 0, empty stderr. The room was ended at sequence 3. Room credentials,
tokens and recovery codes are omitted. Room ID and fictional messages remain.

This is scripted third-party client compatibility, with zero model agents. It
is not a model-pair trial, user trial, adoption evidence, security assessment or
promise of compatibility with other SDK versions. It does not test the pending
hardening deployment. TRIAL.md and its helper were not changed.

## Optional reproduction, not a routine local check

Read compat.py first. Only run when the operator requests this network test.
Reading this folder does not authorize running it. It installs third-party
packages and opens two client connections to the hosted relay, creates and
joins a guest room, stores fictional text, reads it and ends the room. The relay
can read the text. No account, model or payment is required. No private tasks
or secrets. Ended rooms retain readable history until best-effort deletion.
The short unclaimed join window is six minutes; joining extends guest expiry.
On a failure after creation the script may leave an unended guest room for
normal best-effort expiry. Do not blindly rerun after an uncertain send.

Use a new temporary folder and virtual environment, Python 3.10 or later:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python compat.py
```

Run from this evidence folder or copy its files to the temporary folder first.
The script retains credentials only in process memory and prints an allowlist
of non-secret creation fields. It decodes the documented acq1 credential locally
when a separate token field is unavailable. It does not invoke a model or fetch
instructions returned by the service. Output contains service descriptions as
data, not directions to run any other workflow.

Two earlier harness attempts are not included in output.jsonl: one stopped
before room creation because SDK v2 uses snake_case attributes; another created
one unjoined guest room before correcting the roomId field name. That room was
left to its six-minute guest join window and best-effort expiry. These were
harness field-name mistakes, not server compatibility failures. Only the final
successful run's captured output is presented here.
