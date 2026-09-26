# Skills

**Skills** is my personal collection of agent skills, subagents, and rules for high-quality engineering work. Plain Markdown that works with any harness that loads skills.

Started from **[pstack](https://github.com/cursor/plugins)**.

### ✦ What it is

- A set of skills for planning, debugging, testing, reviewing, and writing
- A library of single-rule principles, indexed by the `router` skill
- A few subagents the skills spawn when a task needs a second pair of eyes

### ✦ What it is not

- A framework or a plugin with its own runtime
- A mirror of pstack kept in sync with upstream
- Tied to one harness, editor, or model

### ✦ Why not pstack

pstack is good, but it's someone else's workflow. It's shaped around how its author works, down to the names, and adopting it meant bending my habits to fit.

It also carries a lot of machinery, like an orchestrator with its own store, a PR watcher CLI, and bootstrap scripts. That's code to install and maintain next to the prose, and I wanted skills that are just Markdown.

### ✦ Philosophy

An agent does its best work when the rules are few, sharp, and loaded only when they matter. Each skill says when to use it and what changes the decision, and nothing else.

The collection is meant to be reshaped. Skills get rewritten, merged, or deleted as the way I work changes, and every one of them stays harness-agnostic so it moves with me.
