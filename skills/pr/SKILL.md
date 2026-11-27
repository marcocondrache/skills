---
name: pr
description: "Use when opening, editing, or stacking a pull request or writing a commit message, as in 'open a PR', 'write the PR description', 'stack these PRs', 'rebase the stack', /pr, or during /ship. Sets the commit, title, and body conventions and opens the PR with gh."
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/context.sh) Bash(git status *) Bash(git log *) Bash(git diff *) Bash(git show *) Bash(gh pr view *) Bash(gh pr list *)
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          if: Bash(gh pr create *)
          command: python3 "${CLAUDE_PLUGIN_ROOT}/skills/pr/scripts/check-pr.py"
        - type: command
          if: Bash(gh pr edit *)
          command: python3 "${CLAUDE_PLUGIN_ROOT}/skills/pr/scripts/check-pr.py"
---

# PR

## Current state

!`${CLAUDE_SKILL_DIR}/scripts/context.sh`

When the repo lists a contributing guide or PR template above, read it. Its conventions win over this skill. The recent titles on the base branch show the convention in practice.

## Before opening

Read the full diff with `git diff <base>...HEAD`. Delete comments that narrate what the code does and keep only a comment that explains a non-obvious why. Apply the `unslop` skill to any prose the diff adds.

Rebase into small, ordered commits. Each commit lands on its own and the order tells the story. Amend when a fix belongs in the commit just made, and add a new commit when the fix is separable. After you rewrite a branch that is already pushed, push it with `git push --force-with-lease`, never `--force`.

## Size and stacks

Prefer several narrow PRs to one large PR. A stack is a chain of base branches. The root PR targets the default branch. Each child branch rebases onto its parent's exact tip and its PR targets the parent branch, via `gh pr create --base <parent-branch>` or `gh pr edit <pr> --base <parent-branch>`. Branch from the default branch only for independent work.

## Title

Use `type(scope): subject`. The squash commit takes this title, and a changelog tool such as release-please may publish it, so write it for a reader of the release notes. In a release-please repo only `feat`, `fix`, `perf`, and breaking changes cut a release and appear in the changelog.

- Type is one of `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `ci`, or `chore`.
- Scope is the changed area, such as a package, module, or service. Omit it when the change spans the project.
- Write the whole title in lower case, including the first word of the subject. Keep a code symbol in its original case.
- Subject uses the imperative and has no trailing period.
- Name the behavior that changes, or the real symbol that carries it. `fix(server): log the request path instead of the full URI`, not `fix(server): fix logging issue`.

While this skill is loaded, a hook blocks `gh pr create` and `gh pr edit` when the title breaks these rules, and blocks `gh pr create --draft`. Fix the title and run the command again.

## Body

Write the body as plain prose, the way you would explain the change to a colleague. The squash commit body is the PR body.

- Open with one to three sentences on why the change exists and what changes for the user or the next maintainer.
- Add a sentence on a decision only when a reviewer would otherwise ask about it.
- State a breaking change in its own sentence that starts with `Breaking:` and names every config key, flag, or API it affects.
- Do not use headings, bold, tables, or checklists. If the repo has a PR template, fill it in and keep the prose inside each section to these rules.
- Do not restate the diff, list files or SHAs, restate the title, or paste verification logs.

Write per `unslop`. Use short declarative sentences, one word for each action, and a plain verb over an `-ing` form.

## Opening

Use `gh` to create, edit, view, and merge. Open every PR ready for review, never as a draft. Run `gh pr view <number>` before you state a PR's status.

Post the URL as `https://github.com/<owner>/<repo>/pull/<number>`. Opening a PR does not start a watch on it, unless the user ran `/ship`, which watches the PR itself. Otherwise continue with the remaining work, and check CI and review threads only when asked.
