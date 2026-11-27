# AGENTS.md

This is Marco's personal collection of Claude Code skills, subagents, and hooks for high-quality engineering work. It started as an import of [pstack](https://github.com/cursor/plugins) (poteto's plugin) and is meant to diverge from it. Treat the pstack content as a starting point to reshape, not an upstream to stay compatible with.

## Layout

- `skills/<name>/SKILL.md` is one skill. Supporting files sit next to it in `references/` (prompts, templates, rubrics loaded on demand) and `scripts/` (executable tools).
- `agents/*.md` are subagent definitions. `comment-sicko` is spawned by the `no-comments` skill.
- `.claude-plugin/` packages the repo as a Claude Code plugin and marketplace. Skills and agents are discovered from their directories, so adding one needs no manifest change. Bump `version` in `plugin.json` when a change should reach installed copies.

## Editing skills

- Frontmatter needs `name` and `description`. The description is the trigger, so write it as when to use the skill, with the phrases a user would type.
- Keep `disable-model-invocation: true` unless the skill should load on its own. Add `paths` globs for a skill tied to a file type.
- The directory name is the skill's id. Other skills cite it by that id, so a rename means updating every reference. Find them with `rg -n '<old-name>'`.
- Delegate to another skill by name or path instead of restating its rules.
- `unslop` rule numbers are stable ids that other skills cite. Removing a rule leaves a gap in the numbering.
- Test a skill meant to change what an agent does. Give a fresh agent three to five requests that should load it and one or two near-misses that should not. It must load on the first, stay out on the second, and be followed once loaded.
- Keep only prose that changes a decision. When in doubt, delete.
- Write every prose file per the `unslop` skill. No em dashes, sentence case headings, no mid-sentence colons, no filler.

## Claude Code first

- Write for Claude Code. Name its tools, subagents, and config by their real names.
- Reach for a Claude Code feature when it makes a skill more reliable or saves context. Load state the skill always needs with `` !`cmd` ``, pre-approve read-only commands with `allowed-tools`, enforce a "never" rule with a hook in the skill's frontmatter, and run a self-contained task that returns a report with `context: fork` and an `agent`.
- Don't fork a skill that needs the conversation. A forked subagent sees only the skill's text.
- Check a frontmatter key or hook field against the current Claude Code docs before you use it, and run the skill with `claude --plugin-dir .` to see it work.
- Put scripts a skill or hook runs in the skill's `scripts/`. Reference them with `${CLAUDE_SKILL_DIR}` in the body and `allowed-tools`, and with `${CLAUDE_PLUGIN_ROOT}` in hook commands.

## Customizing away from pstack

- Changing or deleting inherited content is expected. Don't add compatibility shims or keep a skill alive only because pstack has it.
- When you rename or remove a skill, update every skill and agent that points at it in the same change.
- When you add, rename, or remove a skill, update its row in `INDEX.md` in the same change.
- Keep `LICENSE` intact. It is MIT and carries both copyright lines.
