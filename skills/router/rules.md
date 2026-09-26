# Router rules

These rules apply to every router playbook and every subagent it spawns.

Paths are relative to this file's directory. A skill named in bold, here or in any playbook or skill you load, lives at `../<name>/SKILL.md`. Read that file when a step names the skill.

- **Code.** Name the data shape before writing logic. Encode the domain in a structure (a state machine, a typed model, a lookup table, a discriminated union) instead of scattered conditionals, unless the code is already clear and local.
- **Types.** Make illegal states unrepresentable. Model variants as tagged unions, not bags of optional fields. Give primitives that mean different things distinct types. Parse external data into typed values where it enters, and don't cast around the compiler.
- **Size.** Make the smallest change that solves the problem, and delete before you add. Add no compatibility shims. Migrate every caller and delete the old API in the same change.
- **Debugging.** Reproduce first, then fix the root cause. Don't add a guard that silences the symptom.
- **Tests.** A test calls the code the way its users do and asserts a literal expected value. If it would still pass with every imported function returning `undefined`, rewrite the assertion or delete the test.
- **Prose.** Every prose surface follows the **unslop** skill, your reply included. Write it clean as you draft, because a cleanup pass afterward misses the patterns. Docs, RFCs, and readmes also follow the **technical-writing** skill. PR and commit text follows `playbooks/opening-a-pr.md` instead. Agent-facing prose also follows `playbooks/authoring-a-skill.md`.
- **Comments.** Keep a code comment only for a non-obvious why. Test and verify scripts get no step-narrating comments, because the assertion or log string names the step. This holds for every file, delegate diffs included.
- **Verification.** Check the real thing before calling work done. Run it and read the actual value, not a proxy, "it compiles", or a subagent's summary. For UI, IDE, and CLI work, use the project's verification skill (`verify-<app>`). If it has none, drive the surface directly and note the gap.
- **Irreversible writes.** Stop and ask before a force-push to a shared branch, a deploy, data deletion, or a customer message.
- **Broken skills.** Fix a skill that breaks mid-task in its own PR. Don't block on it, and don't silently work around it.
