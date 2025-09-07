#!/usr/bin/env bash
set -euo pipefail

# Verificar que no hay cambios sin commitear
if ! git diff-index --quiet HEAD --; then
  echo "❌ Error: Hay cambios sin commitear. Commitea primero antes de crear el PR."
  git status --short
  exit 1
fi

# Config
BASE_BRANCH="${BASE_BRANCH:-dev}"
PR_TITLE="${PR_TITLE:-$(git rev-parse --abbrev-ref HEAD)}"   # o usa el último commit: git log -1 --pretty=%s
TEMPLATE_PATH="${TEMPLATE_PATH:-.github/PULL_REQUEST_TEMPLATE.md}"
TMP_BODY="$(mktemp -t pr-body.XXXXXX.md)"

# Sección: diffs & commits
DIFFSTAT=$(git fetch origin "$BASE_BRANCH" >/dev/null 2>&1 || true; git diff --stat origin/"$BASE_BRANCH"...HEAD || git diff --stat "$BASE_BRANCH"...HEAD)
FILES_CHANGED=$(git diff --name-only origin/"$BASE_BRANCH"...HEAD || git diff --name-only "$BASE_BRANCH"...HEAD)
COMMITS=$(git log --pretty='- %h %s (%an)' origin/"$BASE_BRANCH"..HEAD || git log --pretty='- %h %s (%an)' "$BASE_BRANCH"..HEAD)

# Si hay múltiples templates, podés elegir con TEMPLATE_PATH=.github/PULL_REQUEST_TEMPLATE/feature.md
if [[ -f "$TEMPLATE_PATH" ]]; then
  cat "$TEMPLATE_PATH" > "$TMP_BODY"
else
  # fallback minimal si no existe template
  cat > "$TMP_BODY" <<'EOF'
## Summary

<!-- breve descripción -->

## Checklist
- [ ] Tests
- [ ] Docs
- [ ] Backward compatible

## Notes
<!-- riesgos, rollout, etc. -->
EOF
fi

# Inyecta datos dinámicos al final
cat >> "$TMP_BODY" <<EOF

---

## 🧾 Commits incluidos
$COMMITS

## 📊 Diffstat
\`\`\`
$DIFFSTAT
\`\`\`
EOF

# Crear PR (ajustá flags a gusto)
# --draft para borrador, --label para etiquetas, --reviewer para reviewers
gh pr create \
  --base "$BASE_BRANCH" \
  --title "$PR_TITLE" \
  --body-file "$TMP_BODY" \
  --assignee "@me" \
  --draft

echo "PR creado con template + contenido dinámico. Archivo temporal: $TMP_BODY"
