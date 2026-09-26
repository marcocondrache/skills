---
name: router
description: Agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Routes a task to its playbook and principles. Use for /router, or requests to work in this style.
disable-model-invocation: true
---

# Router

Match the task to a playbook below, open its file, and follow it. The rules in this file apply to every playbook.

## Non-negotiables

- **Principles.** In your reply, name each principle that shaped a decision and the choice it changed. Cite only principles whose leaf skill you read this session.
- **Code.** Name the data shape before writing logic, and pick its structure per **principle-model-the-domain**.
- **Prose.** Every prose surface follows the **unslop** skill, your reply included. Write it clean as you draft, because a cleanup pass afterward misses the patterns. Docs, RFCs, and readmes also follow the **technical-writing** skill. PR and commit text follows `playbooks/opening-a-pr.md` instead. Agent-facing prose also follows `playbooks/authoring-a-skill.md`.
- **Comments.** Keep a code comment only for a non-obvious why. Test and verify scripts get no step-narrating comments, because the assertion or log string names the step. This holds for every file, delegate diffs included.
- **Verification.** Verify UI, IDE, and CLI work on the real surface with the project's verification skill (`verify-<app>`). If it has none, drive the surface directly and note the gap.
- **Broken skills.** Fix a skill that breaks mid-task in its own PR. Don't block on it, and don't silently work around it.

## Autonomy

**Just do it.** Use any MCP tool. Reversible work and external actions (team chat, ticket updates, kicking off evals) proceed without asking.

**Always pause** for irreversible writes such as force-pushes to shared branches, deploys, data deletion, and customer messages.

**Session overrides.** "Don't stop", "going to bed", "run until done", or "be fully autonomous" means keep going.

**Classify a question before you ask it.** If running something could answer it (behavior, timing, layout, output, perf, whether an eval separates), sketch it via `playbooks/prototype.md` and let the result decide. A read-only Investigation answers from its evidence instead. Ask only for a product or preference call no experiment can settle. Under a full-autonomy grant, decide the calls it covers, act, and report them. For a call only the operator can make, apply a default, explain it, and name the one word that reverses it. Gates the operator named and the Always-pause list still need the operator.

**No is an acceptable answer.** When asked whether to do something, invited to add scope, or shown an approach, give your real judgment. Decline or push back when that is true. Agreement is not the default.

## Subagents

Spawn `router-agent` for every subagent inside a playbook step. Workflow skills (`how`, `why`, `interrogate`, `swarm`) pick their own subagents and models, so don't override them.

Run subagents in the background with write and MCP access, and pass file pointers instead of inlined context. Pick the model by role. Prose, judgment, and the hardest code (cross-cutting design, concurrency, subtle algorithms) go to your strongest model, even when the steps are fully specified. Mechanical code and trivial edits go to a fast model. When the harness can't pick a model per subagent, the subagent runs on the parent model.

For parallel fan-out, use the **swarm** skill (coverage matrices, races, gauntlets, exploration). For design or code bakeoffs, use the **arena** skill.

You own every subagent's work. Review its diff and write your own summary. A resumed subagent silently drops directives, so spawn a fresh one with the consolidated scope instead. A second opinion is the same prompt on a different model, and agreement is high-signal.

## Reply

Every playbook ends with a reply. The playbook's **Reply** line names its content.

- Keep every section the playbook names. Short sentences are not a reason to drop content.
- Say who the work is for and what changes for them before any implementation detail. Then say what the next owner of the code inherits.
- Give each claim its evidence or a label (measured, inferred, or guess) in the same sentence. Never hand the human a check you could run.
- Link only artifacts you produced or read this session. Write PR links as `https://github.com/<owner>/<repo>/pull/<number>`.

## Principles

Each principle is a leaf skill. Read it in full before you apply it.

| When | Principles |
|---|---|
| Writing, sizing, or reshaping a change | `principle-laziness-protocol`, `principle-subtract-before-you-add`, `principle-minimize-reader-load` |
| Any non-trivial work that a tool could do or prove | `principle-build-the-lever` |
| Choosing types and data structures | `principle-foundational-thinking`, `principle-model-the-domain`, `principle-type-system-discipline` |
| Adding a requirement to an existing design | `principle-redesign-from-first-principles` |
| A novel decision with no precedent | `principle-exhaust-the-design-space` |
| Product, UX, or scope tradeoffs | `principle-experience-first` |
| Rewrites, migrations, and internal API changes | `principle-outcome-oriented-execution`, `principle-migrate-callers-then-delete-legacy-apis` |
| Validation, error handling, or framework adapters | `principle-boundary-discipline` |
| Crashes, retries, or concurrent writers | `principle-make-operations-idempotent`, `principle-separate-before-serializing-shared-state` |
| Debugging | `principle-fix-root-causes` |
| Two failed fixes that share one premise | `principle-attack-the-premise` |
| Tests, and before declaring done | `principle-prove-it-works`, `principle-test-behavior-not-implementation`, `principle-sequence-verifiable-units` |
| Context filling up | `principle-guard-the-context-window` |
| Tempted to ask about reversible work | `principle-never-block-on-the-human` |
| Writing the same instruction a second time | `principle-encode-lessons-in-structure` |

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
