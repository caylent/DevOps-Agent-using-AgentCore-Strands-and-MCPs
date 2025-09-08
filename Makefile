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

run-no-account-selection: ## Run the agent without interactive account selection
	@echo "🚀 Starting AWS DevOps Agent (no account selection)..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		echo "✅ Using virtual environment: $$VIRTUAL_ENV"; \
		python main.py --mode interactive --no-account-selection; \
	else \
		echo "⚠️  No virtual environment detected. Using system Python..."; \
		python3 main.py --mode interactive --no-account-selection; \
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
		uv tool list 2>/dev/null | grep -E "(cost-explorer|cloudwatch|aws-pricing|terraform|dynamodb)" || echo "❌ No AWS MCP servers found"; \
		echo "Note: GitHub MCP server requires Docker (ghcr.io/github/github-mcp-server)"; \
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
		echo "Installing terraform-mcp-server..."; \
		uv tool install awslabs.terraform-mcp-server@latest || echo "⚠️  Failed to install terraform-mcp-server"; \
		echo "Installing dynamodb-mcp-server..."; \
		uv tool install awslabs.dynamodb-mcp-server@latest || echo "⚠️  Failed to install dynamodb-mcp-server"; \
		echo "Note: GitHub MCP server requires Docker (ghcr.io/github/github-mcp-server)"; \
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
		echo "Starting terraform-mcp-server..."; \
		uvx awslabs.terraform-mcp-server@latest & \
		echo "Starting dynamodb-mcp-server..."; \
		uvx awslabs.dynamodb-mcp-server@latest & \
		echo "Note: GitHub MCP server requires Docker: ghcr.io/github/github-mcp-server"; \
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
	@pkill -f "terraform-mcp-server" || true
	@pkill -f "dynamodb-mcp-server" || true
	@echo "Note: GitHub MCP server runs in Docker, stop manually if needed"
	@echo "✅ MCP servers stopped"

mcp-test: ## Test MCP server connections
	@echo "🧪 Testing MCP server connections..."
	@if [ -n "$$VIRTUAL_ENV" ]; then \
		python tests/integration/test_mcp_integration.py; \
	else \
		python3 tests/integration/test_mcp_integration.py; \
	fi

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

setup: ## Complete setup: create venv, install deps, install MCP servers, install AgentCore
	@echo "🔧 Setting up AWS DevOps Agent..."
	@echo "1️⃣ Creating virtual environment..."
	python3 -m venv .venv
	@echo "2️⃣ Installing dependencies..."
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -r requirements_dev.txt
	@echo "3️⃣ Installing Bedrock AgentCore CLI..."
	.venv/bin/pip install bedrock-agentcore
	@echo "4️⃣ Installing AWS MCP servers..."
	@if command -v uvx >/dev/null 2>&1; then \
		echo "Installing MCP servers..."; \
		uv tool install awslabs.cost-explorer-mcp-server@latest || echo "⚠️  Failed to install cost-explorer-mcp-server"; \
		uv tool install awslabs.cloudwatch-mcp-server@latest || echo "⚠️  Failed to install cloudwatch-mcp-server"; \
		uv tool install awslabs.aws-pricing-mcp-server@latest || echo "⚠️  Failed to install aws-pricing-mcp-server"; \
		uv tool install awslabs.terraform-mcp-server@latest || echo "⚠️  Failed to install terraform-mcp-server"; \
		uv tool install awslabs.dynamodb-mcp-server@latest || echo "⚠️  Failed to install dynamodb-mcp-server"; \
		echo "Note: GitHub MCP server requires Docker (ghcr.io/github/github-mcp-server)"; \
		echo "✅ MCP installation attempt completed"; \
	else \
		echo "⚠️  uvx not available. MCP servers not installed"; \
		echo "💡 Install uvx with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
		echo "💡 Then run: make mcp-install"; \
	fi
	@echo "✅ Setup complete!"
	@echo "💡 Run 'source .venv/bin/activate' then 'make run'"
	@echo "🚀 For AgentCore deployment: 'make agentcore-configure' then 'make agentcore-deploy'"

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
# BEDROCK AGENTCORE DEPLOYMENT
# =============================================================================

agentcore-install: ## Install Bedrock AgentCore CLI in virtual environment
	@echo "🔧 Installing Bedrock AgentCore CLI..."
	@if [ -f .venv/bin/activate ]; then \
		.venv/bin/pip install bedrock-agentcore; \
		echo "✅ Bedrock AgentCore CLI installed"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-env-dev: ## Create development .env file
	@echo "🔧 Creating development .env file..."
	@cd deployment/bedrock && \
	cp env.example .env && \
	sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=true/' .env && \
	sed -i.bak 's/LOG_LEVEL=INFO/LOG_LEVEL=DEBUG/' .env && \
	sed -i.bak 's/HOST=0.0.0.0/HOST=localhost/' .env && \
	rm .env.bak 2>/dev/null || true && \
	echo "✅ Development .env file created"

agentcore-env-prod: ## Create production .env file
	@echo "🔧 Creating production .env file..."
	@cd deployment/bedrock && \
	cp env.example .env && \
	sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=false/' .env && \
	sed -i.bak 's/LOG_LEVEL=INFO/LOG_LEVEL=WARNING/' .env && \
	sed -i.bak 's/HOST=0.0.0.0/HOST=0.0.0.0/' .env && \
	rm .env.bak 2>/dev/null || true && \
	echo "✅ Production .env file created"

agentcore-env-staging: ## Create staging .env file
	@echo "🔧 Creating staging .env file..."
	@cd deployment/bedrock && \
	cp env.example .env && \
	sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=false/' .env && \
	sed -i.bak 's/LOG_LEVEL=INFO/LOG_LEVEL=INFO/' .env && \
	sed -i.bak 's/HOST=0.0.0.0/HOST=0.0.0.0/' .env && \
	rm .env.bak 2>/dev/null || true && \
	echo "✅ Staging .env file created"

agentcore-configure: ## Configure AgentCore for production deployment
	@echo "⚙️  Configuring Bedrock AgentCore..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		if [ ! -f .env ]; then \
			echo "📋 Creating .env file from template..."; \
			cp env.example .env; \
			echo "✅ Created .env file - please customize it for your environment"; \
		else \
			echo "✅ .env file already exists"; \
		fi; \
		echo ""; \
		echo "📋 AgentCore configuration:"; \
		echo "  - Entrypoint: app.py"; \
		echo "  - Environment file: .env"; \
		echo "  - Agent: AWS DevOps Agent"; \
		echo ""; \
		echo "⚠️  IMPORTANT: All values in .env are REQUIRED - no defaults for safety"; \
		echo "✅ AgentCore configuration completed"; \
		echo "💡 Edit deployment/bedrock/.env to customize your settings"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-validate: ## Validate environment configuration
	@echo "🔍 Validating environment configuration..."
	@python3 scripts/validate_env.py

agentcore-build: ## Build Docker image for AgentCore deployment
	@echo "🐳 Building Docker image for AgentCore deployment..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		cp ../../requirements_production.txt . && \
		cp -r ../../src . && \
		docker build -t aws-devops-agent:latest . && \
		rm -rf src requirements_production.txt && \
		echo "✅ Docker image built successfully"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-health: ## Check AgentCore health status
	@echo "🏥 Checking AgentCore health status..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		curl -f http://localhost:8080/health || echo "❌ Health check failed - agent may not be running"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-metrics: ## Get AgentCore metrics
	@echo "📊 Getting AgentCore metrics..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		curl -s http://localhost:8080/metrics | python3 -m json.tool || echo "❌ Metrics endpoint not available"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-test-local: ## Test AgentCore deployment locally
	@echo "🧪 Testing AgentCore deployment locally..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		if [ ! -f .env ]; then \
			echo "📋 Creating .env file for local testing..."; \
			cp ../../docs/env.example .env; \
			sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=true/' .env; \
			sed -i.bak 's/HOST=0.0.0.0/HOST=localhost/' .env; \
			rm .env.bak 2>/dev/null || true; \
		fi; \
		../../.venv/bin/python app.py; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-deploy-verify: ## Human verification for production deployment
	@echo "🔒 DEPLOYMENT VERIFICATION REQUIRED"
	@echo "=================================="
	@echo "⚠️  CRITICAL: This will deploy to PRODUCTION"
	@echo ""
	@echo "📋 Current Configuration:"
	@echo "  - Agent: AWS DevOps Agent"
	@echo "  - Environment: PRODUCTION"
	@echo "  - Region: $$(aws configure get region 2>/dev/null || echo 'us-east-1')"
	@echo "  - Account: $$(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo 'Not configured')"
	@echo ""
	@read -p "❓ Are you authorized to deploy to PRODUCTION? (yes/no): " auth_confirm; \
	if [ "$$auth_confirm" != "yes" ]; then \
		echo "❌ Deployment aborted - unauthorized"; \
		exit 1; \
	fi
	@read -p "❓ Have you reviewed the deployment configuration? (yes/no): " config_confirm; \
	if [ "$$config_confirm" != "yes" ]; then \
		echo "❌ Deployment aborted - configuration not reviewed"; \
		exit 1; \
	fi
	@read -p "❓ Are you ready to proceed with PRODUCTION deployment? (yes/no): " final_confirm; \
	if [ "$$final_confirm" != "yes" ]; then \
		echo "❌ Deployment aborted - not ready"; \
		exit 1; \
	fi
	@echo "✅ All verifications passed - proceeding with deployment"

agentcore-deploy: agentcore-deploy-verify ## Deploy to Bedrock AgentCore (PRODUCTION)
	@echo "🚀 Deploying to Bedrock AgentCore (PRODUCTION)..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		if [ ! -f .env ]; then \
			echo "📋 Creating .env file for production deployment..."; \
			cp ../../docs/env.example .env; \
			sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=false/' .env; \
			sed -i.bak 's/HOST=0.0.0.0/HOST=0.0.0.0/' .env; \
			rm .env.bak 2>/dev/null || true; \
		fi; \
		../../.venv/bin/python app.py; \
		echo "✅ Deployment completed"; \
		echo "💡 Run 'make agentcore-status' to check deployment status"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-status: ## Check AgentCore deployment status
	@echo "📊 Checking AgentCore deployment status..."
	@if [ -f .venv/bin/activate ]; then \
		echo "🔍 AgentCore Status:"; \
		echo "  - Agent: AWS DevOps Agent"; \
		echo "  - Model: $${BEDROCK_MODEL_ID:-claude-3.5-sonnet}"; \
		echo "  - Debug Mode: $${DEBUG_MODE:-false}"; \
		echo "  - Port: $${PORT:-8080}"; \
		echo "  - Host: $${HOST:-0.0.0.0}"; \
		echo ""; \
		echo "💡 To test the agent, use: make agentcore-test"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-logs: ## View AgentCore deployment logs
	@echo "📝 AgentCore logs are displayed in the console when running"
	@echo "💡 To see logs, run the agent with: make agentcore-test-local or make agentcore-deploy"

agentcore-test: ## Test deployed AgentCore agent
	@echo "🧪 Testing AgentCore agent..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		echo "🧪 Testing agent with sample query..."; \
		curl -X POST http://localhost:8080/invoke \
			-H "Content-Type: application/json" \
			-d '{"prompt": "What are your capabilities?"}' \
			2>/dev/null || echo "❌ Agent not running. Start with: make agentcore-test-local"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

agentcore-rollback: ## Rollback AgentCore deployment (with verification)
	@echo "🔄 ROLLBACK PROCEDURE"
	@echo "===================="
	@echo "⚠️  WARNING: This will stop the production deployment"
	@echo ""
	@read -p "❓ Are you sure you want to stop the agent? (yes/no): " rollback_confirm; \
	if [ "$$rollback_confirm" != "yes" ]; then \
		echo "❌ Rollback aborted"; \
		exit 1; \
	fi
	@echo "🔄 Stopping agent..."
	@pkill -f "python.*app.py" || echo "No running agent found"
	@echo "✅ Agent stopped"

agentcore-monitor: ## Monitor AgentCore deployment performance
	@echo "🔍 Monitoring AgentCore deployment..."
	@if [ -f .venv/bin/activate ]; then \
		echo "📊 Agent Status:"; \
		make agentcore-status; \
		echo ""; \
		echo "🧪 Testing Agent Functionality:"; \
		make agentcore-test; \
		echo ""; \
		echo "💡 For detailed logs, check the console output when running the agent"; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

# =============================================================================
# DEPLOYMENT (Legacy - kept for compatibility)
# =============================================================================

deploy: ## Deploy to Bedrock Agent Core (legacy - use agentcore-deploy)
	@echo "⚠️  Using legacy deploy command. Consider using 'make agentcore-deploy'"
	@make agentcore-deploy

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

example-data-sources: ## Run data sources focused demo
	@echo "📊 Running data sources focused demo..."
	@python docs/demos/demo_data_sources_simple.py

example-report: ## Run document generation example
	@echo "📄 Running document generation example..."
	make query QUERY="Generate a cost analysis report for my AWS infrastructure"