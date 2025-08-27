#!/bin/bash
# Production Installation Script
# Clean setup for AWS DevOps Agent

set -e

echo "🚀 AWS DevOps Agent - Production Installation"
echo "=============================================="

# Check dependencies
echo "🔍 Checking dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.10+ required"
    exit 1
fi
echo "✅ Python 3 found"

# Check uv
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "✅ uv package manager ready"

# Install AWS MCP Servers
echo "🌩️ Installing official AWS MCP servers..."

echo "   Installing AWS Pricing MCP server..."
if uv tool install awslabs.aws-pricing-mcp-server@latest; then
    echo "   ✅ AWS Pricing MCP server installed"
else
    echo "   ⚠️ AWS Pricing MCP server installation failed"
fi

echo "   Installing AWS DynamoDB MCP server..."
if uv tool install awslabs.dynamodb-mcp-server@latest; then
    echo "   ✅ AWS DynamoDB MCP server installed"
else
    echo "   ⚠️ AWS DynamoDB MCP server installation failed"
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if [ -f "$HOME/.aws/credentials" ] || [ -n "$AWS_ACCESS_KEY_ID" ]; then
    echo "✅ AWS credentials found"
else
    echo "⚠️ AWS credentials not found"
    echo "   Run: aws configure"
    echo "   Or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
fi

# Installation summary
echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Install Strands SDK (requires access)"
echo "2. Configure AWS credentials if not done"
echo "3. Run: python3 aws_devops_agent.py"
echo ""
echo "For demo: python3 aws_devops_agent.py demo"