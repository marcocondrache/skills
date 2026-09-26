---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

The parent finds its own transcript file before fanning out. Transcripts live in the harness's transcript store for the current workspace. Find it from the system prompt or the harness docs. If no transcripts are reachable, write a tight digest of the session and pass that instead. Never read transcripts from other workspaces. They hold private chats from unrelated projects.

List the newest transcript files in that store and pick candidates. For each candidate, check that its first entry contains the conversation's opening user prompt. Take the matching path. If no path resolves, pass the digest.

### 2. Spawn three reviewers in parallel

Spawn three general-purpose subagents in one message, with write and MCP access. Reviewers need MCP access for context lookups (tickets, chat threads, observability traces referenced in the transcript). Put each reviewer on a different model family when the harness offers several. Otherwise run them all on the parent model, each in a fresh context.

| Lens | Prompt template |
|---|---|
| Judgment | `references/judgment-reviewer.md` |
| Tooling | `references/tooling-reviewer.md` |
| Divergent | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in their final response.

### 3. Synthesize

Spawn one general-purpose subagent on your strongest model, with write and MCP access. The synthesizer's quality check includes spot-verifying citations, which can require MCP access. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Backlog items file to whatever devex / backlog tracker your team uses automatically. Only the Accepted list waits for approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): follow the router's authoring playbook, `../router/playbooks/authoring-a-skill.md`.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): rewrite the description to lead with the phrases a user would type in the missed case, per the same playbook.
- `new skill: <kebab-name>`: create it through the same playbook. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
