# AWS DevOps Agent - Strands + Bedrock Agent Core

🚀 **Production-ready AWS DevOps automation agent** using Strands framework with Bedrock Agent Core deployment, integrating official AWS MCP servers for real-time optimization, compliance, and infrastructure management.

## 🎯 What This Does

This agent transforms AWS DevOps operations into intelligent, automated processes:

- **Real-time cost optimization** with AWS Pricing API integration
- **Infrastructure as Code analysis** for Terraform and CloudFormation  
- **Security and compliance validation** (SOC2, HIPAA, PCI-DSS, ISO27001)
- **Multi-account AWS operations** across organizations
- **Automated GitHub PR generation** for infrastructure improvements

## ✅ Implementation Status

**AGENT FEATURES:**
- ✅ **Strands + Bedrock Agent Core** integration with proper configuration
- ✅ **AWS Cost Optimization Tools** with real-time pricing via MCP
- ✅ **IaC Analysis Tools** for Terraform and CloudFormation validation
- ✅ **Security & Compliance Tools** supporting major standards
- ✅ **Multi-Account Management** for organization-wide operations  
- ✅ **GitHub Integration** with automated PR generation
- ✅ **Comprehensive Testing** with interactive test framework
- ✅ **Production Deployment** ready for Bedrock Agent Core

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
    └── APP_INFO.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- AWS credentials configured
- Strands SDK access
- uv package manager

### Installation

```bash
# 1. Clone repository
git clone https://github.com/your-org/strands-bedrock-mcp-devops-agent
cd strands-bedrock-mcp-devops-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install AWS MCP Servers
uvx install awslabs.cost-explorer-mcp-server@latest
uvx install awslabs.cloudwatch-mcp-server@latest
uvx install awslabs.aws-pricing-mcp-server@latest

# 4. Configure environment
cp .env.example .env
# Edit .env with your AWS credentials
```

### Basic Usage

```bash
# Start the agent (development)
python main.py --mode interactive

# Or using module syntax
python -m src.aws_devops_agent.main --mode demo

# Production installation
pip install -e .
aws-devops-agent --mode interactive

# Available modes:
# --mode interactive    # Interactive chat mode
# --mode demo          # Run demo scenarios
# --query "your query" # Single query mode
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
python devops_agent.py
```

### Example Demo
```bash
python example_usage.py
```

## 🔧 Configuration

### Environment Variables
```bash
export AWS_DEFAULT_REGION=us-east-1
export AWS_PROFILE=default
export BEDROCK_REGION=us-east-1
```

### Modern Python Structure
```
strands-bedrock-mcp-devops-agent/
├── main.py                   # Main entry point
├── pyproject.toml            # Modern Python configuration
├── requirements.txt          # Production dependencies
├── requirements_dev.txt      # Development dependencies
├── src/aws_devops_agent/     # Main package (src/ layout)
│   ├── main.py              # Core agent implementation
│   ├── config/              # Configuration management
│   ├── tools/               # Organized AWS DevOps tools
│   └── mcp_clients/         # MCP integration layer
├── deployment/bedrock/       # Production deployment
├── scripts/                  # Setup and utility scripts
├── tests/                   # Organized testing structure
└── docs/                    # Documentation
```

## 🤝 Contributing

This is a demonstration project for AWS Argentina Community Day presentation. The architecture shows how to combine:
- **Strands SDK** for AI orchestration
- **Official AWS MCP Servers** for real-time data
- **Bedrock Agent Core** for sophisticated reasoning
- **Natural language interfaces** for DevOps operations