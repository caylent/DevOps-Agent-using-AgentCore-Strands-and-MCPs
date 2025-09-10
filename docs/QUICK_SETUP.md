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

## 2️⃣ Setup MCP Servers (Choose One)

**Option A: Install for Production (Recommended)**
```bash
# Install MCP servers globally (AWS + GitHub)
make mcp-install

# Check status
make mcp-check
```

**GitHub MCP Configuration (Optional):**
```bash
# Add GitHub token for repository management
echo "GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here" >> src/aws_devops_agent/config/.env

# Test GitHub connectivity
make github-test-connectivity REPO=octocat/Hello-World
```

**Option B: Run Directly for Development**
```bash
# Run MCP servers directly (no installation, always latest)
make mcp-run

# Stop when done
make mcp-stop
```

## 3️⃣ Configure Environment

**For AgentCore Deployment (Production):**
```bash
# Create production environment
make agentcore-env-prod

# Validate configuration
make agentcore-validate
```

**For Development:**
```bash
# Create development environment
make agentcore-env-dev

# Or copy environment template
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
# Development mode (requires virtual environment)
source .venv/bin/activate
PYTHONPATH=src python main.py --mode interactive

# Demo mode
source .venv/bin/activate
PYTHONPATH=src python main.py --mode demo

# Single query
source .venv/bin/activate
PYTHONPATH=src python main.py --query "your query here"
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
make install           # Alias for setup (same as make setup)
make clean             # Clean up temporary files and virtual environment
make status            # Show project status

# MCP Server Management
make mcp-check         # Check if MCP servers are installed (AWS + GitHub)
make mcp-install       # Install AWS MCP servers + GitHub MCP server
make mcp-test          # Test MCP server connections

# Development & Testing
make test              # Run core tests (unit + document generation)
make test-integration  # Run integration tests (requires GitHub config)
make format            # Format code

# Examples & Demos
make example TYPE=cost # Run cost analysis example
make example TYPE=iac  # Run IaC analysis example
make example TYPE=compliance # Run compliance check example
make example TYPE=github # Test GitHub connectivity

# AgentCore Deployment (Production)
make agentcore-configure # Configure AgentCore for deployment
make agentcore-deploy    # Deploy to Bedrock AgentCore (PRODUCTION)
make agentcore-test      # Test deployed AgentCore agent
```

### **Manual Commands (Advanced)**
```bash
# Interactive mode (requires virtual environment)
source .venv/bin/activate
PYTHONPATH=src python main.py --mode interactive

# Demo scenarios
source .venv/bin/activate
PYTHONPATH=src python main.py --mode demo

# Single query
source .venv/bin/activate
PYTHONPATH=src python main.py --query "Analyze AWS costs for my infrastructure"

# Run without account selection
source .venv/bin/activate
PYTHONPATH=src python main.py --mode interactive --no-account-selection
```

## 🚀 AgentCore Deployment (Production)

### **Quick AgentCore Setup**
```bash
# 1. Validate environment
make agentcore-validate

# 2. Test locally
make agentcore-test-local

# 3. Build Docker image
make agentcore-build

# 4. Deploy to production (with human verification)
make agentcore-deploy
```

### **AgentCore Monitoring**
```bash
# Health checks
make agentcore-health       # Check health status
make agentcore-metrics      # Get metrics

# Monitoring
make agentcore-status       # Deployment status
make agentcore-logs         # View logs
make agentcore-monitor      # Performance monitoring
```

### **AgentCore Configuration Files**
- `deployment/bedrock/app.py` - Main application
- `deployment/bedrock/Dockerfile` - Container config
- `deployment/bedrock/.bedrock_agentcore.yaml` - AgentCore config
- `deployment/bedrock/iam-policy.json` - IAM permissions
- `deployment/bedrock/env.example` - Environment template

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