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

# AI Configuration
USE_AI="${USE_AI:-true}"
AI_MODEL="${AI_MODEL:-anthropic.claude-3-sonnet-20240229-v1:0}"
AI_MAX_TOKENS="${AI_MAX_TOKENS:-1000}"

# Section: diffs & commits
DIFFSTAT=$(git fetch origin "$BASE_BRANCH" >/dev/null 2>&1 || true; git diff --stat origin/"$BASE_BRANCH"...HEAD || git diff --stat "$BASE_BRANCH"...HEAD)
FILES_CHANGED=$(git diff --name-only origin/"$BASE_BRANCH"...HEAD || git diff --name-only "$BASE_BRANCH"...HEAD)
COMMITS=$(git log --pretty='- %h %s (%an)' origin/"$BASE_BRANCH"..HEAD || git log --pretty='- %h %s (%an)' "$BASE_BRANCH"..HEAD)
LAST_COMMIT_BODY=$(git log -1 --pretty=%b)
DIFF_CONTENT=$(git diff origin/"$BASE_BRANCH"...HEAD || git diff "$BASE_BRANCH"...HEAD)

# Function to generate AI description using Bedrock
generate_ai_description() {
  local diff_content="$1"
  local commits="$2"
  local files_changed="$3"
  
  # Skip AI if disabled
  if [[ "$USE_AI" != "true" ]]; then
    echo "<!-- AI description disabled -->"
    return 1
  fi
  
  # Check dependencies
  if ! command -v aws &> /dev/null; then
    echo "⚠️  AWS CLI no está instalado, saltando generación de IA"
    echo "<!-- AI description generation failed, using fallback -->"
    return 1
  fi
  
  if ! command -v jq &> /dev/null; then
    echo "⚠️  jq no está instalado, saltando generación de IA"
    echo "<!-- AI description generation failed, using fallback -->"
    return 1
  fi
  
  if ! aws sts get-caller-identity &> /dev/null; then
    echo "⚠️  AWS no está autenticado, saltando generación de IA"
    echo "<!-- AI description generation failed, using fallback -->"
    return 1
  fi
  
  # Limit diff size to prevent JSON issues
  if [[ ${#diff_content} -gt 10000 ]]; then
    echo "⚠️  Diff muy largo (${#diff_content} chars), usando resumen"
    diff_content=$(echo "$diff_content" | head -100)
    diff_content="$diff_content

[... diff truncado por tamaño ...]"
  fi

  # Create prompt for Bedrock
  local prompt="Analyze the following git changes and generate a concise, professional pull request description in Spanish.

Files changed:
$files_changed

Commits:
$commits

Code changes:
$diff_content

Please provide:
1. A brief summary of what this PR does
2. Key changes made
3. Any potential impact or considerations

Keep the response concise and professional, suitable for a pull request description."

  # Escape JSON special characters in prompt (simplified)
  local escaped_prompt
  escaped_prompt=$(echo "$prompt" | sed 's/"/\\"/g' | tr '\n' ' ' | sed 's/  */ /g')
  
  # Create JSON payload
  local json_payload="{
    \"anthropic_version\": \"bedrock-2023-05-31\",
    \"max_tokens\": $AI_MAX_TOKENS,
    \"messages\": [
      {
        \"role\": \"user\",
        \"content\": \"$escaped_prompt\"
      }
    ]
  }"

  # Call Bedrock API with timeout
  echo "🤖 Generando descripción inteligente con Bedrock ($AI_MODEL)..."
  local ai_response
  local temp_response="/tmp/bedrock-response-$$.json"
  
  # Use timeout to prevent hanging
  if timeout 30s aws bedrock-runtime invoke-model \
    --model-id "$AI_MODEL" \
    --body "$json_payload" \
    --cli-binary-format raw-in-base64-out \
    "$temp_response" 2>/dev/null; then
    
    if [[ -f "$temp_response" ]]; then
      ai_response=$(cat "$temp_response" | jq -r '.content[0].text' 2>/dev/null)
      rm -f "$temp_response"
      
      if [[ -n "$ai_response" && "$ai_response" != "null" ]]; then
        echo "$ai_response"
        return 0
      fi
    fi
  fi
  
  # Fallback if Bedrock fails
  echo "⚠️  Error generando descripción con IA, usando fallback"
  echo "<!-- AI description generation failed, using fallback -->"
  return 1
}

# Generate AI description
echo "🧠 Analizando cambios para generar descripción inteligente..."
echo "Debug: Diff size: ${#DIFF_CONTENT} chars, Files: $(echo "$FILES_CHANGED" | wc -l) files"

if [[ "$USE_AI" == "true" ]]; then
  if AI_DESCRIPTION=$(generate_ai_description "$DIFF_CONTENT" "$COMMITS" "$FILES_CHANGED"); then
    echo "✅ IA description generada exitosamente"
  else
    echo "⚠️  IA falló, continuando con fallback"
    AI_DESCRIPTION="<!-- AI description generation failed, using fallback -->"
  fi
else
  echo "ℹ️  IA deshabilitada, usando fallbacks"
  AI_DESCRIPTION="<!-- AI description generation disabled -->"
fi

# If multiple templates exist, you can choose with TEMPLATE_PATH=.github/PULL_REQUEST_TEMPLATE/feature.md
if [[ -f "$TEMPLATE_PATH" ]]; then
  cat "$TEMPLATE_PATH" > "$TMP_BODY"
  
  # Use AI description if available, otherwise use last commit body
  if [[ "$AI_DESCRIPTION" != "<!-- AI description generation failed, using fallback -->" && "$AI_DESCRIPTION" != "<!-- AI description generation disabled -->" ]]; then
    # Use a temp file to avoid sed escaping issues
    echo "$AI_DESCRIPTION" > /tmp/ai_desc.txt
    sed -i '/<!-- Describe what this PR does and why -->/r /tmp/ai_desc.txt' "$TMP_BODY"
    sed -i '/<!-- Describe what this PR does and why -->/d' "$TMP_BODY"
    rm -f /tmp/ai_desc.txt
    echo "✅ Descripción inteligente generada con éxito"
  elif [[ -n "$LAST_COMMIT_BODY" ]]; then
    # Fallback to last commit body
    echo "$LAST_COMMIT_BODY" > /tmp/commit_body.txt
    sed -i '/<!-- Describe what this PR does and why -->/r /tmp/commit_body.txt' "$TMP_BODY"
    sed -i '/<!-- Describe what this PR does and why -->/d' "$TMP_BODY"
    rm -f /tmp/commit_body.txt
    echo "⚠️  Usando descripción del último commit como fallback"
  else
    echo "⚠️  No se pudo generar descripción automática"
  fi
else
  # minimal fallback if template doesn't exist
  if [[ "$AI_DESCRIPTION" != "<!-- AI description generation failed, using fallback -->" && "$AI_DESCRIPTION" != "<!-- AI description generation disabled -->" ]]; then
    cat > "$TMP_BODY" <<EOF
## Summary

$AI_DESCRIPTION

## Checklist
- [ ] Tests
- [ ] Docs
- [ ] Backward compatible

## Notes
<!-- risks, rollout, etc. -->
EOF
    echo "✅ Usando descripción inteligente en template por defecto"
  else
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
    echo "⚠️  Usando template por defecto sin descripción automática"
  fi
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

echo "🎉 PR created with AI-generated description + dynamic content. Temp file: $TMP_BODY"
