# 🌍 Environment Variables Configuration

## Overview

The AWS DevOps Agent uses environment variables for configuration, making it easy to deploy across different environments (development, staging, production) without code changes.

## Quick Start with .env Files

### 1. Create Environment File

```bash
# Create development environment
make agentcore-env-dev

# Or create production environment
make agentcore-env-prod

# Or create staging environment
make agentcore-env-staging

# Validate configuration
make agentcore-validate
```

### 2. Customize Configuration

Edit the generated `.env` file in `deployment/bedrock/`:

```bash
# Edit the .env file
nano deployment/bedrock/.env
```

### 3. Run the Agent

```bash
# Test locally
make agentcore-test-local

# Deploy to production
make agentcore-deploy
```

## Manual Environment Variable Setup

If you prefer to set environment variables manually instead of using .env files:

## Required Environment Variables

### AWS Configuration
```bash
# AWS Region (required)
export AWS_REGION=us-east-1

# AWS Profile (optional, defaults to 'default')
export AWS_PROFILE=production

# Bedrock Region (optional, defaults to AWS_REGION)
export BEDROCK_REGION=us-east-1
```

### Agent Configuration
```bash
# Model ID (required)
export BEDROCK_MODEL_ID=claude-3.5-sonnet
# or use specific model ID
export BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0

# Alternative: Use STRANDS_MODEL (fallback)
export STRANDS_MODEL=claude-3.5-sonnet
```

### Server Configuration
```bash
# Server Port (optional, defaults to 8080)
export PORT=8080

# Server Host (optional, defaults to 0.0.0.0)
export HOST=0.0.0.0

# Debug Mode (optional, defaults to false)
export DEBUG_MODE=false
```

## Optional Environment Variables

### Logging Configuration
```bash
# Log Level (optional, defaults to INFO)
export LOG_LEVEL=INFO

# Debug Mode (optional, defaults to false)
export DEBUG_MODE=true
```

### Multi-Account Configuration
```bash
# Cross-Account Roles (optional)
export CROSS_ACCOUNT_ROLES=account1:role1,account2:role2

# AWS Account Configuration (optional - will be detected interactively if not set)
export AWS_ACCOUNT_ID=123456789012
export AWS_ACCOUNT_NAME=My Production Account
export AWS_ROLE_ARN=arn:aws:iam::123456789012:role/DevOpsRole
```

### MCP Server Configuration
```bash
# MCP Timeout (optional, defaults to 30)
export MCP_TIMEOUT=30

# MCP Max Workers (optional, defaults to 10)
export MCP_MAX_WORKERS=10
```

### GitHub MCP Configuration
```bash
# GitHub Personal Access Token (required for GitHub MCP)
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub Organization (optional)
export GITHUB_ORG=your-organization

# GitHub Default Repository (optional)
export GITHUB_DEFAULT_REPO=your-org/your-repo
```

**GitHub Token Setup:**
1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/personal-access-tokens/new)
2. Generate a new token with these scopes:
   - `repo` - Full control of private repositories
   - `read:org` - Read org and team membership
   - `read:user` - Read user profile data
   - `project` - Read/write project boards
3. Copy the token and add it to your `.env` file

## Environment-Specific Configurations

### Development Environment
```bash
# .env.development
AWS_REGION=us-east-1
AWS_PROFILE=dev
BEDROCK_MODEL_ID=claude-3.5-sonnet
PORT=8080
HOST=localhost
DEBUG_MODE=true
LOG_LEVEL=DEBUG
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_dev_token_here
GITHUB_ORG=dev-organization
```

### Staging Environment
```bash
# .env.staging
AWS_REGION=us-east-1
AWS_PROFILE=staging
BEDROCK_MODEL_ID=claude-3.5-sonnet
PORT=8080
HOST=0.0.0.0
DEBUG_MODE=false
LOG_LEVEL=INFO
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_staging_token_here
GITHUB_ORG=staging-organization
```

### Production Environment
```bash
# .env.production
AWS_REGION=us-east-1
AWS_PROFILE=production
BEDROCK_MODEL_ID=claude-3.5-sonnet
PORT=8080
HOST=0.0.0.0
DEBUG_MODE=false
LOG_LEVEL=WARNING
CROSS_ACCOUNT_ROLES=prod-account1:DevOpsRole,prod-account2:DevOpsRole
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_prod_token_here
GITHUB_ORG=production-organization
GITHUB_DEFAULT_REPO=prod-org/infrastructure
```

## Model ID Mapping

The agent supports both model names and full model IDs:

### Supported Model Names
- `claude-4` → `us.anthropic.claude-sonnet-4-20250514-v1:0`
- `claude-3.5-sonnet` → `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- `nova-micro` → `us.amazon.nova-micro-v1:0`
- `nova-lite` → `us.amazon.nova-lite-v1:0`

### Using Full Model IDs
```bash
# Use full model ID directly
export BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0
```

## Docker Environment Variables

When running in Docker, you can pass environment variables:

```bash
# Run with environment variables
docker run -e AWS_REGION=us-east-1 \
           -e BEDROCK_MODEL_ID=claude-3.5-sonnet \
           -e PORT=8080 \
           -e DEBUG_MODE=false \
           aws-devops-agent

# Or use .env file
docker run --env-file .env.production aws-devops-agent
```

## Kubernetes Environment Variables

For Kubernetes deployments, use ConfigMaps and Secrets:

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-devops-agent-config
data:
  AWS_REGION: "us-east-1"
  BEDROCK_MODEL_ID: "claude-3.5-sonnet"
  PORT: "8080"
  HOST: "0.0.0.0"
  DEBUG_MODE: "false"
  LOG_LEVEL: "INFO"

---
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: aws-devops-agent-secrets
type: Opaque
data:
  AWS_ACCESS_KEY_ID: <base64-encoded-key>
  AWS_SECRET_ACCESS_KEY: <base64-encoded-secret>
```

## Environment Variable Validation

The agent validates environment variables on startup:

```bash
# Check if all required variables are set
python -c "
import os
required_vars = ['AWS_REGION', 'BEDROCK_MODEL_ID']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f'❌ Missing required environment variables: {missing_vars}')
    exit(1)
else:
    print('✅ All required environment variables are set')
"
```

## Best Practices

### 1. Use .env Files for Local Development
```bash
# Create .env file
cat > .env << EOF
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=claude-3.5-sonnet
PORT=8080
DEBUG_MODE=true
EOF

# Load environment variables
source .env
```

### 2. Never Commit Secrets
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
echo "*.env" >> .gitignore
```

### 3. Use Different Files for Different Environments
```bash
# Development
.env.development

# Staging  
.env.staging

# Production
.env.production
```

### 4. Validate Configuration Before Deployment
```bash
# Check configuration
make agentcore-status
```

## Troubleshooting

### Common Issues

#### 1. Missing AWS Credentials
```bash
# Error: AWS credentials not found
# Solution: Configure AWS credentials
aws configure
# or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

#### 2. Invalid Model ID
```bash
# Error: Invalid model ID
# Solution: Use supported model name or full ID
export BEDROCK_MODEL_ID=claude-3.5-sonnet
# or
export BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0
```

#### 3. Port Already in Use
```bash
# Error: Port 8080 already in use
# Solution: Use different port
export PORT=8081
```

#### 4. Debug Mode Issues
```bash
# Error: Debug mode not working
# Solution: Ensure DEBUG_MODE is set correctly
export DEBUG_MODE=true
# or
export DEBUG_MODE=false
```

## AWS Account Management

The AWS DevOps Agent now includes intelligent account management that works in two modes:

### Interactive Mode (Default)
When you start the agent, it will:
1. **Detect your current AWS account** from credentials
2. **Show account information** (ID, name, permissions)
3. **Offer options** to use current account or specify a different one
4. **Validate access** before proceeding

### Environment Variable Mode
Set these variables to skip interactive selection:
```bash
export AWS_ACCOUNT_ID=123456789012
export AWS_ACCOUNT_NAME=My Production Account
export AWS_ROLE_ARN=arn:aws:iam::123456789012:role/DevOpsRole
```

### Account Management Commands
Once running, use these commands:
- `accounts` - Show all managed accounts
- `switch-account` - Switch to a different account
- `account-status` - Show current account details
- `help` - Show all available commands

### Cross-Account Access
For multi-account operations, configure cross-account roles:
```bash
export CROSS_ACCOUNT_ROLES=account1:role1,account2:role2
```

## Quick Reference

### Essential Variables
```bash
# Minimum required for basic operation
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=claude-3.5-sonnet
```

### Full Configuration
```bash
# Complete configuration
export AWS_REGION=us-east-1
export AWS_PROFILE=production
export BEDROCK_REGION=us-east-1
export BEDROCK_MODEL_ID=claude-3.5-sonnet
export PORT=8080
export HOST=0.0.0.0
export DEBUG_MODE=false
export LOG_LEVEL=INFO
export CROSS_ACCOUNT_ROLES=account1:role1,account2:role2
```

### Testing Configuration
```bash
# Test with debug mode
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
export PORT=8080
export HOST=localhost
```

---

**💡 Tip**: Always test your configuration with `make agentcore-test-local` before deploying to production!
