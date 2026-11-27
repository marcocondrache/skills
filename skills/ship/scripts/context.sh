#!/usr/bin/env bash
# Always exits 0: a failed injected command aborts the whole skill.

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not a git repository."
  exit 0
fi

base=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
base=${base:-origin/main}
git rev-parse --verify --quiet "$base" >/dev/null || base=main

echo "Branch: $(git branch --show-current 2>/dev/null)"
echo "Base: $base"

echo
echo "Working tree:"
git status --short 2>/dev/null | head -n 40

echo
echo "Commits on this branch:"
git log --oneline --no-decorate "$base..HEAD" 2>/dev/null | head -n 30

echo
echo "Diff stat against $base:"
git diff --stat=100 --stat-count=40 "$base...HEAD" 2>/dev/null

echo
echo "Recent titles on $base:"
git log --format=%s -n 8 "$base" 2>/dev/null

echo
echo "Open PR for this branch:"
if command -v gh >/dev/null 2>&1; then
  gh pr view --json number,title,url,baseRefName,isDraft,state \
    --template '#{{.number}} {{.title}} ({{.state}}, base {{.baseRefName}}{{if .isDraft}}, draft{{end}}) {{.url}}{{"\n"}}' 2>/dev/null \
    || echo "none"
else
  echo "unknown, gh is not installed"
fi

echo
echo "Repo conventions:"
found=0
for f in CONTRIBUTING.md .github/CONTRIBUTING.md docs/CONTRIBUTING.md \
  .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md \
  pull_request_template.md docs/pull_request_template.md; do
  if [ -f "$f" ]; then echo "$f"; found=1; fi
done
if [ -d .github/PULL_REQUEST_TEMPLATE ]; then echo ".github/PULL_REQUEST_TEMPLATE/"; found=1; fi
[ "$found" = 1 ] || echo "none found"
exit 0
