---
name: why
description: "Use for 'why does X work this way', 'why did we pick Y', 'is it safe to change this', or the design rationale behind code. Reads git history, PRs, and written docs, then returns a cited answer that keeps what the record says apart from what you infer. Use how for runtime behavior."
disable-model-invocation: true
---

# Why

Find the reasons behind the code's current shape. The **how** skill covers what the code does. This skill covers why it is that way.

Code is not evidence of its own intent. The reasons live in what people wrote down, such as commit messages, PR bodies and reviews, docs, comments, and tests. When none of it says why, the answer is "we don't know", and that tells the user to ask the author before acting on a guess.

## Steps

1. Pin the target and the question. If the target is vague, state your best guess from the conversation and go on. If the question carries its own guess ("I assume it's for perf"), treat it as one candidate and check it like any other.
2. Anchor it in code. Name the files, the line range, and the key symbols.
3. Read the git record.
   - `git blame -L <start>,<end> <file>` finds the commits that last touched each line.
   - `git log --follow --oneline -- <file>` lists the history through renames.
   - `git log -S '<exact string>' -- <file>` finds the commits that added or removed a string.
   - `git show <hash>` shows the whole change.
   - `gh pr view <number> --json title,body,comments,reviews,closingIssuesReferences` reads the PR behind a commit. The number is usually in the commit subject as `(#123)`.

   Review threads often hold more of the reasoning than commit messages. In a squash-merged repo, the PR body is the record. Skip bot commits. The latest commit is rarely the whole story, so follow the history back to where the shape first appeared, and trace a copied pattern to its first use.
4. Read the docs. Search the repo's written record for the feature name and the key symbols. That means READMEs, `docs/`, ADRs, RFCs, the CHANGELOG, and tests whose names state an edge case. Search a connected docs tool too, if the session has one. For defensive code (a retry, a timeout, a null guard, a flag), look for the incident behind it. Docs are often written before the code and never updated, so check each one against the PR that shipped the code.
5. Write the answer in the format below.

When the history is long, give steps 3 and 4 to one subagent on a fast model. It returns the evidence as quotes with citations, not raw logs.

## Answer format

- **Found.** What an author wrote about why, each with its citation (commit, PR, doc, or `file:line`) and a short quote. Only these claims say "because".
- **Inferred.** Readings the record supports but never states. Hedge each one ("likely", "suggests") and give the evidence behind it. When several readings fit, list each with what supports it and what undercuts it.
- **Unknown.** What you couldn't find, and exactly where you looked. Name the commits, PRs, and docs you read and the terms you searched.

When two sources disagree, show both instead of picking the tidier one. Missing evidence is not evidence, so "nobody mentioned security" does not mean security wasn't a concern.

When the question comes before a change, end with what the change must preserve, what it can safely change, and what it risks.
