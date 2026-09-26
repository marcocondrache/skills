# Architect runner prompt

The orchestrator passes this file through to every parallel candidate runner when Phase B runs arena, and fills in the variable inputs around it: the task, the Phase A grounding artifacts, the isolated working directory, and the path to write outputs. The working directory is a git worktree when available, otherwise a per-runner subdirectory under the sketch dir. What matters is independence between candidates.

You are producing one candidate design in architect's parallel exploration. Read the **architect** skill in full first and follow its Phase B discipline. Output a candidate design package: type sketch, function signatures, module map, and prose rationale shaped per [`rationale-template.md`](rationale-template.md).

You are one of several independent runners, often each on a different model. Produce the best design you can make. Don't hedge against the others. Differences between candidates are the signal used to pick a base and graft. Converging on a safe-looking middle defeats the exploration.
