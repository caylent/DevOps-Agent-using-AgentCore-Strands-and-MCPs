# 🚀 AWS DevOps Agent - Usage Guide

## 📋 Table of Contents
- [Quick Start](#-quick-start)
- [Installation & Setup](#-installation--setup)
- [Running the Agent](#-running-the-agent)
- [Usage Examples](#-usage-examples)
- [Tool Categories](#-tool-categories)
- [Advanced Usage](#-advanced-usage)
- [Troubleshooting](#-troubleshooting)
- [Best Practices](#-best-practices)

---

## 🚀 Quick Start

### **1. Complete Setup (3 minutes)**
```bash
# Clone and setup
git clone <repository-url>
cd strands-bedrock-mcp-devops-agent
make setup
source .venv/bin/activate
```

### **2. Run the Agent**
```bash
# Interactive mode (recommended)
make run

# Demo mode (see examples)
make dev

# Single query
make query QUERY="Analyze my AWS costs"
```

---

## 🔧 Installation & Setup

### **Prerequisites**
- Python 3.10+
- AWS credentials configured
- `uv` package manager (for MCP servers)

### **Step-by-Step Setup**

#### **1. Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt

# For development
pip install -r requirements_dev.txt
```

#### **2. Setup AWS MCP Servers (Choose One Approach)**

**Option A: Install for Production (Recommended)**
```bash
# Install MCP servers globally (persistent, fast)
make mcp-install

# Check MCP server status
make mcp-check
```

**Option B: Run Directly for Development (No Installation)**
```bash
# Run MCP servers directly (always latest, no installation)
make mcp-run

# Stop MCP servers when done
make mcp-stop
```

**Manual Installation (Alternative)**
```bash
# Install manually
uv tool install awslabs.cost-explorer-mcp-server@latest
uv tool install awslabs.cloudwatch-mcp-server@latest
uv tool install awslabs.aws-pricing-mcp-server@latest

# Or run directly
uvx awslabs.cost-explorer-mcp-server@latest
uvx awslabs.cloudwatch-mcp-server@latest
uvx awslabs.aws-pricing-mcp-server@latest
```

#### **3. Configure AWS Credentials**
```bash
# Method 1: AWS CLI
aws configure

# Method 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Method 3: IAM Role (recommended for production)
# Attach IAM role with required permissions
```

#### **4. Verify Setup**
```bash
# Check project status
make status

# Test MCP connections
make mcp-test
```

---

## 🎯 Running the Agent

### **Interactive Mode (Recommended)**
```bash
make run
```
- **Best for**: Interactive conversations, exploration, complex queries
- **Features**: Full conversation history, context awareness
- **Usage**: Type your questions and get detailed responses

### **Demo Mode**
```bash
make dev
```
- **Best for**: Learning, testing, seeing examples
- **Features**: Pre-defined scenarios, step-by-step examples
- **Usage**: Watch automated demos of key capabilities

### **Query Mode**
```bash
make query QUERY="Your specific question"
```
- **Best for**: Single questions, automation, scripts
- **Features**: One-shot responses, easy integration
- **Usage**: Perfect for CI/CD pipelines or quick lookups

---

## 💡 Usage Examples

### **Cost Analysis Examples**

#### **1. Basic Cost Analysis**
```
👤 User: Analyze my AWS costs for the last 30 days
🤖 Agent: I'll analyze your AWS costs using the Cost Explorer MCP Server...

📊 Cost Analysis Summary (Last 30 Days):
• Total Spend: $1,234.56
• Top Service: EC2 (37% - $456.78)
• Growth: +12.5% vs previous month

🎯 Top Recommendations:
1. Reserved Instances: Save up to $164/month on EC2
2. S3 Intelligent Tiering: Save 68% on infrequent access
3. Rightsize underutilized t3.large instances

💡 Quick Wins:
• Enable Cost Anomaly Detection
• Set up billing alerts at $1,500
• Review 8 idle EBS volumes ($23/month savings)
```

#### **2. Instance Comparison**
```
👤 User: Compare t3.medium vs m5.large for web application
🤖 Agent: I'll compare these instances for web application workloads...

💰 Cost Comparison (us-east-1, 24/7 usage):

t3.medium:
• On-Demand: $30.37/month
• Reserved (1yr): $19.54/month (36% savings)
• Best for: Variable web traffic, burst capability

m5.large:
• On-Demand: $70.08/month  
• Reserved (1yr): $44.90/month (36% savings)
• Best for: Consistent high traffic, memory-intensive apps

🎯 Recommendation: 
Start with t3.medium for cost efficiency. Upgrade to m5.large when:
• CPU utilization consistently >70%
• Memory usage >6GB consistently
• Response time SLA requirements increase
```

#### **3. Multi-Service Analysis**
```
👤 User: Compare RDS vs DynamoDB costs for my database
🤖 Agent: I'll analyze both database options for your use case...

📊 Database Cost Analysis:

RDS (PostgreSQL):
• db.t3.medium: $45.60/month
• Storage (100GB): $11.50/month
• Backup storage: $2.30/month
• Total: $59.40/month

DynamoDB:
• On-demand: $0.25 per million requests
• Storage: $0.25/GB/month
• Estimated: $35-50/month (based on usage)

🎯 Recommendation:
• Use RDS for: Complex queries, ACID compliance, existing SQL skills
• Use DynamoDB for: High-scale, simple queries, serverless architecture
```

### **Infrastructure as Code Examples**

#### **1. Terraform Analysis**
```
👤 User: Analyze my Terraform configuration for best practices
🤖 Agent: I'll analyze your Terraform configuration...

🔍 Terraform Analysis Results:

✅ Good Practices Found:
• Proper resource tagging
• State file management configured
• Variable usage for environment-specific values

⚠️  Issues Found:
• Missing lifecycle rules for critical resources
• No data source validation
• Hardcoded region values

🛠️  Recommendations:
1. Add lifecycle rules to prevent accidental deletion
2. Implement data source validation
3. Use variables for region configuration
4. Add resource dependencies documentation

📋 Generated PR: #123 - Terraform Best Practices Update
```

#### **2. CloudFormation Validation**
```
👤 User: Validate my CloudFormation template
🤖 Agent: I'll validate your CloudFormation template...

✅ CloudFormation Validation Results:

Template Structure: ✅ Valid
Resource Dependencies: ✅ Properly defined
Parameter Validation: ⚠️  Missing constraints
Output Values: ✅ Well documented

🔧 Issues to Fix:
• Add parameter constraints for instance types
• Include resource descriptions
• Add condition functions for environment-specific resources

📋 Generated PR: #124 - CloudFormation Template Improvements
```

### **Security & Compliance Examples**

#### **1. Security Policy Validation**
```
👤 User: Check security policies for my EC2 instances
🤖 Agent: I'll validate your EC2 security policies...

🔒 Security Policy Analysis:

✅ Compliant:
• Security groups properly configured
• IAM roles follow least privilege
• Encryption enabled for EBS volumes

⚠️  Security Issues:
• Public IP addresses without proper restrictions
• Overly permissive security group rules
• Missing VPC flow logs

🛡️  Recommendations:
1. Restrict public IP access to specific CIDR blocks
2. Tighten security group rules (port 22, 80, 443 only)
3. Enable VPC flow logs for monitoring
4. Implement AWS Config for continuous compliance

📋 Generated PR: #125 - Security Policy Hardening
```

#### **2. Compliance Check**
```
👤 User: Check SOC2 compliance for my infrastructure
🤖 Agent: I'll perform a SOC2 compliance assessment...

📋 SOC2 Compliance Assessment:

✅ Access Controls (CC6.1):
• IAM policies properly configured
• Multi-factor authentication enabled
• Regular access reviews scheduled

✅ System Operations (CC7.1):
• CloudWatch monitoring active
• Automated backups configured
• Incident response procedures documented

⚠️  Areas for Improvement:
• Log retention period needs extension (90 days → 1 year)
• Encryption key rotation not automated
• Vulnerability scanning schedule needs definition

📊 Overall Compliance: 85% (Good)
🎯 Action Items: 3 critical, 5 recommended
```

### **GitHub Integration Examples**

#### **1. Automated PR Creation**
```
👤 User: Create a PR with cost optimization recommendations
🤖 Agent: I'll create a pull request with your cost optimizations...

🚀 Pull Request Created: #126 - AWS Cost Optimization Recommendations

📋 Changes Included:
• Reserved Instance recommendations
• S3 lifecycle policy updates
• EBS volume optimization
• Lambda function rightsizing

💰 Estimated Savings: $234/month (18% reduction)
⏱️  Implementation Time: 2-3 hours
🔧 Risk Level: Low (non-breaking changes)

📝 PR Description:
This PR implements cost optimization recommendations identified by the AWS DevOps Agent:
- Convert 5 EC2 instances to Reserved Instances
- Enable S3 Intelligent Tiering for 3 buckets
- Resize 2 over-provisioned Lambda functions
- Clean up 8 unused EBS volumes

All changes are backward compatible and can be applied during maintenance windows.
```

#### **2. Infrastructure Updates**
```
👤 User: Update my infrastructure based on security recommendations
🤖 Agent: I'll create infrastructure updates for security improvements...

🔧 Infrastructure Update PR: #127 - Security Hardening

📋 Changes:
• Update security group rules
• Add VPC flow logs configuration
• Implement AWS Config rules
• Update IAM policies

🛡️  Security Improvements:
• Reduced attack surface by 40%
• Enhanced monitoring capabilities
• Automated compliance checking
• Improved incident response

📝 Implementation Plan:
1. Apply security group changes (5 minutes)
2. Deploy VPC flow logs (10 minutes)
3. Configure AWS Config (15 minutes)
4. Update IAM policies (5 minutes)
5. Test and validate (30 minutes)

Total downtime: < 5 minutes
```

---

## 🛠️ Tool Categories

### **💰 Cost Optimization Tools**
- `get_real_aws_pricing` - Real-time AWS pricing data
- `analyze_cost_optimization_opportunities` - Find cost savings
- `generate_cost_comparison_report` - Compare pricing options
- `calculate_reserved_instance_savings` - Reserved instance analysis
- `get_actual_aws_costs` - Live cost data from Cost Explorer
- `analyze_cost_trends_real` - Cost trend analysis
- `get_rightsizing_recommendations` - Instance rightsizing
- `get_reserved_instance_recommendations` - RI recommendations

### **🏗️ Infrastructure as Code Tools**
- `analyze_terraform_configuration` - Terraform best practices
- `validate_cloudformation_template` - CloudFormation validation
- `scan_infrastructure_drift` - Detect configuration drift
- `generate_iac_best_practices_report` - IaC recommendations

### **🔒 Security & Compliance Tools**
- `validate_security_policies` - Security policy validation
- `check_compliance_standards` - Compliance framework checks
- `generate_compliance_report` - Compliance reporting
- `scan_security_vulnerabilities` - Vulnerability scanning

### **🌐 Multi-Account Tools**
- `list_cross_account_resources` - Cross-account resource discovery
- `execute_cross_account_operation` - Multi-account operations
- `generate_multi_account_report` - Organization-wide reporting
- `monitor_cross_account_compliance` - Cross-account compliance

### **📱 GitHub Integration Tools**
- `create_optimization_pull_request` - Automated PR creation
- `update_iac_via_github` - Infrastructure updates via GitHub
- `list_infrastructure_repositories` - Repository discovery
- `monitor_infrastructure_prs` - PR monitoring and management

---

## 🔧 Advanced Usage

### **Environment Variables**
```bash
# AWS Configuration
export AWS_DEFAULT_REGION=us-east-1
export AWS_PROFILE=production
export BEDROCK_REGION=us-east-1

# Agent Configuration
export STRANDS_MODEL=claude-3.5-sonnet
export LOG_LEVEL=INFO
export DEBUG_MODE=false

# Multi-Account Configuration
export CROSS_ACCOUNT_ROLES=account1:role1,account2:role2
```

### **Custom Queries**
```bash
# Cost analysis for specific service
make query QUERY="Analyze RDS costs for production database"

# Security check for specific resource
make query QUERY="Check security policies for my Lambda functions"

# Compliance assessment
make query QUERY="Perform HIPAA compliance check on my infrastructure"

# Multi-account analysis
make query QUERY="Generate cost report for all accounts in my organization"
```

### **Integration with CI/CD**
```yaml
# GitHub Actions example
- name: AWS Cost Analysis
  run: |
    make query QUERY="Analyze costs for this deployment"
    
- name: Security Validation
  run: |
    make query QUERY="Validate security policies for new resources"
    
- name: Compliance Check
  run: |
    make query QUERY="Check SOC2 compliance for infrastructure changes"
```

### **Automated Reporting**
```bash
# Daily cost report
make query QUERY="Generate daily cost report and send to team"

# Weekly security assessment
make query QUERY="Perform weekly security assessment and create PR"

# Monthly compliance review
make query QUERY="Generate monthly compliance report for audit"
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **1. AWS Credentials Not Found**
```bash
# Error: The security token included in the request is invalid
# Solution: Configure AWS credentials
aws configure
# or
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

#### **2. MCP Servers Not Available**
```bash
# Error: Warning: MCP client not available, using mock data
# Solution: Install MCP servers
make mcp-install
make mcp-check
```

#### **3. Permission Denied**
```bash
# Error: User is not authorized to perform: ce:GetCostAndUsage
# Solution: Update IAM permissions
# Add Cost Explorer permissions to your IAM policy
```

#### **4. Virtual Environment Issues**
```bash
# Error: ModuleNotFoundError: No module named 'strands'
# Solution: Activate virtual environment
source .venv/bin/activate
# or recreate environment
make clean
make setup
```

### **Debug Mode**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
make run

# Check agent status
make status

# Test specific functionality
make mcp-test
```

### **Getting Help**
```bash
# Show all available commands
make help

# Check project status
make status

# View logs
tail -f logs/agent.log
```

---

## 💡 Best Practices

### **1. Cost Optimization**
- **Regular Analysis**: Run cost analysis weekly
- **Reserved Instances**: Plan RI purchases quarterly
- **Rightsizing**: Review instance utilization monthly
- **Cleanup**: Remove unused resources regularly

### **2. Security & Compliance**
- **Continuous Monitoring**: Enable AWS Config and CloudTrail
- **Regular Audits**: Perform security assessments monthly
- **Policy Updates**: Keep security policies current
- **Incident Response**: Have procedures documented and tested

### **3. Infrastructure as Code**
- **Version Control**: Keep all IaC in version control
- **Testing**: Validate templates before deployment
- **Documentation**: Document all infrastructure decisions
- **Automation**: Use CI/CD for infrastructure changes

### **4. Multi-Account Management**
- **Centralized Billing**: Use AWS Organizations
- **Cross-Account Roles**: Implement least privilege access
- **Monitoring**: Set up organization-wide monitoring
- **Compliance**: Ensure consistent policies across accounts

### **5. GitHub Integration**
- **Automated PRs**: Use for non-critical changes
- **Review Process**: Always review generated PRs
- **Testing**: Test changes in development first
- **Documentation**: Document all automated changes

---

## 📞 Support

### **Getting Help**
- **Documentation**: Check this guide and `README_production.md`
- **Issues**: Report bugs and feature requests on GitHub
- **Community**: Join the AWS DevOps community discussions

### **Contributing**
- **Code**: Follow the project's coding standards
- **Testing**: Add tests for new features
- **Documentation**: Update docs for changes
- **PRs**: Submit pull requests for improvements

---

## 🎯 Quick Reference

### **Essential Commands**
```bash
# Setup
make setup                    # Complete setup
make status                   # Check status

# Running
make run                      # Interactive mode
make dev                      # Demo mode
make query QUERY="question"   # Single query

# MCP Management
make mcp-check               # Check MCP servers
make mcp-install             # Install MCP servers
make mcp-test                # Test MCP connections

# Development
make test                    # Run tests
make format                  # Format code
make clean                   # Clean up
```

### **Common Queries**
```bash
# Cost Analysis
"Analyze my AWS costs for the last 30 days"
"Compare EC2 instance types for my workload"
"Find cost optimization opportunities"

# Security
"Check security policies for my infrastructure"
"Perform SOC2 compliance assessment"
"Scan for security vulnerabilities"

# Infrastructure
"Analyze my Terraform configuration"
"Validate my CloudFormation template"
"Check for infrastructure drift"

# Multi-Account
"Generate cost report for all accounts"
"Check compliance across my organization"
"List resources in all accounts"
```

---

**Happy AWS DevOps Automation! 🚀**
