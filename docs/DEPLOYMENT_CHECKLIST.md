# 🚀 Production Deployment Checklist - Bedrock AgentCore

## Pre-Deployment Verification

### Environment Setup
- [ ] Virtual environment created and activated (`.venv/`)
- [ ] All dependencies installed (`make setup` completed successfully)
- [ ] Bedrock AgentCore CLI installed in virtual environment
- [ ] AWS credentials configured for production account
- [ ] AWS CLI authenticated and working (`aws sts get-caller-identity`)

### Code Quality
- [ ] All tests passing (`make test`)
- [ ] Code formatted (`make format`)
- [ ] No linting errors
- [ ] Code review completed and approved
- [ ] AgentCore wrapper tested locally (`make agentcore-test-local`)

### MCP Integration
- [ ] MCP servers installed and functional (`make mcp-check`)
- [ ] MCP connections tested (`make mcp-test`)
- [ ] Real AWS APIs accessible via MCP servers
- [ ] Fallback mechanisms working for MCP failures

### Configuration
- [ ] Production environment variables set
- [ ] AWS region configured correctly (us-east-1)
- [ ] Model configuration appropriate for production
- [ ] Logging level set to INFO or WARNING (not DEBUG)

## Deployment Steps

### 1. Configuration Phase
```bash
# Configure AgentCore for production
make agentcore-configure
```

**Verification Required:**
- [ ] Review generated `.bedrock_agentcore.yaml` file
- [ ] Verify entrypoint points to correct file (`app.py`)
- [ ] Confirm region is set to `us-east-1`
- [ ] Check environment is set to `production`
- [ ] Validate agent name is appropriate

### 2. Local Testing Phase
```bash
# Test deployment locally before production
make agentcore-test-local
```

**Verification Required:**
- [ ] Agent starts successfully locally
- [ ] All tools are loaded and functional
- [ ] MCP servers connect properly
- [ ] Agent responds to test queries
- [ ] No critical errors in logs

### 3. Human Verification Phase
```bash
# Run human verification (mandatory)
make agentcore-deploy-verify
```

**Verification Required:**
- [ ] Authorized personnel confirmed
- [ ] Configuration reviewed and approved
- [ ] Ready to proceed with production deployment
- [ ] Rollback plan understood and available

### 4. Production Deployment
```bash
# Deploy to production (only after all verifications)
make agentcore-deploy
```

**Verification Required:**
- [ ] Deployment completed successfully
- [ ] No deployment errors
- [ ] Agent status shows as running

## Post-Deployment Verification

### Immediate Verification (0-5 minutes)
- [ ] Check deployment status (`make agentcore-status`)
- [ ] Test agent functionality (`make agentcore-test`)
- [ ] Verify logs show no critical errors (`make agentcore-logs`)
- [ ] Confirm all tools are accessible

### Functional Testing (5-15 minutes)
- [ ] Test cost analysis capabilities
- [ ] Test IaC analysis tools
- [ ] Test security compliance tools
- [ ] Test multi-account operations
- [ ] Test GitHub integration tools

### Performance Monitoring (15-30 minutes)
- [ ] Monitor response times
- [ ] Check resource utilization
- [ ] Verify MCP server connections
- [ ] Monitor error rates
- [ ] Check memory usage

### Long-term Monitoring (ongoing)
- [ ] Set up CloudWatch alarms
- [ ] Monitor cost impact
- [ ] Track agent performance metrics
- [ ] Review logs regularly
- [ ] Monitor MCP server health

## Rollback Procedures

### Immediate Rollback (if critical issues)
```bash
# Rollback deployment
make agentcore-rollback
```

**Rollback Verification:**
- [ ] Rollback completed successfully
- [ ] Previous version restored
- [ ] Agent functionality verified
- [ ] No data loss occurred

### Investigation Phase
- [ ] Review logs for root cause
- [ ] Identify specific failure points
- [ ] Document issues and solutions
- [ ] Plan remediation steps

### Re-deployment (after fixes)
- [ ] Fix identified issues
- [ ] Test fixes locally
- [ ] Follow full deployment checklist again
- [ ] Monitor closely after re-deployment

## Emergency Contacts

### Primary Contacts
- **Deployment Lead**: [Name] - [Email] - [Phone]
- **AWS Admin**: [Name] - [Email] - [Phone]
- **DevOps Team**: [Name] - [Email] - [Phone]

### Escalation Path
1. **Level 1**: DevOps Team (immediate response)
2. **Level 2**: AWS Admin (if AWS-related issues)
3. **Level 3**: Deployment Lead (if critical issues)
4. **Level 4**: Management (if business impact)

## Security Considerations

### Access Control
- [ ] Only authorized personnel can deploy
- [ ] AWS credentials properly secured
- [ ] No hardcoded secrets in code
- [ ] Environment variables properly configured

### Data Protection
- [ ] No sensitive data in logs
- [ ] Proper data encryption in transit
- [ ] Secure communication with AWS APIs
- [ ] MCP server connections secured

### Compliance
- [ ] Deployment follows company policies
- [ ] All changes documented
- [ ] Audit trail maintained
- [ ] Compliance requirements met

## Success Criteria

### Technical Success
- [ ] Agent deploys without errors
- [ ] All tools functional
- [ ] Performance within acceptable limits
- [ ] No critical security issues

### Business Success
- [ ] Agent provides value to users
- [ ] Cost optimization recommendations accurate
- [ ] Security analysis comprehensive
- [ ] Compliance reporting effective

## Post-Deployment Tasks

### Documentation
- [ ] Update deployment documentation
- [ ] Document any configuration changes
- [ ] Update runbooks if needed
- [ ] Share lessons learned

### Monitoring Setup
- [ ] Configure CloudWatch dashboards
- [ ] Set up alerting rules
- [ ] Create monitoring runbooks
- [ ] Train team on monitoring tools

### Maintenance Planning
- [ ] Schedule regular health checks
- [ ] Plan for updates and patches
- [ ] Create maintenance windows
- [ ] Document maintenance procedures

---

## Quick Reference Commands

```bash
# Setup and Installation
make setup                    # Complete setup including AgentCore
make agentcore-install        # Install AgentCore CLI only

# Configuration and Testing
make agentcore-configure      # Configure for production
make agentcore-test-local     # Test locally before deployment

# Deployment
make agentcore-deploy-verify  # Human verification (mandatory)
make agentcore-deploy         # Deploy to production

# Monitoring and Management
make agentcore-status         # Check deployment status
make agentcore-logs           # View logs
make agentcore-test           # Test deployed agent
make agentcore-monitor        # Comprehensive monitoring

# Emergency
make agentcore-rollback       # Rollback deployment
```

---

**⚠️ CRITICAL REMINDER**: This checklist must be completed in full before any production deployment. No shortcuts or skipped steps are allowed.
