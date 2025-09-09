# AWS DevOps Agent - Complete User Manual

## Overview

The AWS DevOps Agent is a production-ready AI-powered automation tool that transforms complex AWS DevOps operations into natural language conversations. Built on the Strands framework with Bedrock Agent Core integration, it combines real-time AWS data with intelligent analysis to provide actionable insights for cost optimization, security compliance, and infrastructure management.

**Core Architecture:**
- **Strands Framework** for AI orchestration
- **Bedrock Agent Core** for sophisticated reasoning with Claude Sonnet 4
- **Official AWS MCP Servers** for real-time data access
- **GitHub Integration** for automated infrastructure improvements
- **Multi-Account Support** for enterprise operations

## What the Agent Does

Instead of manually running complex AWS CLI commands, navigating multiple consoles, or writing custom scripts, you can:

- **Analyze costs** with real-time AWS pricing and usage data
- **Optimize infrastructure** with actionable recommendations
- **Validate security** against compliance frameworks (SOC2, HIPAA, PCI-DSS, ISO27001)
- **Manage Infrastructure as Code** for Terraform, CloudFormation, and CDK
- **Generate professional reports** automatically saved to files
- **Create GitHub pull requests** with infrastructure improvements
- **Monitor multi-account** AWS environments
- **Automate compliance** checking and reporting

## Quick Start

### Prerequisites
- Python 3.10+
- AWS credentials configured
- Basic familiarity with AWS services

### Complete Setup (5 minutes)

```bash
# 1. Clone and setup everything
git clone <repository-url>
cd strands-bedrock-mcp-devops-agent
make setup
source .venv/bin/activate

# 2. Start the agent
make run
```

The setup automatically installs and configures all required components including AWS MCP servers.

## How to Use the Agent

### Three Ways to Interact

**1. Interactive Mode (Recommended)**
```bash
make run
```
Full conversation mode with context awareness and follow-up questions.

**2. Single Query Mode**
```bash
make query QUERY="Analyze my AWS costs for the last 30 days"
```
Perfect for automation, scripts, and CI/CD pipelines.

**3. Demo Mode**
```bash
make dev
```
Watch automated examples to learn capabilities.

## Complete Tool Reference

### Cost Analysis and Optimization Tools

**Real-Time Cost Analysis**
- `get_actual_aws_costs` - Live cost data from Cost Explorer
- `analyze_cost_trends_real` - Cost trend analysis over time
- `get_real_aws_pricing` - Current AWS pricing across all services
- `analyze_cost_optimization_opportunities` - Find savings opportunities

**Instance and Resource Optimization**
- `get_rightsizing_recommendations` - EC2 instance rightsizing
- `get_reserved_instance_recommendations` - RI savings analysis
- `calculate_reserved_instance_savings` - RI vs On-Demand cost comparison
- `generate_cost_comparison_report` - Multi-service cost comparisons

**Example Queries:**
```
"Analyze my AWS costs for the last 30 days"
"Compare t3.medium vs m5.large for web application workloads"
"Find Reserved Instance opportunities with ROI analysis"
"What would it cost to migrate this workload to us-west-2?"
```

### Infrastructure as Code (IaC) Analysis Tools

**Terraform Analysis**
- `analyze_terraform_project` - Comprehensive project analysis
- `validate_terraform_configuration` - Syntax and logic validation
- `plan_terraform_changes` - Generate and analyze Terraform plans
- `analyze_terraform_state` - State file analysis and drift detection
- `generate_terraform_optimization_report` - Detailed optimization reports

**CloudFormation Analysis**
- `validate_cloudformation_template` - Template validation
- `analyze_cloudformation_stack` - Stack configuration analysis
- `scan_infrastructure_drift` - Detect configuration drift
- `generate_iac_best_practices_report` - Best practices validation

**CDK Analysis**
- `analyze_cdk_project` - CDK project structure and code analysis
- `synthesize_cdk_project` - Generate CloudFormation from CDK
- `analyze_cdk_synthesized_output` - Analyze generated templates
- `generate_cdk_optimization_report` - Comprehensive CDK optimization

**Example Queries:**
```
"Analyze my Terraform configuration for best practices"
"Validate my CloudFormation template for security issues"
"Generate a CDK optimization report for my project"
"Check for infrastructure drift in my environment"
```

### Security and Compliance Tools

**Real AWS Security Analysis**
- `analyze_security_hub_findings` - Live Security Hub data
- `analyze_config_compliance` - AWS Config compliance status
- `analyze_inspector_findings` - Amazon Inspector vulnerabilities
- `get_security_recommendations` - Trusted Advisor security recommendations
- `perform_comprehensive_security_analysis` - Combined security assessment

**Compliance Framework Support**
- `validate_security_policies` - Security policy validation
- `check_compliance_standards` - SOC2, HIPAA, PCI-DSS, ISO27001 checks
- `generate_compliance_report` - Framework-specific compliance reports
- `scan_security_vulnerabilities` - Multi-service vulnerability scanning

**Example Queries:**
```
"Perform comprehensive security analysis using real AWS data"
"Check SOC2 compliance for my infrastructure"
"Scan for security vulnerabilities across all services"
"Generate HIPAA compliance report for my healthcare application"
```

### Multi-Account Management Tools

**Cross-Account Operations**
- `list_cross_account_resources` - Resource discovery across accounts
- `execute_cross_account_operation` - Multi-account operations
- `generate_multi_account_report` - Organization-wide reporting
- `monitor_cross_account_compliance` - Cross-account compliance monitoring

**Account Management**
- Interactive account selection and switching
- Cross-account role assumption
- Organization-wide cost analysis
- Centralized compliance monitoring

**Example Queries:**
```
"Generate cost report for all accounts in my organization"
"Check compliance across all AWS accounts"
"List all EC2 instances across my organization"
"Monitor security status across multiple accounts"
```

### GitHub Integration Tools

**Automated Infrastructure Improvements**
- `create_optimization_pull_request` - Cost optimization PRs
- `update_iac_via_github` - Infrastructure updates via GitHub
- `create_terraform_security_pr` - Security improvement PRs
- `list_infrastructure_repositories` - Repository discovery
- `monitor_infrastructure_prs` - PR monitoring and management

**Repository Analysis**
- `check_repository_connectivity` - Test GitHub access
- `get_repository_info` - Repository details and structure
- `list_repository_branches` - Branch listing and analysis
- `create_branch_simple` - Automated branch creation

**Example Queries:**
```
"Create a pull request with cost optimization recommendations"
"Generate infrastructure updates based on security analysis"
"Analyze my Terraform repository structure"
"Create a GitHub issue for critical security findings"
```

### Document Generation Tools

**Automatic Report Creation**
- `generate_document` - General document generation
- `generate_cost_analysis_document` - Cost analysis reports
- `generate_security_compliance_document` - Security compliance reports
- `generate_infrastructure_document` - IaC analysis reports
- `generate_cdk_analysis_document` - CDK optimization reports

**Report Management**
- `list_generated_documents` - View all generated reports
- `get_document_info` - Document details and metadata
- Automatic organization in `reports/` folder
- Multiple formats: Markdown, JSON, CSV, Excel

**Example Queries:**
```
"Generate a comprehensive cost analysis report"
"Create a security compliance document for audit"
"Generate executive summary of infrastructure analysis"
"List all reports generated this month"
```

## Document Generation and Reports

### Automatic File Creation
All analysis can be saved as professional reports in the `reports/` folder:

```
reports/
├── cost-analysis/          # Cost optimization reports
├── security-compliance/    # Security and compliance reports
├── infrastructure-as-code/ # IaC analysis reports
├── cdk-analysis/          # CDK project reports
├── compliance-reports/    # Framework-specific compliance
├── multi-account/         # Organization-wide reports
└── general/              # Custom reports
```

### Report Formats
- **Markdown (.md)** - Human-readable with rich formatting
- **JSON (.json)** - Machine-readable structured data
- **CSV (.csv)** - Spreadsheet-compatible tabular data
- **Excel (.xlsx)** - Complex reports with multiple sheets

### Timestamped Files
All files are automatically timestamped to prevent overwrites:
- Format: `{title}_{YYYYMMDD_HHMMSS}.{extension}`
- Example: `cost_analysis_20250906_192643.md`

## Configuration and Environment

### Environment Variables

**Required for Production:**
```bash
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=claude-3.5-sonnet
export PORT=8080
export HOST=0.0.0.0
```

**Optional Configuration:**
```bash
export DEBUG_MODE=false
export LOG_LEVEL=INFO
export AWS_PROFILE=production
export MCP_TIMEOUT=30
export MCP_MAX_WORKERS=10
```

**GitHub Integration:**
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxxxxx
export GITHUB_ORG=your-organization
export GITHUB_DEFAULT_REPO=your-org/your-repo
```

**Multi-Account Configuration:**
```bash
export CROSS_ACCOUNT_ROLES=account1:role1,account2:role2
export AWS_ACCOUNT_ID=123456789012
export AWS_ACCOUNT_NAME=Production Account
```

### Quick Environment Setup
```bash
# Create production environment
make agentcore-env-prod

# Create development environment
make agentcore-env-dev

# Validate configuration
make agentcore-validate
```

## Deployment Options

### Local Development
```bash
# Standard local deployment
make run

# Test locally before production
make agentcore-test-local
```

### Production Deployment to Bedrock AgentCore

**Complete Production Process:**
```bash
# 1. Configure for production
make agentcore-configure

# 2. Test locally first
make agentcore-test-local

# 3. Human verification (mandatory)
make agentcore-deploy-verify

# 4. Deploy to production
make agentcore-deploy

# 5. Monitor deployment
make agentcore-status
make agentcore-logs
```

**Production Features:**
- Multi-stage Docker build with security hardening
- Health monitoring endpoints (`/health`, `/metrics`)
- Structured logging with request tracking
- IAM policy with comprehensive permissions
- Automatic rollback capabilities

### CI/CD Integration
```yaml
# Example GitHub Actions
- name: AWS Cost Analysis
  run: make query QUERY="Analyze costs for this deployment"
  
- name: Security Validation
  run: make query QUERY="Validate security policies for new resources"
```

## Safety and Security Features

### Critical Safety Measures

**No Automatic Actions:**
- Never creates PRs without explicit user consent
- Never modifies infrastructure without permission
- Never pushes code without approval
- All dangerous operations require `user_consent=True` parameter

**Function-Level Protection:**
```python
# All dangerous functions include safety checks
if not user_consent:
    return {
        "status": "error",
        "error": "CRITICAL: User consent required!",
        "safety_message": "This function requires explicit user approval."
    }
```

**Message-Level Protection:**
The agent automatically detects dangerous patterns in requests:
- "create pull request", "deploy", "modify infrastructure"
- Blocks action and requests explicit approval
- Provides clear safety warnings

### Read-Only Operations (Safe)
- `analyze_*`, `scan_*`, `check_*`, `validate_*`
- `monitor_*`, `list_*`, `get_*`, `read_*`
- `generate_report`, `prepare_recommendations`

### Consent-Required Operations (Dangerous)
- `create_*`, `update_*`, `modify_*`, `deploy_*`
- `push_*`, `commit_*`, infrastructure changes
- Any GitHub or code modifications

### Security Configuration
```python
@dataclass
class SafetyConfig:
    require_explicit_consent_for_prs: bool = True
    require_explicit_consent_for_commits: bool = True
    require_explicit_consent_for_infrastructure_changes: bool = True
```

## GitHub Integration

### Setup Requirements
1. **GitHub Personal Access Token** with scopes:
   - `repo` - Full control of private repositories
   - `read:org` - Read org and team membership
   - `read:user` - Read user profile data
   - `project` - Read/write project boards

2. **Go Installation** (for GitHub MCP server)
3. **Environment Configuration**

### GitHub Tools Available
- **Repository Management**: Browse, analyze, manage repositories
- **Pull Request Automation**: Create PRs with infrastructure changes
- **Issue Tracking**: Create and manage GitHub issues
- **Branch Operations**: Create branches, manage merges
- **Code Analysis**: Analyze repository structure and dependencies

### Quick GitHub Test
```bash
# Install GitHub MCP server
make mcp-install

# Add GitHub token
echo "GITHUB_PERSONAL_ACCESS_TOKEN=your_token" >> .env

# Test connectivity
make github-test-connectivity REPO=octocat/Hello-World

# Start agent with GitHub integration
make run
```

## MCP Server Integration

### Official AWS MCP Servers
- **Cost Explorer MCP** - Real-time cost data
- **CloudWatch MCP** - Metrics and monitoring data
- **AWS Pricing MCP** - Current service pricing
- **Terraform MCP** - Terraform operations
- **DynamoDB MCP** - Database operations
- **GitHub MCP** - Repository management

### MCP Management Commands
```bash
# Check all MCP servers
make mcp-check

# Install MCP servers
make mcp-install

# Test MCP connections
make mcp-test

# Start MCP servers
make mcp-run

# Stop MCP servers
make mcp-stop
```

## Advanced Usage Examples

### Cost Optimization Workflow
```
1. "Analyze my AWS costs for the last 90 days"
2. "Find Reserved Instance opportunities with ROI analysis"
3. "Generate a cost optimization report for management"
4. "Create a GitHub PR with cost optimization changes"
```

### Security Compliance Workflow
```
1. "Perform comprehensive security analysis using real AWS data"
2. "Check SOC2 compliance for my infrastructure"
3. "Generate security compliance report for audit"
4. "Create GitHub issues for critical security findings"
```

### Infrastructure Analysis Workflow
```
1. "Analyze my Terraform project for best practices"
2. "Check for security vulnerabilities in my CDK code"
3. "Generate infrastructure optimization report"
4. "Create PR with recommended infrastructure improvements"
```

### Multi-Account Management Workflow
```
1. "List all accounts in my organization"
2. "Generate cost report across all accounts"
3. "Check compliance status organization-wide"
4. "Create consolidated security assessment"
```

## Common Use Cases

### Daily Operations
- Morning cost check: "Show yesterday's AWS spending"
- Resource optimization: "Find underutilized resources"
- Security monitoring: "Check for new security alerts"
- Performance review: "Show CloudWatch metrics for critical services"

### Weekly Reviews
- Cost trend analysis: "Analyze weekly cost trends"
- Compliance monitoring: "Run weekly security assessment"
- Infrastructure health: "Check infrastructure drift"
- Team reporting: "Generate weekly DevOps summary"

### Monthly Planning
- Executive reporting: "Generate monthly cost report for management"
- Capacity planning: "Analyze resource utilization trends"
- Security audits: "Perform comprehensive monthly security review"
- Compliance preparation: "Generate SOC2 compliance documentation"

### Project Workflows
- New deployments: "Estimate cost impact of new infrastructure"
- Migration planning: "Compare costs between architectures"
- Code reviews: "Analyze IaC changes for security issues"
- Compliance validation: "Check changes against compliance requirements"

## Troubleshooting

### Setup Issues

**Virtual Environment Problems:**
```bash
# Recreate environment
make clean
make setup
source .venv/bin/activate
```

**AWS Credentials Issues:**
```bash
# Configure credentials
aws configure
aws sts get-caller-identity
```

**MCP Server Issues:**
```bash
# Reinstall MCP servers
make mcp-install
make mcp-check
```

### Runtime Issues

**Permission Denied:**
- Ensure AWS credentials have required permissions
- Check IAM policies include necessary actions
- Verify cross-account roles are properly configured

**GitHub Integration Issues:**
```bash
# Check GitHub token
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# Test connectivity
make github-test-connectivity REPO=octocat/Hello-World
```

**Agent Not Responding:**
```bash
# Check status
make status

# View logs
make agentcore-logs

# Restart agent
make clean && make setup
```

### Debug Mode
```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
export DEBUG_MODE=true
make run
```

## Best Practices

### Cost Management
- Run cost analysis weekly
- Review RI recommendations quarterly
- Monitor for cost anomalies daily
- Implement cost allocation tags

### Security and Compliance
- Perform security assessments monthly
- Enable continuous compliance monitoring
- Keep security policies current
- Maintain audit documentation

### Infrastructure Management
- Use Infrastructure as Code consistently
- Implement automated testing
- Maintain version control for all infrastructure
- Document architecture decisions

### Multi-Account Operations
- Use AWS Organizations for centralized billing
- Implement least privilege access
- Standardize policies across accounts
- Monitor all accounts consistently

### GitHub Integration
- Review all generated PRs before merging
- Test infrastructure changes in development
- Document all automated changes
- Maintain branch protection rules

## Supported Technologies

### AWS Services
**Cost Management:** Cost Explorer, Pricing API, Budgets, Trusted Advisor
**Compute:** EC2, Lambda, ECS, EKS, Fargate
**Storage:** S3, EBS, EFS, FSx
**Database:** RDS, DynamoDB, ElastiCache, Redshift
**Security:** Security Hub, Config, Inspector, IAM, KMS
**Networking:** VPC, CloudFront, Route 53, Load Balancers
**Monitoring:** CloudWatch, CloudTrail, X-Ray

### Infrastructure as Code
**Terraform:** HCL configuration analysis, state management, plan generation
**CloudFormation:** Template validation, stack analysis, drift detection
**AWS CDK:** TypeScript, JavaScript, Python, Java project analysis

### Compliance Frameworks
**SOC2:** System and Organization Controls Type 2
**HIPAA:** Healthcare Information Portability and Accountability Act
**PCI-DSS:** Payment Card Industry Data Security Standard
**ISO27001:** Information Security Management System
**NIST:** National Institute of Standards and Technology frameworks

### Programming Languages
**CDK Support:** TypeScript, JavaScript, Python, Java
**Terraform:** HCL (HashiCorp Configuration Language)
**CloudFormation:** JSON, YAML templates

## Performance and Scaling

### Response Times
- Cost analysis: 10-30 seconds
- Security analysis: 15-45 seconds
- IaC analysis: 5-20 seconds
- Document generation: 5-15 seconds

### Scaling Considerations
- Multi-account operations may take longer
- Large Terraform projects require more processing time
- Comprehensive security analysis increases with resource count
- GitHub operations depend on repository size

### Resource Usage
- Memory: 512MB - 2GB depending on analysis complexity
- Network: Requires stable internet for AWS API calls
- Storage: Reports stored locally in `reports/` folder

## Getting Maximum Value

### Start Simple
Begin with basic cost analysis to understand current spending patterns and tool capabilities.

### Build Workflows
Integrate the agent into daily operations:
- Morning: Quick cost and security checks
- Code reviews: IaC analysis for changes
- Planning: Cost estimation for new projects
- Reporting: Automated report generation

### Automate Integration
Use in CI/CD pipelines for:
- Cost impact analysis on deployments
- Security validation on infrastructure changes
- Compliance checks before production releases
- Automated documentation generation

### Team Collaboration
- Generate reports for different stakeholders
- Use GitHub integration for team reviews
- Maintain consistency across environments
- Document decisions and recommendations

## Support and Updates

### Documentation Resources
- This comprehensive user manual
- Individual tool documentation in source
- Example workflows and demos
- Troubleshooting guides

### Getting Help
```bash
# Check all available commands
make help

# View system status
make status

# Run diagnostics
make mcp-test
```

### Staying Updated
- AWS MCP servers automatically provide latest data
- Agent uses current AWS APIs for real-time information
- GitHub integration stays current with repository changes

---

## Command Reference

### Essential Commands
```bash
# Setup and Installation
make setup                    # Complete setup with all components
make status                   # Check system status
make help                     # Show all commands

# Running the Agent
make run                      # Interactive conversation mode
make dev                      # Demo mode with examples  
make query QUERY="question"   # Single query mode

# MCP Server Management
make mcp-check               # Check MCP server status
make mcp-install             # Install all AWS MCP servers
make mcp-test                # Test MCP connections

# GitHub Integration
make github-test-connectivity REPO=owner/repo
make mcp-install             # Includes GitHub MCP setup

# Production Deployment
make agentcore-configure     # Configure for Bedrock AgentCore
make agentcore-test-local    # Test locally before production
make agentcore-deploy-verify # Mandatory human verification
make agentcore-deploy        # Deploy to production
make agentcore-status        # Check deployment status
make agentcore-logs          # View production logs
make agentcore-rollback      # Emergency rollback

# Environment Management  
make agentcore-env-prod      # Create production environment
make agentcore-env-dev       # Create development environment
make agentcore-validate      # Validate configuration

# Maintenance
make clean                   # Clean temporary files
make test                    # Run test suite
```

---

**The AWS DevOps Agent transforms complex AWS operations into natural conversations, providing real-time insights, automated improvements, and professional reports. Whether you're optimizing costs, ensuring compliance, or managing infrastructure, the agent makes advanced AWS operations accessible to everyone.**