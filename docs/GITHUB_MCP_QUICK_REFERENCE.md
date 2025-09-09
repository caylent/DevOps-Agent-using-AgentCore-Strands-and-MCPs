# 🐙 GitHub MCP Quick Reference

## Essential Commands

### Setup & Installation
```bash
# Install all MCP servers (including GitHub)
make mcp-install

# Check MCP server status
make mcp-check

# Test GitHub connectivity
make github-test-connectivity REPO=owner/repo
```

### Configuration
```bash
# Add GitHub token to config
echo "GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here" >> src/aws_devops_agent/config/.env

# Test configuration
make mcp-test
```

### Agent Usage
```bash
# Start agent with GitHub integration
make run

# Example queries in the agent:
# "List all repositories in my organization"
# "Create a new branch for infrastructure changes"
# "Analyze the structure of my Terraform repository"
# "Create a pull request for cost optimization changes"
```

## GitHub Tools Available

| Tool | Description | Usage |
|------|-------------|-------|
| `check_repository_connectivity` | Test connection to repository | `make github-test-connectivity REPO=owner/repo` |
| `get_repository_info` | Get repository details | Available in agent |
| `list_repository_branches` | List all branches | Available in agent |
| `create_branch_simple` | Create new branch | Available in agent |

## Environment Variables

```bash
# Required
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
GITHUB_ORG=your-organization
GITHUB_DEFAULT_REPO=your-org/your-repo
```

## Troubleshooting

### Common Issues
```bash
# Token not found
echo "GITHUB_PERSONAL_ACCESS_TOKEN=your_token" >> src/aws_devops_agent/config/.env

# MCP server not starting
make mcp-install

# Connection failed
make github-test-connectivity REPO=octocat/Hello-World
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
make run
```

## GitHub Token Scopes Required

- `repo` - Full control of private repositories
- `read:org` - Read org and team membership
- `read:user` - Read user profile data
- `project` - Read/write project boards

## Quick Test

```bash
# 1. Install MCP servers
make mcp-install

# 2. Add GitHub token
echo "GITHUB_PERSONAL_ACCESS_TOKEN=your_token" >> src/aws_devops_agent/config/.env

# 3. Test connectivity
make github-test-connectivity REPO=octocat/Hello-World

# 4. Start agent
make run
```

## Integration Examples

### Cost Optimization + GitHub
```bash
make query QUERY="Analyze my AWS costs and create a GitHub pull request with optimization recommendations"
```

### Security Analysis + GitHub
```bash
make query QUERY="Scan my infrastructure for security issues and create GitHub issues for critical findings"
```

### Infrastructure Analysis + GitHub
```bash
make query QUERY="Analyze my Terraform configuration and create a GitHub pull request with improvements"
```

---

**💡 Tip**: Start with `make github-test-connectivity REPO=octocat/Hello-World` to verify everything is working!
