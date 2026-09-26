---
name: router
description: Agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Routes a task to its playbook. Use for /router, or requests to work in this style.
disable-model-invocation: true
---

# Router

Read `rules.md` in this skill's directory first. Its rules apply to every playbook, and it says where the skills named here live. Then match the task to a playbook below, open its file, and follow it. Paths in this file are relative to its directory.

## Autonomy

**Just do it.** Use any MCP tool. Reversible work and external actions (team chat, ticket updates, kicking off evals) proceed without asking.

**Session overrides.** "Don't stop", "going to bed", "run until done", or "be fully autonomous" means keep going.

**Classify a question before you ask it.** If running something could answer it (behavior, timing, layout, output, perf, whether an eval separates), sketch it via `playbooks/prototype.md` and let the result decide. A read-only Investigation answers from its evidence instead. Ask only for a product or preference call no experiment can settle. Under a full-autonomy grant, decide the calls it covers, act, and report them. For a call only the operator can make, apply a default, explain it, and name the one word that reverses it. Gates the operator named and the irreversible writes in `rules.md` still need the operator.

**No is an acceptable answer.** When asked whether to do something, invited to add scope, or shown an approach, give your real judgment. Decline or push back when that is true. Agreement is not the default.

## Subagents

Spawn `router-agent` for every subagent inside a playbook step. Pass it the task (file paths, the data shape, and success criteria) and the path to `rules.md`. Workflow skills (`how`, `why`, `interrogate`, `swarm`) pick their own subagents and models, so don't override them.

Run subagents in the background with write and MCP access, and pass file pointers instead of inlined context. Pick the model by role. Prose, judgment, and the hardest code (cross-cutting design, concurrency, subtle algorithms) go to your strongest model, even when the steps are fully specified. Mechanical code and trivial edits go to a fast model. When the harness can't pick a model per subagent, the subagent runs on the parent model.

For parallel fan-out, use the **swarm** skill (coverage matrices, races, gauntlets, exploration). For design or code bakeoffs, use the **arena** skill.

You own every subagent's work. Review its diff and write your own summary. A resumed subagent silently drops directives, so spawn a fresh one with the consolidated scope instead. A second opinion is the same prompt on a different model, and agreement is high-signal.

## Reply

Every playbook ends with a reply. The playbook's **Reply** line names its content.

- Keep every section the playbook names. Short sentences are not a reason to drop content.
- Say who the work is for and what changes for them before any implementation detail. Then say what the next owner of the code inherits.
- Give each claim its evidence or a label (measured, inferred, or guess) in the same sentence. Never hand the human a check you could run.
- Link only artifacts you produced or read this session. Write PR links as `https://github.com/<owner>/<repo>/pull/<number>`.

## Playbooks

Open a todolist whose first items are the matched playbook's steps, copied verbatim. A step you skip stays in the list as `skip: <reason>`.

When no playbook fits, work without one.

| Task | Playbook |
|---|---|
| Read-only question. How does X work, why is Y built this way, are we sure about Z, X or Y | `playbooks/investigation.md` |
| A reported defect to reproduce, root-cause, and fix | `playbooks/bug-fix.md` |
| A slowness to fix against a measured baseline | `playbooks/perf-issue.md` |
| New or changed behavior | `playbooks/feature.md` |
| A behavior-preserving structure change (rename, extract, inline, dedupe, move) | `playbooks/refactoring.md` |
| A throwaway sketch to settle a design or empirical fork ("prototype", "mock it up", "try this layout") | `playbooks/prototype.md` |
| Writing or editing a skill | `playbooks/authoring-a-skill.md` |
| The end of every other playbook | `playbooks/opening-a-pr.md` |
