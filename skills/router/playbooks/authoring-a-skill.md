### Authoring or modifying a skill

**You own the skill's voice.** A skill is a directory whose `SKILL.md` an agent loads when the task matches its description. The directory name is the skill's id. A project skill lives in the project's skills directory, a personal one in the user's personal skills directory.

1. Name the trigger. Write three to five requests a user would type that should load the skill, and one or two near-misses that should not. If you can't list them, the skill has no clear job yet.
2. Write the frontmatter. `name` matches the directory name. `description` is the trigger, because the agent sees only the description when it decides whether to load the skill. Say when to use the skill, with the phrases from step 1, not what the skill contains. Keep `disable-model-invocation: true` unless the skill should load on its own. Add `paths` globs (`paths: ["**/*.ts", "**/*.tsx"]`) for a skill tied to a file type. Add no other keys unless the target harness documents them.
3. Draft the body. Keep `SKILL.md` to what every invocation needs. Move material loaded on demand into `references/` (prompts, templates, rubrics), step lists a skill routes to into `playbooks/`, and executable tools into `scripts/`. Link each from `SKILL.md` by relative path. Write the prose per the **unslop** skill.
4. Validate. Frontmatter has `name` and `description`, referenced files exist, and cross-skill links resolve. On a rename, find every citation of the old id with `rg -n '<old-name>'` and update it in the same change.
5. Test if the skill is structural, meaning it should change what an agent does. Give each step-1 request to a fresh agent with the skill installed and read what it did. The skill must load on the triggers and stay out on the near-misses, and the output must follow it. To compare against the current version, give the same requests to an agent with the old version and compare the two. Skip testing for a subjective skill and say so.
6. Iterate. A load that misfires means the description is wrong. Behavior that misses means the body is wrong. Fix one, re-run step 5, and stop when every trigger and near-miss passes.
7. Run **Opening a PR**.

When in doubt, delete. Keep only prose that changes a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) per the **encode-lessons-in-structure** principle skill. Delegate to other skills by name or path. Don't restate them. When you keep hitting a workflow that no skill captures, propose a new skill.

**Reply:** summary of the skill, key design decisions, the trigger and near-miss results, validation notes.
