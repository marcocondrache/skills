### Opening a PR

Invoked at the end of every other playbook.

**Worktree.** Work from a git worktree off main. Subagents inherit it. Multiple subagents on the same branch each get their own worktree, or `git fetch && git reset --hard origin/<branch>` between them. Dirty branch with unrelated work: patch out, fresh worktree, apply. Snarled worktree: reset from main, redo minimally.

**Commits.** Commit liberally. Rebase into small, ordered commits before opening PRs. Each commit is a future PR: landable, ordered to tell the story. Amend when the fix belongs in a just-made commit. New commit when separable.

**PRs.** Before commit, re-read the diff and strip slop per the **unslop** skill (prose) and the **no-comments** skill (comments). Run `/no-comments` before review. Write every PR title, PR description, and commit body per the **unslop** skill and the rules below. Skip the **technical-writing** skill for them. Write the real symbol, file, flag, or command name instead of a description of it. Use one word for each action, keep articles, and avoid `-ing` when a plain verb works.

**Titles.** Use Conventional Commits in the form `type(scope): subject`. Use `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf` as the type. Use the changed area, such as `router` or `unslop`, as the scope. Keep the subject short and imperative. Name a real symbol when one carries the change. For example, `fix(router): link playbooks by relative path`. Do not add a trailing period.

**Descriptions.** Write the PR body as plain prose, the way you would explain the change to a colleague. Use one to three sentences that say why the change exists. Add a sentence on a decision only when a reviewer would otherwise ask about it. Do not use headings, bullets, bold, tables, or checklists. Do not restate the diff, list files or SHAs, or paste verification logs. The squash commit body is the PR body, and a commit body does not restate its subject.

**Forge.** Use GitHub CLI (`gh`) for create, edit, view, watch, and merge. Do not require Graphite (`gt`).

**Size and stacks.** Prefer five narrow PRs to one large PR. A stack is a base-branch chain. The root PR targets trunk. Each child branch rebases onto its parent's exact tip and its PR targets the parent branch. Create a child with `gh pr create --base <parent-branch>`. Retarget an existing child with `gh pr edit <pr> --base <parent-branch>`. Branch from trunk only for independent work. Rebase on trunk before substantial stack work.

**Readiness.** Open every PR ready, never as a draft. With `gh`, omit `--draft`. Some harness PR tools default to draft, so set `draft: false` on every PR creation call. If a PR still opens as a draft, run `gh pr ready <number>`. Run `gh pr view <number>` before you refer to PR status.

**After opening.** Post the URL and keep building. Opening a PR does not start watching it. Push back when review feedback drifts from intent.

A subagent that opens a PR strips slop from the diff, runs `/no-comments`, posts the URL, and returns to the parent.
