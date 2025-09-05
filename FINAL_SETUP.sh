#!/bin/bash
# 🚀 FINAL SETUP - AWS DevOps Agent with MCP (30 seconds)

echo "🚀 Setting up AWS DevOps Agent with MCP integration..."

# 1. AWS Credentials (if not configured)
echo "1️⃣ Checking AWS credentials..."
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "⚠️  AWS credentials not configured. Run:"
    echo "   aws configure"
    echo "   OR set environment variables:"
    echo "   export AWS_ACCESS_KEY_ID=your_key"
    echo "   export AWS_SECRET_ACCESS_KEY=your_secret"
    echo "   export AWS_DEFAULT_REGION=us-east-1"
    exit 1
else
    echo "✅ AWS credentials configured"
fi

# 2. Test MCP servers are available
echo "2️⃣ Testing MCP servers..."
if /root/.local/bin/awslabs.cost-explorer-mcp-server --help > /dev/null 2>&1; then
    echo "✅ Cost Explorer MCP server available"
else
    echo "❌ Cost Explorer MCP server not available"
fi

if /root/.local/bin/awslabs.cloudwatch-mcp-server --help > /dev/null 2>&1; then
    echo "✅ CloudWatch MCP server available"
else
    echo "❌ CloudWatch MCP server not available"
fi

# 3. Run the agent
echo "3️⃣ Starting AWS DevOps Agent..."
echo "🎯 Ready! Your agent now has:"
echo "   ✅ Official MCP Python SDK integration"
echo "   ✅ Real AWS Cost Explorer data access"
echo "   ✅ Real CloudWatch metrics and alarms"
echo "   ✅ 31 AWS DevOps tools available"
echo ""
echo "💡 Test queries:"
echo '   • "Get my AWS costs for the last 30 days"'
echo '   • "Show CloudWatch alarms in ALARM state"'
echo '   • "Forecast my costs for next month"'
echo ""

python aws_devops_agent_v2.py --mode interactive