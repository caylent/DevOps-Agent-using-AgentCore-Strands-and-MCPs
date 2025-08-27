# AWS DevOps Agent with Strands, Bedrock and Official MCP Servers

Cloud operations optimization agent that transforms DevOps tasks into intelligent operations. Analyzes infrastructure, optimizes costs, and validates compliance using natural language through AWS MCP Servers, Strands SDK, and Bedrock Agent Core.

## 🎯 Key Features

### Cost Optimization
- **Real-time pricing queries**: "What's the cost of m5.large in us-east-1?"
- **Multi-service cost analysis**: Combines pricing + usage + optimization in one query
- **Executive reporting**: Generates C-level cost summaries with actionable insights
- **Cross-account operations**: Scales analysis across multiple AWS accounts

### Infrastructure Intelligence
- **Natural language operations**: Ask complex questions in plain English
- **Automated recommendations**: AI-powered cost and security optimization
- **Compliance validation**: Checks best practices across services
- **Multi-region analysis**: Compare costs and configurations across regions

### Integration Benefits
- **Official AWS MCP Servers**: Real-time data via official AWS APIs
- **Strands SDK**: Advanced AI orchestration with tool coordination  
- **Bedrock Agent Core**: Claude Sonnet 4 for sophisticated reasoning
- **No rigid pipelines**: Conversational, adaptive workflows

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Natural Language Interface             │
│              (CLI / API / Slack / Teams)               │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│            Strands Agent Orchestrator                   │
│  - Bedrock Agent Core (Claude Sonnet 4)               │
│  - Multi-tool coordination                             │
│  - Context management                                  │
└─────────┬───────┬───────┬───────┬───────┬───────┬───────┘
          │       │       │       │       │       │
┌─────────▼┐ ┌────▼───┐ ┌─▼────┐ ┌▼────┐ ┌▼────┐ ┌▼─────┐
│AWS MCP   │ │Cost    │ │IaC   │ │Comp │ │Git  │ │Report│
│Pricing   │ │Explorer│ │Scan  │ │Check│ │Ops  │ │Gen   │
│Server    │ │MCP     │ │Tools │ │Tools│ │MCP  │ │Tools │
└──────────┘ └────────┘ └──────┘ └─────┘ └─────┘ └──────┘
          │       │       │       │       │       │
          ▼       ▼       ▼       ▼       ▼       ▼
    ┌─────────────────────────────────────────────────┐
    │              AWS APIs & Services                │
    │  Pricing • Cost Explorer • CloudFormation      │
    │  EC2 • S3 • RDS • CloudWatch • CodeCommit      │
    └─────────────────────────────────────────────────┘
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

# 2. Run setup script
python setup.py

# 3. Install AWS MCP Servers
uv tool install aws-pricing-mcp-server
# More servers as they become available:
# uv tool install aws-cost-explorer-mcp-server
# uv tool install aws-cloudwatch-mcp-server
```

### Basic Usage

```bash
# Start the agent
python devops_agent.py

# Available commands:
analyze                        # Full cost analysis
compare t3.medium,m5.large    # Compare instance costs  
pricing EC2 m5.large          # Get specific pricing
chat                          # Natural language conversation
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

### Files Structure
```
strands-bedrock-mcp-devops-agent/
├── devops_agent.py           # Main agent implementation
├── mcp_tools/                # MCP integration layer
│   ├── mcp_client.py        # MCP client for AWS servers
│   └── aws_mcp_tools.py     # Strands tools using MCP
├── example_usage.py          # Demo and examples
├── setup.py                  # Installation script
├── requirements.txt          # Dependencies
└── goal                      # Project goals and architecture
```

## 🤝 Contributing

This is a demonstration project for AWS re:Invent presentation. The architecture shows how to combine:
- **Strands SDK** for AI orchestration
- **Official AWS MCP Servers** for real-time data
- **Bedrock Agent Core** for sophisticated reasoning
- **Natural language interfaces** for DevOps operations