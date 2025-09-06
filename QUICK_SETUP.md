# ⚡ QUICK SETUP - Modern AWS DevOps Agent Ready in 3 Minutes

## 1️⃣ Install Dependencies
```bash
# Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
pip install -r requirements.txt

# For development (optional)
pip install -r requirements_dev.txt
```

## 2️⃣ Setup AWS MCP Servers (Choose One)

**Option A: Install for Production (Recommended)**
```bash
# Install MCP servers globally (persistent, fast)
make mcp-install

# Check status
make mcp-check
```

**Option B: Run Directly for Development**
```bash
# Run MCP servers directly (no installation, always latest)
make mcp-run

# Stop when done
make mcp-stop
```

## 3️⃣ Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Configure AWS credentials (choose one method):

# Method 1: AWS CLI
aws configure

# Method 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret  
export AWS_DEFAULT_REGION=us-east-1

# Method 3: Edit .env file
# Edit .env file with your credentials
```

## 3.5️⃣ CDK Setup (Optional - for CDK Analysis)
```bash
# Install AWS CDK CLI (if not already installed)
npm install -g aws-cdk

# Verify CDK installation
cdk --version

# Bootstrap CDK (if using CDK for the first time in your AWS account)
cdk bootstrap
```

## 4️⃣ Test MCP Integration
```bash
python tests/test_mcp_integration.py
```

## 5️⃣ Run the Agent

### 🚀 **EASY WAY (Recommended)**
```bash
# Complete setup and run (BEST)
make setup
source .venv/bin/activate
make run

# Or step by step
make setup            # Create venv, install deps, install MCP servers
source .venv/bin/activate  # Activate venv
make run              # Start the agent
```

### 🔧 **Manual Way**
```bash
# Development mode
python main.py --mode interactive

# Or using module syntax
python -m src.aws_devops_agent.main --mode demo

# Production installation
pip install -e .
aws-devops-agent --mode interactive
```

## ✅ Done! 
Your modern AWS DevOps Agent is ready with:
- ✅ **Modern Python structure** (src/ layout, pyproject.toml)
- ✅ **Real AWS MCP integration** (Cost Explorer, CloudWatch, Pricing)
- ✅ **Organized tools** (cost, IaC, compliance, GitHub, CDK)
- ✅ **CDK Analysis** (project analysis, synthesis, optimization)
- ✅ **Production deployment** (Bedrock Agent Core)
- ✅ **Development tools** (pytest, black, mypy)

## 📖 Next Steps
- **Learn how to use it**: See [docs/APP_USAGE.md](docs/APP_USAGE.md) for comprehensive examples
- **Explore capabilities**: Run `make dev` to see demo scenarios
- **Start optimizing**: Run `make run` and ask about your AWS costs

## 🚀 Available Commands

### **Makefile Commands (Simplified)**
```bash
# Main Commands (PRIORITIZED)
make run               # Start interactive mode - MAIN COMMAND
make dev               # Start demo mode
make query QUERY="your query"  # Single query

# Setup & Installation
make setup             # Complete setup: create venv, install deps, install MCP servers
make install           # Install dependencies only (if venv exists)

# Development & Testing
make test              # Run all tests
make format            # Format code

# MCP Server Management
make mcp-check         # Check if MCP servers are installed
make mcp-install       # Install AWS MCP servers
make mcp-test          # Test MCP server connections

# Deployment & Utilities
make deploy            # Deploy to Bedrock Agent Core
make clean             # Clean up temporary files and virtual environment
make status            # Show project status

# Examples
make example-cost      # Run cost analysis example
make example-iac       # Run IaC analysis example
make example-compliance # Run compliance check example
```

### **Manual Commands**
```bash
# Interactive mode
python main.py --mode interactive

# Demo scenarios
python main.py --mode demo

# Single query
python main.py --query "Analyze AWS costs for my infrastructure"

# Production mode
aws-devops-agent --mode interactive
```

## 🔧 IAM Permissions Needed:
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

## 🎯 What's New
- **No version numbers** in filenames (maintainable)
- **Domain-organized tools** (easy to navigate)
- **Modern Python packaging** (industry standard)
- **Multiple entry points** (development & production)
- **Comprehensive testing** (unit, integration, fixtures)

That's it! 🎉