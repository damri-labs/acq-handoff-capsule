# Pinned trial source fixture

By Instinct, an AI agent acting on behalf of Tal Chaim Damri.

pinned-TRIAL.md is the exact tracked TRIAL.md blob from merged main commit
6743a399e676c2681def076148264862035a509a, not a separately maintained helper.
The offline regression verifies its full-file hash against SHA256SUMS for
TRIAL.md and its extracted helper against the current card helper. Updating
TRIAL.md intentionally requires reviewing and updating this pin and fixture.
Contributor note: any TRIAL.md edit must update both README prompt pins and
this fixture in the same PR, together with SHA256SUMS.
No network execution is part of these tests.
