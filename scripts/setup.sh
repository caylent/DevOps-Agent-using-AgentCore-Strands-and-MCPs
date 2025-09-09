#!/bin/bash
set -e

echo "🔧 Setting up virtual environment..."

# Create venv with --system-site-packages to avoid externally-managed error
python3 -m venv --system-site-packages .venv

# Activate venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements-production.txt

echo "📦 Installing AWS MCP servers..."
uv tool install awslabs.cost-explorer-mcp-server@latest
uv tool install awslabs.cloudwatch-mcp-server@latest
uv tool install awslabs.aws-pricing-mcp-server@latest
uv tool install awslabs.terraform-mcp-server@latest
uv tool install awslabs.dynamodb-mcp-server@latest
# Note: GitHub MCP server requires Docker (ghcr.io/github/github-mcp-server)

echo "✅ Setup complete! Run: source .venv/bin/activate"