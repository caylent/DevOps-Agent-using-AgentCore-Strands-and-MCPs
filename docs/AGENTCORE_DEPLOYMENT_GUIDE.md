# 🚀 AWS DevOps Agent - Bedrock AgentCore Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the AWS DevOps Agent to Amazon Bedrock AgentCore with comprehensive safety measures and human-in-the-loop verification.

## Prerequisites

### System Requirements
- Python 3.10+
- AWS CLI configured with production credentials
- Virtual environment support
- `uv` package manager (for MCP servers)

### Environment Variables
The agent uses environment variables for configuration. See [Environment Variables Guide](ENVIRONMENT_VARIABLES.md) for complete details.

**Required:**
- `AWS_REGION` - AWS region (e.g., us-east-1)
- `BEDROCK_MODEL_ID` - Model ID (e.g., claude-3.5-sonnet)

**Optional:**
- `PORT` - Server port (default: 8080)
- `HOST` - Server host (default: 0.0.0.0)
- `DEBUG_MODE` - Debug mode (default: false)
- `LOG_LEVEL` - Log level (default: INFO)

### AWS Permissions Required
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:*",
                "ecr:*",
                "iam:*",
                "cloudformation:*",
                "s3:*",
                "logs:*",
                "ce:*",
                "cloudwatch:*",
                "pricing:*"
            ],
            "Resource": "*"
        }
    ]
}
```

## Quick Start Deployment

### 1. Complete Setup (5 minutes)
```bash
# Clone and setup everything
git clone <repository-url>
cd strands-bedrock-mcp-devops-agent
make setup
source .venv/bin/activate
```

### 2. Configure Environment Variables (2 minutes)
```bash
# Set production environment variables
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=claude-3.5-sonnet
export PORT=8080
export HOST=0.0.0.0
export DEBUG_MODE=false

# Or create .env.production file
cat > .env.production << EOF
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=claude-3.5-sonnet
PORT=8080
HOST=0.0.0.0
DEBUG_MODE=false
EOF
```

### 3. Test Locally (5 minutes)
```bash
# Test deployment locally before production
make agentcore-test-local
```

### 4. Deploy to Production (10 minutes)
```bash
# Deploy with human verification
make agentcore-deploy
```

## Detailed Deployment Process

### Phase 1: Environment Preparation

#### 1.1 Verify Prerequisites
```bash
# Check Python version
python3 --version  # Should be 3.10+

# Check AWS credentials
aws sts get-caller-identity

# Check virtual environment
ls -la .venv/
```

#### 1.2 Complete Setup
```bash
# Run complete setup (includes AgentCore installation)
make setup

# Verify installation
make status
```

### Phase 2: Configuration

#### 2.1 Configure AgentCore
```bash
# Configure for production deployment
make agentcore-configure
```

This command will:
- Generate `.bedrock_agentcore.yaml` configuration file
- Create `Dockerfile` for containerization
- Set up production environment settings
- Configure region and environment parameters

#### 2.2 Review Configuration
```bash
# Review generated configuration
cat deployment/bedrock/.bedrock_agentcore.yaml
cat deployment/bedrock/Dockerfile
```

**Critical Review Points:**
- Entrypoint points to `app.py`
- Region set to `us-east-1`
- Environment set to `production`
- Agent name is appropriate
- Resource limits are reasonable

### Phase 3: Local Testing

#### 3.1 Test Deployment Locally
```bash
# Test the deployment locally
make agentcore-test-local
```

This will:
- Build the Docker image locally
- Start the agent in local mode
- Test all functionality
- Verify MCP server connections

#### 3.2 Verify Local Functionality
```bash
# Test agent capabilities
make agentcore-test
```

**Test Scenarios:**
- Basic agent response
- Cost analysis tools
- IaC analysis tools
- Security compliance tools
- Multi-account operations

### Phase 4: Production Deployment

#### 4.1 Human Verification (Mandatory)
```bash
# Run human verification process
make agentcore-deploy-verify
```

This will prompt for:
- Authorization confirmation
- Configuration review confirmation
- Final deployment confirmation

#### 4.2 Deploy to Production
```bash
# Deploy to Bedrock AgentCore
make agentcore-deploy
```

This will:
- Build production Docker image
- Push to Amazon ECR
- Deploy to Bedrock AgentCore
- Configure production environment

### Phase 5: Post-Deployment Verification

#### 5.1 Immediate Verification
```bash
# Check deployment status
make agentcore-status

# Test deployed agent
make agentcore-test

# View logs
make agentcore-logs
```

#### 5.2 Comprehensive Monitoring
```bash
# Run comprehensive monitoring
make agentcore-monitor
```

## Safety Measures

### Human-in-the-Loop Verification
- **Mandatory approval** before production deployment
- **Multi-step confirmation** process
- **Configuration review** requirement
- **Authorization check** for deployment personnel

### Environment Protection
- **Production-only** deployment target
- **Explicit environment confirmation**
- **Account verification** before deployment
- **Region validation** to prevent misconfiguration

### Rollback Capabilities
- **Immediate rollback** available (`make agentcore-rollback`)
- **Version tracking** for easy rollback
- **Verification steps** after rollback
- **Monitoring** to detect issues

## Monitoring and Maintenance

### Daily Monitoring
```bash
# Check agent status
make agentcore-status

# Review recent logs
make agentcore-logs

# Test functionality
make agentcore-test
```

### Weekly Maintenance
```bash
# Comprehensive monitoring
make agentcore-monitor

# Check MCP server health
make mcp-check

# Run full test suite
make test
```

### Monthly Review
- Review performance metrics
- Analyze cost impact
- Update documentation
- Plan improvements

## Troubleshooting

### Common Issues

#### 1. Virtual Environment Not Found
```bash
# Error: Virtual environment not found
# Solution: Run setup first
make setup
source .venv/bin/activate
```

#### 2. AWS Credentials Not Configured
```bash
# Error: AWS credentials not found
# Solution: Configure AWS credentials
aws configure
aws sts get-caller-identity
```

#### 3. AgentCore CLI Not Found
```bash
# Error: agentcore command not found
# Solution: Install AgentCore CLI
make agentcore-install
```

#### 4. MCP Servers Not Available
```bash
# Error: MCP servers not available
# Solution: Install MCP servers
make mcp-install
make mcp-check
```

#### 5. Deployment Fails
```bash
# Error: Deployment failed
# Solution: Check logs and rollback if needed
make agentcore-logs
make agentcore-rollback
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
make agentcore-deploy

# Check detailed logs
make agentcore-logs
```

## Emergency Procedures

### Critical Issues
1. **Immediate Rollback**
   ```bash
   make agentcore-rollback
   ```

2. **Check Status**
   ```bash
   make agentcore-status
   ```

3. **Review Logs**
   ```bash
   make agentcore-logs
   ```

4. **Contact Support**
   - Check emergency contacts in deployment checklist
   - Escalate according to severity

### Performance Issues
1. **Monitor Performance**
   ```bash
   make agentcore-monitor
   ```

2. **Check Resource Usage**
   ```bash
   make agentcore-logs | grep -i "memory\|cpu\|error"
   ```

3. **Scale if Needed**
   - Contact AWS support for scaling options
   - Consider resource adjustments

## Best Practices

### Security
- Use IAM roles instead of access keys
- Rotate credentials regularly
- Monitor access logs
- Implement least privilege access

### Performance
- Monitor resource usage
- Set up CloudWatch alarms
- Regular performance reviews
- Optimize based on usage patterns

### Maintenance
- Regular health checks
- Update dependencies
- Monitor security advisories
- Plan maintenance windows

## Support and Resources

### Documentation
- [Deployment Checklist](DEPLOYMENT_CHECKLIST.md)
- [Usage Guide](APP_USAGE.md)
- [AWS Security Analysis](AWS_SECURITY_ANALYSIS.md)

### Commands Reference
```bash
# Setup and Installation
make setup                    # Complete setup
make agentcore-install        # Install AgentCore CLI
make mcp-install             # Install MCP servers

# Configuration and Testing
make agentcore-configure      # Configure for production
make agentcore-test-local     # Test locally

# Deployment
make agentcore-deploy-verify  # Human verification
make agentcore-deploy         # Deploy to production

# Monitoring and Management
make agentcore-status         # Check status
make agentcore-logs           # View logs
make agentcore-test           # Test agent
make agentcore-monitor        # Comprehensive monitoring

# Emergency
make agentcore-rollback       # Rollback deployment
```

### Getting Help
- Check this guide and deployment checklist
- Review logs for error details
- Contact DevOps team for support
- Escalate critical issues immediately

---

**⚠️ IMPORTANT**: Always follow the deployment checklist and never skip human verification steps. Production deployments require explicit approval and careful monitoring.
