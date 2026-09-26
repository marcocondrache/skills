# AGENTS.md

This is Marco's personal collection of agent skills, subagents, and rules for high-quality engineering work. It started as an import of [pstack](https://github.com/cursor/plugins) (poteto's plugin) and is meant to diverge from it. Treat the pstack content as a starting point to reshape, not an upstream to stay compatible with.

## Layout

- `skills/<name>/SKILL.md` is one skill. Supporting files sit next to it in `references/` (prompts, templates, rubrics loaded on demand), `playbooks/` (step lists a skill routes to), and `scripts/` (executable tools).
- `skills/router/SKILL.md` holds the rules every playbook shares and routes tasks to its playbooks.
- `agents/*.md` are subagent definitions. `router-agent` wraps `router`, and `comment-sicko` is spawned by the `no-comments` skill.
- `.claude-plugin/` packages the repo as a Claude Code plugin and marketplace. Skills and agents are discovered from their directories, so adding one needs no manifest change. Bump `version` in `plugin.json` when a change should reach installed copies.

## Editing skills

- Frontmatter needs `name` and `description`. The description is the trigger, so write it as when to use the skill, with the phrases a user would type.
- Keep `disable-model-invocation: true` unless the skill should load on its own. Add `paths` for file-type skills (see `typescript-best-practices`).
- The directory name is the skill's id. Other skills cite it by that id, so a rename means updating every reference. Find them with `rg -n '<old-name>'`.
- Delegate to another skill by name or path instead of restating its rules.
- `unslop` rule numbers are stable ids that other skills cite. Removing a rule leaves a gap in the numbering.
- Keep only prose that changes a decision. When in doubt, delete.
- Write every prose file per the `unslop` skill. No em dashes, sentence case headings, no mid-sentence colons, no filler.

## Customizing away from pstack

- Changing or deleting inherited content is expected. Don't add compatibility shims or keep a skill alive only because pstack has it.
- Keep every skill harness-agnostic. Don't name one harness's tools, paths, plugins, config files, or model ids. Describe the capability instead ("spawn a subagent", "ask the user", "your strongest model", "the project's skills directory").
- When you rename or remove a skill or playbook, update its entry in `skills/router/SKILL.md` and any agent that points at it in the same change.
- Keep `LICENSE` intact. It is MIT and carries both copyright lines.
