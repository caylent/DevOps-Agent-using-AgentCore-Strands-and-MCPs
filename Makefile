# AWS DevOps Agent - Simplified Makefile
# Focus on running the application with minimal complexity

.PHONY: help run dev setup clean test

# Default target
help: ## Show this help message
	@echo "🚀 AWS DevOps Agent - Available Commands"
	@echo "========================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "💡 Quick Start: make setup && make run"

# =============================================================================
# MAIN COMMANDS (PRIORITIZED)
# =============================================================================

run: ## Run the agent (interactive mode) - MAIN COMMAND
	@echo "🚀 Starting AWS DevOps Agent..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "✅ Using virtual environment: $$VIRTUAL_ENV"; \
		python main.py --mode interactive; \
	else \
		echo "⚠️  No virtual environment detected. Using system Python..."; \
		python3 main.py --mode interactive; \
	fi

dev: ## Run in demo mode
	@echo "🎭 Starting AWS DevOps Agent in demo mode..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python main.py --mode demo; \
	else \
		python3 main.py --mode demo; \
	fi

query: ## Run a single query (usage: make query QUERY="your query")
	@if [ -z "$(QUERY)" ]; then \
		echo "❌ Please provide a query: make query QUERY='your query'"; \
		exit 1; \
	fi
	@echo "🔍 Running query: $(QUERY)"
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python main.py --query "$(QUERY)"; \
	else \
		python3 main.py --query "$(QUERY)"; \
	fi

# =============================================================================
# MCP SERVER MANAGEMENT
# =============================================================================

mcp-check: ## Check if MCP servers are installed
	@echo "🔌 Checking AWS MCP servers..."
	@echo ""
	@if command -v uv >/dev/null 2>&1; then \
		echo "✅ uv is available"; \
		echo ""; \
		echo "Checking installed MCP servers:"; \
		uv tool list 2>/dev/null | grep -E "(cost-explorer|cloudwatch|aws-pricing)" || echo "❌ No AWS MCP servers found"; \
	else \
		echo "❌ uv not available. Install with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
	fi

mcp-install: ## Install AWS MCP servers (recommended for production)
	@echo "🔌 Installing AWS MCP servers (production approach)..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "Installing cost-explorer-mcp-server..."; \
		uv tool install awslabs.cost-explorer-mcp-server@latest || echo "⚠️  Failed to install cost-explorer-mcp-server"; \
		echo "Installing cloudwatch-mcp-server..."; \
		uv tool install awslabs.cloudwatch-mcp-server@latest || echo "⚠️  Failed to install cloudwatch-mcp-server"; \
		echo "Installing aws-pricing-mcp-server..."; \
		uv tool install awslabs.aws-pricing-mcp-server@latest || echo "⚠️  Failed to install aws-pricing-mcp-server"; \
		echo ""; \
		echo "✅ MCP installation completed"; \
		echo "💡 Run 'make mcp-check' to verify installation"; \
	else \
		echo "❌ uv not available. Install with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
		exit 1; \
	fi

mcp-run: ## Run MCP servers directly (recommended for development)
	@echo "🚀 Running AWS MCP servers directly (development approach)..."
	@if command -v uvx >/dev/null 2>&1; then \
		echo "Starting cost-explorer-mcp-server..."; \
		uvx awslabs.cost-explorer-mcp-server@latest & \
		echo "Starting cloudwatch-mcp-server..."; \
		uvx awslabs.cloudwatch-mcp-server@latest & \
		echo "Starting aws-pricing-mcp-server..."; \
		uvx awslabs.aws-pricing-mcp-server@latest & \
		echo ""; \
		echo "✅ MCP servers started in background"; \
		echo "💡 Use 'make mcp-stop' to stop all servers"; \
	else \
		echo "❌ uvx not available. Install with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
		exit 1; \
	fi

mcp-stop: ## Stop all running MCP servers
	@echo "🛑 Stopping MCP servers..."
	@pkill -f "cost-explorer-mcp-server" || true
	@pkill -f "cloudwatch-mcp-server" || true
	@pkill -f "aws-pricing-mcp-server" || true
	@echo "✅ MCP servers stopped"

mcp-test: ## Test MCP server connections
	@echo "🧪 Testing MCP server connections..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python tests/test_mcp_integration.py; \
	else \
		python3 tests/test_mcp_integration.py; \
	fi

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

setup: ## Complete setup: create venv, install deps, install MCP servers
	@echo "🔧 Setting up AWS DevOps Agent..."
	@echo "1️⃣ Creating virtual environment..."
	python3 -m venv .venv
	@echo "2️⃣ Installing dependencies..."
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements_dev.txt
	@echo "3️⃣ Installing AWS MCP servers..."
	@if command -v uvx >/dev/null 2>&1; then \
		echo "Installing MCP servers..."; \
		uv tool install awslabs.cost-explorer-mcp-server@latest || echo "⚠️  Failed to install cost-explorer-mcp-server"; \
		uv tool install awslabs.cloudwatch-mcp-server@latest || echo "⚠️  Failed to install cloudwatch-mcp-server"; \
		uv tool install awslabs.aws-pricing-mcp-server@latest || echo "⚠️  Failed to install aws-pricing-mcp-server"; \
		echo "✅ MCP installation attempt completed"; \
	else \
		echo "⚠️  uvx not available. MCP servers not installed"; \
		echo "💡 Install uvx with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
		echo "💡 Then run: make mcp-install"; \
	fi
	@echo "✅ Setup complete!"
	@echo "💡 Run 'source .venv/bin/activate' then 'make run'"

install: ## Install dependencies only (if venv exists)
	@if [ -f .venv/bin/activate ]; then \
		echo "📦 Installing dependencies in virtual environment..."; \
		.venv/bin/pip install --upgrade pip; \
		.venv/bin/pip install -r requirements.txt; \
		.venv/bin/pip install -r requirements_dev.txt; \
		echo "✅ Dependencies installed"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

# =============================================================================
# DEVELOPMENT & TESTING
# =============================================================================

test: ## Run all tests
	@echo "🧪 Running tests..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python -m pytest tests/ -v; \
	else \
		python3 -m pytest tests/ -v; \
	fi

test-terraform: ## Run Terraform tests
	@echo "🏗️ Running Terraform tests..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python -m pytest tests/terraform/ -v; \
	else \
		python3 -m pytest tests/terraform/ -v; \
	fi

format: ## Format code
	@echo "🎨 Formatting code..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		black src/ tests/ --line-length=100; \
		isort src/ tests/ --profile black; \
	else \
		black src/ tests/ --line-length=100; \
		isort src/ tests/ --profile black; \
	fi
	@echo "✅ Code formatted"

# =============================================================================
# DEPLOYMENT
# =============================================================================

deploy: ## Deploy to Bedrock Agent Core
	@echo "🚀 Deploying to Bedrock Agent Core..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python deployment/bedrock/app.py; \
	else \
		python3 deployment/bedrock/app.py; \
	fi

# =============================================================================
# UTILITIES
# =============================================================================

clean: ## Clean up temporary files and virtual environment
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf .venv/
	@echo "✅ Cleanup complete"

status: ## Show project status
	@echo "📊 AWS DevOps Agent - Project Status"
	@echo "===================================="
	@echo ""
	@if [ -f .venv/bin/activate ]; then \
		echo "✅ Virtual environment: .venv/"; \
	else \
		echo "❌ Virtual environment: Not created"; \
	fi
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "✅ Virtual environment: Active ($$VIRTUAL_ENV)"; \
	else \
		echo "⚠️  Virtual environment: Not active"; \
	fi
	@echo ""
	@echo "🔌 MCP Servers:"
	@if command -v uv >/dev/null 2>&1; then \
		uv tool list 2>/dev/null | grep -E "(cost-explorer|cloudwatch|aws-pricing)" >/dev/null && echo "✅ AWS MCP servers installed" || echo "❌ AWS MCP servers not installed"; \
	else \
		echo "❌ uv not available (needed for MCP servers)"; \
	fi
	@echo ""
	@echo "🏗️  Infrastructure Tools:"
	@if command -v terraform >/dev/null 2>&1; then \
		echo "✅ Terraform CLI: $(shell terraform version -json | jq -r '.terraform_version' 2>/dev/null || echo 'Available')"; \
	else \
		echo "❌ Terraform CLI: Not installed (optional for Terraform analysis)"; \
	fi
	@if command -v cdk >/dev/null 2>&1; then \
		echo "✅ AWS CDK CLI: $(shell cdk --version 2>/dev/null || echo 'Available')"; \
	else \
		echo "❌ AWS CDK CLI: Not installed (optional for CDK analysis)"; \
	fi
	@echo ""
	@echo "📁 Project Structure:"
	@find . -type d -not -path "./.git*" -not -path "./bkp*" -not -path "./__pycache__*" | head -8
	@echo ""
	@echo "🐍 Python Files: $(shell find . -name "*.py" -not -path "./bkp*" -not -path "./.git*" | wc -l | tr -d ' ')"

# =============================================================================
# EXAMPLES
# =============================================================================

example-cost: ## Run cost analysis example
	@echo "💰 Running cost analysis example..."
	make query QUERY="Analyze my AWS costs and provide optimization recommendations"

example-iac: ## Run IaC analysis example
	@echo "🏗️ Running IaC analysis example..."
	make query QUERY="Analyze my Terraform configuration for security and cost optimization"

example-compliance: ## Run compliance check example
	@echo "🔒 Running compliance check example..."
	make query QUERY="Check my AWS infrastructure for SOC2 compliance"

example-cdk: ## Run CDK analysis example
	@echo "🏗️ Running CDK analysis example..."
	make query QUERY="Analyze my CDK project for optimization opportunities and security issues"

example-terraform: ## Run Terraform analysis example
	@echo "🏗️ Running Terraform analysis example..."
	make query QUERY="Analyze my Terraform project for cost optimization and security issues"

example-security: ## Run AWS security analysis example
	@echo "🛡️ Running AWS security analysis example..."
	@python docs/demos/demo_aws_security_analysis.py

example-security-hub: ## Run Security Hub focused demo
	@echo "🔍 Running Security Hub focused demo..."
	@python docs/demos/demo_security_hub_simple.py

example-trusted-advisor: ## Run Trusted Advisor focused demo
	@echo "💡 Running Trusted Advisor focused demo..."
	@python docs/demos/demo_trusted_advisor_simple.py

example-cdk-pricing: ## Run CDK pricing focused demo
	@echo "💰 Running CDK pricing focused demo..."
	@python docs/demos/demo_cdk_pricing_simple.py

example-report: ## Run document generation example
	@echo "📄 Running document generation example..."
	make query QUERY="Generate a cost analysis report for my AWS infrastructure"