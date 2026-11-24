# Local Agent Skills format validation

By Instinct, an AI agent acting on behalf of Tal Chaim Damri.

Run date: 2026-11-24T00:51:10Z (02:51:10 Asia/Jerusalem).

Validator: skills-ref 0.1.0, installed locally from agentskills/agentskills commit `83021e2be457a9b6679148719c1f6074f0ad975e`.
Source: https://github.com/agentskills/agentskills/tree/main/skills-ref

Command from capsule repository root:

```sh
skills-ref validate .agents/skills/acq-two-seat-trial
```

Actual combined stdout/stderr:

```text
Valid skill: .agents/skills/acq-two-seat-trial
```

Exit code: 0.

Validated SKILL.md SHA256: `d6fb195a54d331f6434408ba64d632fc61c37123f62e93a0d46d12028610f706`.
Bundled references/TRIAL.md SHA256: `65d027b249522ea7e60f30a43860df4cff8a7d71483e2e3535f9248cfb78c20e`.

This validates the directory's format only. It does not prove client discovery or triggering, correct model behavior, real model-pair execution, network safety, or adoption. The owner has not yet run the trial with a real model pair. The captured successful two-process run was synthetic scripted Python, not models.
