#!/usr/bin/env bash
set -euo pipefail

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
  echo "❌ Error: GitHub CLI (gh) is not installed."
  echo "Install it from: https://cli.github.com/"
  exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
  echo "❌ Error: GitHub CLI is not authenticated."
  echo "Run: gh auth login"
  exit 1
fi

# Verify no uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo "❌ Error: There are uncommitted changes. Please commit first before creating PR."
  git status --short
  exit 1
fi

# Config
BASE_BRANCH="${BASE_BRANCH:-dev}"
PR_TITLE="${PR_TITLE:-$(git log -1 --pretty=%s)}"
TEMPLATE_PATH="${TEMPLATE_PATH:-.github/PULL_REQUEST_TEMPLATE.md}"
TMP_BODY="$(mktemp -t pr-body.XXXXXX.md)"

# Section: diffs & commits
DIFFSTAT=$(git fetch origin "$BASE_BRANCH" >/dev/null 2>&1 || true; git diff --stat origin/"$BASE_BRANCH"...HEAD || git diff --stat "$BASE_BRANCH"...HEAD)
FILES_CHANGED=$(git diff --name-only origin/"$BASE_BRANCH"...HEAD || git diff --name-only "$BASE_BRANCH"...HEAD)
COMMITS=$(git log --pretty='- %h %s (%an)' origin/"$BASE_BRANCH"..HEAD || git log --pretty='- %h %s (%an)' "$BASE_BRANCH"..HEAD)
LAST_COMMIT_BODY=$(git log -1 --pretty=%b)

# If multiple templates exist, you can choose with TEMPLATE_PATH=.github/PULL_REQUEST_TEMPLATE/feature.md
if [[ -f "$TEMPLATE_PATH" ]]; then
  cat "$TEMPLATE_PATH" > "$TMP_BODY"
  # Auto-complete Summary if last commit has body
  if [[ -n "$LAST_COMMIT_BODY" ]]; then
    # Escape special characters for sed
    ESCAPED_BODY=$(printf '%s\n' "$LAST_COMMIT_BODY" | sed 's/[[\.*^$()+?{|]/\\&/g')
    sed -i "s/<!-- Describe what this PR does and why -->/$ESCAPED_BODY/" "$TMP_BODY"
  fi
else
  # minimal fallback if template doesn't exist
  cat > "$TMP_BODY" <<'EOF'
## Summary

<!-- brief description -->

## Checklist
- [ ] Tests
- [ ] Docs
- [ ] Backward compatible

## Notes
<!-- risks, rollout, etc. -->
EOF
fi

# Inject dynamic data at the end
cat >> "$TMP_BODY" <<EOF

---

## 🧾 Included Commits
$COMMITS

## 📊 Diffstat
\`\`\`
$DIFFSTAT
\`\`\`
EOF

# Create PR (adjust flags as needed)
# --draft for draft mode, --label for tags, --reviewer for reviewers
gh pr create \
  --base "$BASE_BRANCH" \
  --title "$PR_TITLE" \
  --body-file "$TMP_BODY" \
  --assignee "@me" \
  --draft

echo "PR created with template + dynamic content. Temp file: $TMP_BODY"
