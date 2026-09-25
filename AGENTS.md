# AGENTS.md

This is Marco's personal collection of agent skills, subagents, and rules for high-quality engineering work. It started as an import of [pstack](https://github.com/cursor/plugins) (poteto's plugin) and is meant to diverge from it. Treat the pstack content as a starting point to reshape, not an upstream to stay compatible with.

## Layout

- `skills/<name>/SKILL.md` is one skill. Supporting files sit next to it in `references/` (prompts, templates, rubrics loaded on demand), `playbooks/` (step lists a skill routes to), and `scripts/` (executable tools).
- `skills/principle-*/` are single-rule principle skills. `skills/poteto-mode/SKILL.md` indexes them and routes tasks to its playbooks.
- `agents/*.md` are subagent definitions. `poteto-agent` wraps `poteto-mode`, and `comment-sicko` is spawned by the `no-comments` skill.

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
- Much of the inherited text assumes Cursor. Examples include the `Task` and `AskQuestion` tool names, `~/.cursor/rules`, the `cursor-team-kit` plugin, Cursor's built-in `create-skill`, and model ids like `grok-4.7-xhigh-fast`. Find them with `rg -n 'cursor|Cursor|AskQuestion|grok'`. Don't treat them as requirements when adapting a skill to another harness.
- When you rename or remove a skill, principle, or playbook, update its entry in `skills/poteto-mode/SKILL.md` and any agent that points at it in the same change.
- Keep `LICENSE` intact. It is MIT and carries both copyright lines.
