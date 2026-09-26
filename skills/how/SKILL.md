---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Answer "how does X work?" at the level a senior engineer needs to start working in the area. Give them a working mental model, not annotated source.

## Steps

1. Scope the question. If it's ambiguous, state your reading and go on. The user can redirect.
2. Read the code yourself. Find the entry point (a user action, an API call, a job), follow the call chain function by function, and read the core types. Note where the area meets the rest of the codebase and anything a newcomer would get wrong. Read the implementation instead of guessing from names. If you can't trace a part, say so.
3. Write the explanation in the format below.

For a subsystem too big to read in one pass (many files across services, or a cross-cutting feature), split it into 2 to 4 distinct slices first. Spawn one read-only explorer per slice on a fast model, all in one message, each with the prompt in `references/explorer-prompt.md`. Then write the explanation yourself from their findings, and check the code where they overlap or disagree.

## Output format

Drop any section that doesn't apply.

- **Overview.** One or two paragraphs on what it is, what it does, and why it exists. A reader should be able to stop here.
- **Key concepts.** The types, services, or abstractions the rest depends on, one line each.
- **How it works.** The longest section. What triggers the flow, what happens step by step, where data goes, and where it branches. Use prose that names real files and functions, not pseudocode or large code blocks. Add a mermaid or ASCII diagram only when components talk to each other or data changes shape across stages.
- **Where things live.** The files and directories someone needs to start working here.
- **Gotchas.** Surprising behavior, historical leftovers, and pitfalls.

Write concretely. "`UserService` calls `AuthClient.refresh()`" beats "the service delegates to the client". Name open questions instead of papering over them.
