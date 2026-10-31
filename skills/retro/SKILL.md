---
name: retro
description: "Run a retrospective on a coding session and propose changes to the agent's environment (steering files, checks, review rules, skills, tooling) so the next run goes better. Use for 'retro', 'run a retro on this session', 'what should we change after that', or 'why did that take so long'."
disable-model-invocation: true
---

# Retro

Look back at a session and propose changes to the environment the agent worked in, not to the code it wrote. The goal is a next run that finds things faster and makes fewer mistakes.

## Steps

1. Read the session. Default to the current one. If the user names another, find its transcript in the session logs on this machine. Read the primary record (tool calls, errors, user corrections), not a summary of it.
2. Mark the moments that cost something. A long search for a file, a mistake the user or a reviewer caught, a command retried after failing, a tool output far larger than needed, a fact the agent had to ask for or guess. Every candidate must point at one of these moments.
3. Read the environment those moments touched. The steering files at repo and user scope, the repo's check commands (build-tool scripts, pre-commit hooks, CI workflows), its docs, and the skills that loaded or should have.
4. Sort each moment into a category below and write the fix.
5. Present the candidates, most severe first. Apply nothing until the user picks.

## Categories

- **Navigation.** The agent took long to find a file, or tripped on a hidden dependency between files. Add a navigation pointer to the file the agent was already reading.
- **Automated checks.** The agent made a mistake a linter, type check, test, or file-layout check could catch. Read the repo's own check command and CI first. A check that exists but isn't wired up or is silently broken is the finding, not a new check. A repo with no guardrail (no pre-commit hook and no CI job running its checks) is a finding on its own.
- **Review rules.** A mistake got past review. Classify it first. A mechanical violation (a banned API, an import shape, a fixed syntactic pattern, a file-location rule) gets a deterministic check in the repo's linter, a hook, or CI, whichever is cheapest. Write a prose rule only for a judgment call no check could make, like cross-file consistency or matching the surrounding style.
- **Steering files.** A steering file is large, or holds rules that belong in a check or a review rule. Move them out.
- **No-ops.** A steering instruction didn't change what the agent did. Delete it.
- **Skills.** A skill missed a matching request, loaded on one that didn't match, or gave steps the agent ignored or couldn't follow. Or the agent repeated a workflow no skill covers. Fix the description for a load miss and the body for a behavior miss.
- **Tool economy.** A tool call returned far more than the agent needed, or ran many times where once would do. Propose a narrower command, a flag, or a small script.
- **Information access.** A fact the agent needed wasn't reachable. Propose access to it, like teeing dev server logs to a file or read-only access to a third-party service.

## Where each fix goes

Implementation carries the most context, because that agent explores, writes code, and debugs. Review gets a diff and little else. So coding standards belong in review, not in what implementation loads.

To choose between a steering file, rule, skill, subagent, hook, or permission, follow the `steering` skill.

- Steering files load into every agent's context. Keep them to navigation pointers and the few rules every task needs.
- Review rules load only at review. Once they pass about 1,000 lines, split them into docs and leave pointers.
- Docs are reference files something else points to. Look for an existing doc before writing a new one.
- Skills hold workflows a user invokes and reference material an agent loads on a matching task, since only the description sits in context until then.

## What to hand back

For each candidate:

- the session moment, quoted or cited
- its category
- the change, naming the target file and the exact text or check to add, edit, or delete
- its severity, from how often it will recur and what it cost this time

Write it through `unslop`.

**Reply:** the ranked candidates, then ask which to apply.
