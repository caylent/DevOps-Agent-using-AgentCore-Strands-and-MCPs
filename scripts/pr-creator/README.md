# PR Creator

Automated Pull Request creation tool.

## Usage

```bash
./scripts/pr-creator/create.sh
```

## Features

- ✅ Validates no uncommitted changes
- 🏷️ Auto-generates title from last commit message
- 📝 Auto-fills description from commit body (if available)
- 📊 Includes commit history and diffstat
- 🚀 Creates draft PR for review

## Configuration

Environment variables:
- `BASE_BRANCH`: Target branch (default: `dev`)
- `PR_TITLE`: Override auto-generated title
- `TEMPLATE_PATH`: Custom template path (default: `.github/PULL_REQUEST_TEMPLATE.md`)

## Requirements

- `gh` CLI tool
- Git repository with remote origin
- Current branch pushed to remote