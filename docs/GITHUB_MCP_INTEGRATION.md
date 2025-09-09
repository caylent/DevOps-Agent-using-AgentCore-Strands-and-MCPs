# 🐙 GitHub MCP Integration

## Overview

The AWS DevOps Agent includes comprehensive GitHub integration through the official GitHub MCP (Model Context Protocol) server. This enables the agent to interact with GitHub repositories, create pull requests, manage issues, and automate infrastructure changes directly through GitHub.

## Features

- **Repository Management**: Browse, analyze, and manage GitHub repositories
- **Pull Request Automation**: Create and manage pull requests for infrastructure changes
- **Issue Tracking**: Create, update, and manage GitHub issues
- **Branch Operations**: Create branches, manage merges, and handle conflicts
- **Code Analysis**: Analyze repository structure, dependencies, and code quality
- **CI/CD Integration**: Trigger workflows and monitor build statuses

## Prerequisites

### 1. GitHub Personal Access Token

You need a GitHub Personal Access Token with the following scopes:

- `repo` - Full control of private repositories
- `read:org` - Read org and team membership  
- `read:user` - Read user profile data
- `project` - Read/write project boards

**Generate Token:**
1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/personal-access-tokens/new)
2. Click "Generate new token (classic)"
3. Select the required scopes
4. Copy the generated token

### 2. Go Installation

The GitHub MCP server is built from source and requires Go:

```bash
# Install Go (if not already installed)
# macOS
brew install go

# Ubuntu/Debian
sudo apt update
sudo apt install golang-go

# Verify installation
go version
```

## Configuration

### 1. Environment Variables

Add these variables to your `.env` file:

```bash
# Required
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional
GITHUB_ORG=your-organization
GITHUB_DEFAULT_REPO=your-org/your-repo
```

### 2. Configuration File Location

The agent looks for GitHub configuration in:
- `src/aws_devops_agent/config/.env` (primary)
- Environment variables (fallback)

### 3. Verify Configuration

```bash
# Check GitHub MCP status
make mcp-check

# Test GitHub connectivity
make github-test-connectivity REPO=octocat/Hello-World
```

## Installation

### Automatic Installation

The GitHub MCP server is automatically installed when you run:

```bash
# Install all MCP servers (including GitHub)
make mcp-install
```

### Manual Installation

If you need to install manually:

```bash
# Clone the GitHub MCP server repository
git clone https://github.com/github/github-mcp-server.git

# Build the server
cd github-mcp-server
go build -o github-mcp-server

# Make it executable
chmod +x github-mcp-server
```

## Usage

### 1. Basic Repository Operations

```bash
# Test connectivity to a repository
make github-test-connectivity REPO=owner/repo

# List repository information
python -c "
from aws_devops_agent.tools.github.integration import get_repository_info
result = get_repository_info('octocat/Hello-World')
print(result)
"
```

### 2. Interactive Agent Usage

Start the agent and use GitHub commands:

```bash
# Start the agent
make run

# Example commands in the agent:
# "List all repositories in my organization"
# "Create a new branch for infrastructure changes"
# "Analyze the structure of my Terraform repository"
# "Create a pull request for cost optimization changes"
```

### 3. Available GitHub Tools

The agent provides these GitHub tools:

- `check_repository_connectivity` - Test connection to a repository
- `get_repository_info` - Get detailed repository information
- `list_repository_branches` - List all branches in a repository
- `create_branch_simple` - Create a new branch

### 4. MCP Server Management

```bash
# Check MCP server status
make mcp-check

# Test all MCP servers
make mcp-test

# Start MCP servers
make mcp-run

# Stop MCP servers
make mcp-stop
```

## GitHub Integration Examples

### 1. Infrastructure as Code Analysis

```bash
# Analyze a Terraform repository
make query QUERY="Analyze the Terraform configuration in my infrastructure repository and suggest cost optimizations"
```

### 2. Automated Pull Request Creation

```bash
# Create a pull request for infrastructure changes
make query QUERY="Create a pull request with the cost optimization changes for my EC2 instances"
```

### 3. Repository Health Check

```bash
# Check repository health and compliance
make query QUERY="Analyze my infrastructure repository for security issues and compliance violations"
```

### 4. Multi-Repository Operations

```bash
# Work with multiple repositories
make query QUERY="Compare the infrastructure configurations across my staging and production repositories"
```

## Advanced Configuration

### 1. Custom GitHub MCP Server

If you need to use a custom GitHub MCP server:

```bash
# Set custom server path
export GITHUB_MCP_SERVER_PATH=/path/to/custom/github-mcp-server

# Or modify the Makefile to use your custom server
```

### 2. Multiple GitHub Organizations

To work with multiple GitHub organizations:

```bash
# Use different tokens for different operations
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_main_token
export GITHUB_ORG=main-organization

# Or switch tokens dynamically in the agent
```

### 3. Private Repository Access

For private repositories, ensure your token has the `repo` scope:

```bash
# Test private repository access
make github-test-connectivity REPO=your-org/private-repo
```

## Troubleshooting

### Common Issues

#### 1. GitHub Token Not Found

```bash
# Error: GitHub token not found
# Solution: Add token to config file
echo "GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here" >> src/aws_devops_agent/config/.env
```

#### 2. MCP Server Not Starting

```bash
# Error: GitHub MCP server not starting
# Solution: Check Go installation and build
go version
cd github-mcp-server && go build -o github-mcp-server
```

#### 3. Repository Access Denied

```bash
# Error: Repository access denied
# Solution: Check token scopes and repository permissions
# Ensure token has 'repo' scope for private repositories
```

#### 4. Connection Timeout

```bash
# Error: Connection timeout
# Solution: Check network connectivity and GitHub API status
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set debug mode
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG

# Run with debug output
make run
```

### Log Files

Check log files for detailed error information:

```bash
# Check agent logs
tail -f logs/aws_devops_agent.log

# Check MCP server logs
tail -f logs/mcp_server.log
```

## Security Considerations

### 1. Token Security

- **Never commit tokens** to version control
- **Use environment variables** or secure config files
- **Rotate tokens regularly**
- **Use minimal required scopes**

### 2. Repository Permissions

- **Limit token access** to necessary repositories
- **Use organization-level tokens** when possible
- **Review token usage** regularly

### 3. Network Security

- **Use HTTPS** for all GitHub API calls
- **Validate SSL certificates**
- **Consider VPN** for sensitive operations

## Best Practices

### 1. Repository Organization

```bash
# Use consistent naming conventions
infrastructure-terraform/
infrastructure-cloudformation/
infrastructure-cdk/

# Organize by environment
environments/
├── dev/
├── staging/
└── prod/
```

### 2. Pull Request Workflow

```bash
# Create feature branches for changes
# Use descriptive commit messages
# Include cost impact analysis
# Add security review requirements
```

### 3. Automation Scripts

```bash
# Create reusable automation scripts
scripts/
├── cost-optimization-pr.sh
├── security-compliance-check.sh
└── infrastructure-analysis.sh
```

## Integration with AWS DevOps Tools

The GitHub MCP integration works seamlessly with other AWS DevOps tools:

### 1. Cost Optimization + GitHub

```bash
# Analyze costs and create GitHub PR
make query QUERY="Analyze my AWS costs and create a pull request with optimization recommendations"
```

### 2. Security Analysis + GitHub

```bash
# Security scan and GitHub issue creation
make query QUERY="Scan my infrastructure for security issues and create GitHub issues for critical findings"
```

### 3. Infrastructure Analysis + GitHub

```bash
# Terraform analysis and GitHub automation
make query QUERY="Analyze my Terraform configuration and create a pull request with improvements"
```

## Monitoring and Maintenance

### 1. Health Checks

```bash
# Regular health checks
make mcp-check
make github-test-connectivity REPO=your-org/your-repo
```

### 2. Token Rotation

```bash
# Update token in config
echo "GITHUB_PERSONAL_ACCESS_TOKEN=new_token_here" > src/aws_devops_agent/config/.env

# Restart MCP servers
make mcp-stop
make mcp-run
```

### 3. Performance Monitoring

```bash
# Monitor MCP server performance
make mcp-test

# Check GitHub API rate limits
curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/rate_limit
```

## Support and Resources

### 1. Documentation

- [GitHub MCP Server Repository](https://github.com/github/github-mcp-server)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

### 2. Community

- [GitHub Discussions](https://github.com/github/github-mcp-server/discussions)
- [AWS DevOps Agent Issues](https://github.com/your-org/aws-devops-agent/issues)

### 3. Professional Support

For enterprise support and custom integrations, contact your AWS DevOps team.

---

**💡 Tip**: Start with the basic connectivity test (`make github-test-connectivity`) before using advanced features!
