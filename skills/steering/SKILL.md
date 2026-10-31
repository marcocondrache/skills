---
name: steering
description: "Pick where an instruction for a coding agent should live (steering file, path-scoped rule, skill, subagent, hook, permission, system prompt) and at what scope. Use for 'where should this rule go', 'should this be a hook or a skill', 'the agent keeps ignoring X', 'our steering file is too long', 'make the agent always/never do Y', or 'set up the agent for this repo'."
disable-model-invocation: true
---

# Steering

Every way to steer a coding agent trades context cost against authority. Pick the cheapest mechanism that still has the authority the instruction needs, and load it only when it matters.

Adapted from Anthropic's article [Steering Claude Code](https://claude.com/resources/articles/steering-claude-code-skills-hooks-rules-subagents-and-more). The mechanism names below are generic. Map each one to what the target harness calls it.

## Steps

1. Write the instruction as one sentence and name its kind. It is a fact about the codebase, a constraint on some files, a procedure, a side task, a guarantee ("always", "never"), or a tone or format preference.
2. Pick the mechanism with the decision rules below, then check it against the table.
3. Pick the scope. Personal preferences go at user scope, which loads in every session in every repo. Team and codebase conventions go at project scope. An org-wide guarantee goes in admin-managed settings, which local config can't override or exclude.
4. Write it there, and delete the old copy in the same change.

## Decision rules

- **"Always do Y" is a hook.** An agent choosing to run the formatter is not the formatter running on every edit. Prose asks, a hook makes it happen.
- **"Never do X" is a hook or a permission.** Agents drop prose rules under pressure, deep in long sessions, in ambiguous cases, and when a file they read injects instructions. Deny the action with a pre-tool hook or a permission rule. For an org-wide guardrail, use managed settings.
- **A procedure is a skill.** A steering file entry past about 30 lines, or any multi-step workflow (deploy, release, review), moves to a skill.
- **A constraint on some files is a path-scoped rule.** A rule without path globs loads everywhere, which makes it the same as writing it in the root steering file. Scope it ("migrations are append-only" on the migrations glob). Prefer path-scoped rules to nested steering files for concerns that cut across directories.
- **A side task whose intermediate output you won't reuse is a subagent.** Deep search, log analysis, and dependency audits fit. When you want to watch and steer each step, use a skill instead, because skills run in the main conversation.
- **Tone and format go in the system prompt.** Append for one run, or use an output style to persist it.
- **Model and effort are separate dials.** They change capability and effort, not instructions. Don't write prose to fix a model that is too weak for the task.

## Mechanisms

| Mechanism | Loads | After compaction | Context cost | Good for |
|---|---|---|---|---|
| Root steering file | Session start, for the whole session | Re-read | High, paid every session | Build commands, layout, conventions, pointers |
| Subdirectory steering file | When the agent reads a file in that directory | Gone until the directory is touched again | Low | Per-team or per-package conventions |
| Unscoped rule | Session start | Re-injected | Same as the root file | Almost nothing; scope it or move it to the root file |
| Path-scoped rule | When a file matching its globs is touched | Reloads on the next match | Low | File-specific and cross-cutting constraints |
| Skill | Name and description at start, body on invocation | Re-injected within a shared budget, oldest dropped first | Low until invoked | Procedures the user or agent invokes |
| Subagent | Name, description, and tool list at start. Body only in its own context | Unaffected, it has its own context | Only its final message returns | Noisy side tasks |
| Hook | Runs outside the context on lifecycle events | Not applicable | Low, output returns only if configured | Guarantees, blocking, automation |
| Output style | Session start, never compacted | Kept | Moderate to high | Persistent tone and format, highest instruction weight |
| Appended system prompt | One invocation, not persisted | Kept | Adds input tokens, cached after the first request | Per-run standards, format, domain facts |

## Steering files

- Keep the root file under 200 lines. Every line costs tokens in every session, and adherence drops as the file grows.
- Give it an owner and review changes to it like code. In shared repos, teams append and nobody deletes, so prune on every edit.
- Make it an index. State the build commands and layout, then point at docs, rules, and skills for the rest.
- Be explicit. Give the reason behind a constraint and an example when the rule is unclear without them.
- In a monorepo, give each team a subdirectory file, and let developers exclude the ones for code they never touch.
- Leave out long procedures, file-specific constraints, and anything only some tasks need.

## Hooks

- Hooks can be shell commands, HTTP calls, or tool calls, which act the same way every time. They can also be model prompts or agents, which use judgment. Pick a deterministic hook for a guarantee.
- Register a hook in settings, in managed policy, or in a skill's or subagent's frontmatter so it runs only while that skill or subagent is active.
- A blocking hook's error output goes back into context, so the agent learns why it was denied. Write that message as the fix ("use `pnpm`, not `npm`"), not just "denied".
- A hook's output stays out of context unless you return it. A hook that writes a backup file before compaction is useless to the agent until it says where the file is.
- Skills and hooks together build agent loops that repeat until a stop condition holds.

## Skills and subagents

- A skill's description is all the agent sees until it loads. Write it as when to use the skill, with the phrases a user would type.
- A subagent's body becomes its system prompt and never enters the parent conversation. Only its final message and metadata come back, so ask for that message in the shape you need.
- Subagents can nest and fan out. Large workflows keep plans and intermediate results in script variables, not in any agent's context.

## System prompt

- An output style replaces the default system prompt unless it says to keep the coding instructions. Without that, the agent loses its defaults for scoping changes, comments, security, and running tests, and acts as a general assistant. Check the built-in styles before writing one.
- Appending is additive and keeps the agent's role. A verbose style also raises output tokens.
- More instructions earn less adherence each, and conflicting ones earn the least. Cut before you add.

## Sharing

Once a few mechanisms work, bundle the skills, subagents, hooks, and output styles into a plugin so teammates and other projects get the same setup.

**Reply:** each instruction with its kind, the mechanism and scope chosen, the target file, and the text or config to write. List anything to delete from its old place.
