#!/usr/bin/env python3
"""PreToolUse hook that holds `gh pr create` and `gh pr edit` to the pr skill's title rules."""

import json
import re
import shlex
import sys

TYPES = ("feat", "fix", "perf", "refactor", "docs", "test", "ci", "chore")
TITLE = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[^()\s]+)\))?!?: (?P<subject>\S.*)$")
OPERATORS = {"&&", "||", ";", "|", "&", "(", ")", "\n"}
EXAMPLE = "fix(server): log the request path instead of the full URI"


def gh_pr_calls(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    tokens = list(lexer)
    calls, current = [], []
    for token in tokens + [";"]:
        if token in OPERATORS:
            if current[:3] in (["gh", "pr", "create"], ["gh", "pr", "edit"]):
                calls.append(current)
            current = []
        else:
            current.append(token)
    return calls


def title_of(args):
    for i, arg in enumerate(args):
        if arg in ("--title", "-t") and i + 1 < len(args):
            return args[i + 1]
        if arg.startswith("--title="):
            return arg.split("=", 1)[1]
    return None


def problem_with(title):
    match = TITLE.match(title)
    if not match:
        return "it is not in the form `type(scope): subject`"
    if match["type"] not in TYPES:
        return f"`{match['type']}` is not one of {', '.join(TYPES)}"
    subject = match["subject"]
    if subject.endswith("."):
        return "the subject ends with a period"
    first = subject.split()[0]
    if first[0].isupper() and first[1:] == first[1:].lower() and not re.search(r"[_.(]", first):
        return f"the subject starts with a capital (`{first}`), and only code symbols keep their case"
    return None


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


def main():
    try:
        command = json.load(sys.stdin)["tool_input"]["command"]
        calls = gh_pr_calls(command)
    except (ValueError, KeyError, TypeError):
        return

    for args in calls:
        if args[2] == "create" and any(a == "--draft" or a.startswith("--draft=") for a in args):
            deny("Open the PR ready for review. Drop `--draft` and run the command again.")
            return
        title = title_of(args)
        if title is None:
            continue
        problem = problem_with(title)
        if problem:
            deny(
                f"The PR title `{title}` breaks the pr skill's rules because {problem}. "
                f"Rewrite it as `type(scope): subject` with a lower-case imperative subject and no trailing period, "
                f"for example `{EXAMPLE}`. If this repo uses a different convention, ask the user how to proceed."
            )
            return


if __name__ == "__main__":
    main()
