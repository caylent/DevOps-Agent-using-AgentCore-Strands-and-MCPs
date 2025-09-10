# AWS DevOps Agent - Modern Python Architecture

🚀 **Production-ready AWS DevOps automation agent** built with modern Python best practices, using Strands framework + Bedrock Agent Core deployment, integrating official AWS MCP servers for real-time optimization, compliance, and infrastructure management.

## 📚 Essential Documentation

### **🚀 Get Started**
- ⚡ **[Quick Setup](docs/QUICK_SETUP.md)** - Get the agent running in 3 minutes with step-by-step installation
- 📖 **[User Manual](docs/USER_MANUAL.md)** - Complete guide to using the AWS DevOps Agent with detailed examples and workflows
- 🚀 **[App Info](docs/APP_INFO.md)** - Comprehensive overview of features, architecture, and implementation status

## 🎯 What This Does

This agent transforms AWS DevOps operations into intelligent, automated processes:

- **Real-time cost optimization** with AWS Pricing API integration
- **Infrastructure as Code analysis** for Terraform and CloudFormation  
- **Security and compliance validation** (SOC2, HIPAA, PCI-DSS, ISO27001)
- **Multi-account AWS operations** across organizations
- **GitHub MCP integration** with repository management and PR automation
- **Document generation** with automatic report creation in organized folders

## 🏗️ Architecture

```
Strands Framework          →         Bedrock Agent Core
┌─────────────────────────┐          ┌─────────────────────────┐
│ AWS DevOps Agent        │    →     │ AWS Bedrock Runtime     │
│ ├── Cost Optimization   │          │ ├── Claude Sonnet 4     │
│ ├── IaC Analysis        │          │ ├── HTTP API Service    │
│ ├── Compliance Check    │          │ └── /invocations        │
│ ├── Multi-Account Mgmt  │          └─────────────────────────┘
│ └── GitHub Automation   │          
└─────────────────────────┘          
              │
    ┌─────────▼──────────┐
    │    AWS MCP Servers │
    │ ├── Pricing        │
    │ ├── DynamoDB       │
    │ ├── Cost Explorer  │
    │ ├── Terraform      │
    │ ├── CloudWatch     │
    │ └── GitHub         │
    └────────────────────┘
```

## 📁 Project Structure

```
strands-bedrock-mcp-devops-agent/
├── main.py                          # 🚀 Main entry point
├── pyproject.toml                   # 📦 Modern Python configuration  
├── requirements.txt                 # 📋 Production dependencies
├── requirements_dev.txt             # 🔧 Development dependencies
├── .env.example                     # 🔐 Environment template
│
├── src/aws_devops_agent/           # 📂 Main package (modern src/ layout)
│   ├── __init__.py
│   ├── main.py                     # Core agent implementation
│   ├── config/                     # ⚙️ Configuration management
│   │   ├── __init__.py
│   │   └── app_config.py
│   ├── tools/                      # 🛠️ Organized AWS DevOps tools
│   │   ├── __init__.py
│   │   ├── aws_cost/              # 💰 Cost optimization
│   │   │   ├── __init__.py
│   │   │   ├── pricing.py         # AWS pricing analysis
│   │   │   ├── optimization.py    # Cost Explorer integration
│   │   │   ├── resources.py       # Live resource scanning
│   │   │   └── multi_account.py   # Multi-account operations
│   │   ├── aws_iac/               # 🏗️ Infrastructure as Code
│   │   │   ├── __init__.py
│   │   │   └── terraform.py       # Terraform/CloudFormation
│   │   ├── aws_compliance/        # 🔒 Security & compliance
│   │   │   ├── __init__.py
│   │   │   └── security.py        # SOC2, HIPAA, PCI-DSS, ISO27001
│   │   └── github/                # 📱 GitHub integration
│   │       ├── __init__.py
│   │       └── integration.py     # PR automation
│   └── mcp_clients/               # 🔌 MCP client integration
│       ├── __init__.py
│       ├── mcp_client.py          # Unified MCP client
│       ├── aws_mcp_client.py      # AWS-specific client
│       ├── strands_mcp_client.py  # Strands-native client
│       └── github_mcp_client.py   # GitHub MCP client
│
├── deployment/bedrock/             # 🚀 Production deployment
│   └── app.py                      # Bedrock Agent Core app
├── scripts/                       # 🔧 Setup and utility scripts
│   └── setup.sh
├── tests/                         # 🧪 Organized testing
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── fixtures/                  # Test fixtures
└── docs/                          # 📚 Documentation
    ├── APP_INFO.md
    └── APP_USAGE.md               # 📖 Comprehensive usage guide
```

## 🚀 Quick Start

> **📖 For detailed setup instructions, see [Quick Setup Guide](docs/QUICK_SETUP.md)**

### Prerequisites
- Python 3.10+
- AWS credentials configured
- Strands SDK access
- uv package manager

### **🚀 EASY WAY (Recommended)**
```bash
# Complete setup and run in one command
make setup
source .venv/bin/activate
make run
```

### **🔧 Manual Installation**
```bash
# 1. Clone repository
git clone https://github.com/your-org/strands-bedrock-mcp-devops-agent
cd strands-bedrock-mcp-devops-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install MCP Servers
make mcp-install

# 4. Configure environment
cp .env.example .env
# Edit .env with your AWS credentials

# 5. Run the agent
python main.py --mode interactive
```

### **Available Commands**
```bash
# Main Commands
make run               # Start interactive mode - MAIN COMMAND
make dev               # Start demo mode
make query QUERY="your query"  # Single query

# Setup & Installation
make setup             # Complete setup: create venv, install deps, install MCP servers
make install           # Install dependencies only (if venv exists)

# Development & Testing
make test              # Run all tests
make format            # Format code
```

## 💬 Example Conversations

### Cost Analysis
```
👤 analyze
🤖 I'll analyze your AWS infrastructure costs using the Cost Explorer MCP Server...

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

### Instance Comparison
```
👤 compare t3.medium,m5.large for web application
🤖 I'll compare these instances for web application workloads...

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

## 🛠️ Advanced Usage

### Multi-Account Analysis
```python
# Analyze costs across multiple AWS accounts
agent = DevOpsAgent()
await agent.analyze_infrastructure_costs(account_id="123456789012")
```

### Custom Pricing Queries
```python
# Compare pricing across regions
response = await agent.chat("""
Compare EC2 costs between us-east-1, eu-west-1, and ap-southeast-1 
for a m5.large instance running 24/7. Include data transfer costs.
""")
```

## 🚀 Deployment

### Local Development
```bash
# Development mode
python main.py --mode interactive

# Run tests
pytest tests/

# Code formatting
black src/ tests/
isort src/ tests/

# Type checking  
mypy src/
```

### Production Deployment
```bash
# Install as package
pip install -e .

# Use CLI command
aws-devops-agent --mode interactive

# Bedrock Agent Core deployment
python deployment/bedrock/app.py
```

## 🔧 Configuration

### Environment Variables
```bash
export AWS_DEFAULT_REGION=us-east-1
export AWS_PROFILE=default
export BEDROCK_REGION=us-east-1
```

### Required AWS Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetForecast",
                "cloudwatch:GetMetricData",
                "cloudwatch:DescribeAlarms",
                "logs:StartQuery",
                "logs:GetQueryResults",
                "pricing:GetProducts",
                "pricing:DescribeServices"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🧪 Testing

### Test Results
- ✅ **Strands SDK**: Installed and functioning (v1.7.0)
- ✅ **Bedrock Agent Core**: Available (v0.1.2)  
- ✅ **MCP Protocol**: Working (v1.13.1)
- ✅ **AWS Configuration**: Loaded correctly (us-east-1)
- ✅ **All Tools**: Cost, Compliance, Multi-Account, GitHub, IaC tools ready

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/unit/
pytest tests/integration/

# Interactive testing
python tests/interactive_test.py
```

## 🤝 Contributing

This is a demonstration project for AWS re:Invent presentation. The architecture shows how to combine:
- **Modern Python practices** with industry standards
- **Strands SDK** for AI orchestration
- **Official AWS MCP Servers** for real-time data
- **Bedrock Agent Core** for sophisticated reasoning
- **Clean architecture** for maintainable DevOps operations

## 📋 Requirements

- **Python 3.10+**
- **Strands SDK** (requires access)
- **AWS credentials** configured
- **uv package manager** (installs automatically)

## 📚 Additional Documentation

### **Usage & Configuration**
- 🎯 **[App Usage](docs/APP_USAGE.md)** - Detailed usage examples, tool categories, and advanced workflows
- 🌍 **[Environment Variables](docs/ENVIRONMENT_VARIABLES.md)** - Complete configuration guide for all environment variables
- 🔒 **[Safety Guidelines](docs/SAFETY_GUIDELINES.md)** - Critical security measures and safety protocols for production use

### **Deployment & Operations**
- 🚀 **[AgentCore Deployment Guide](docs/AGENTCORE_DEPLOYMENT_GUIDE.md)** - Step-by-step Bedrock AgentCore deployment with safety measures
- ✅ **[Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md)** - Production deployment verification checklist
- 📄 **[Document Generation](docs/DOCUMENT_GENERATION.md)** - Automatic report generation and file organization

### **Analysis & Integration**
- 🛡️ **[AWS Security Analysis](docs/AWS_SECURITY_ANALYSIS.md)** - Real-time security analysis using AWS Security Hub, Config, and Inspector
- 🏗️ **[Terraform Analysis](docs/TERRAFORM_ANALYSIS.md)** - Comprehensive Terraform project analysis and optimization
- 📦 **[CDK Analysis](docs/CDK_ANALYSIS.md)** - AWS Cloud Development Kit project analysis and cost optimization
- 🐙 **[GitHub MCP Integration](docs/GITHUB_MCP_INTEGRATION.md)** - Complete GitHub integration for PR automation and repository management
- 🔧 **[GitHub MCP Quick Reference](docs/GITHUB_MCP_QUICK_REFERENCE.md)** - Essential commands and quick setup for GitHub MCP server

### **Demos & Examples**
- 📁 **[Demos](docs/demos/)** - Interactive demo scripts and examples for testing agent capabilities

## 🔗 Official AWS MCP Servers

- [AWS Pricing MCP Server](https://awslabs.github.io/mcp/servers/aws-pricing-mcp-server/)
- [AWS DynamoDB MCP Server](https://awslabs.github.io/mcp/servers/dynamodb-mcp-server/) 
- [Full AWS MCP Documentation](https://awslabs.github.io/mcp/)

---

## 📄 License

MIT License

Copyright (c) 2024 AWS DevOps Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

**🎉 Ready for production!** 

This agent provides **real AWS data integration** via official MCP servers, not simulated responses. Always emphasize data authenticity and provide specific, actionable recommendations with cost implications.