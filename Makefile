# AWS DevOps Agent - Consolidated Makefile
# Simplified and consolidated commands

.PHONY: help run dev setup clean test

# Default target
help: ## Show this help message
	@echo "🚀 AWS DevOps Agent - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "🎯 MAIN COMMANDS"
	@echo "=================="
	@echo "\033[36mrun\033[0m                  Run the agent (interactive mode) - MAIN COMMAND"
	@echo "\033[36mdev\033[0m                  Run in demo mode"
	@echo "\033[36mquery\033[0m                Run a single query (usage: make query QUERY=\"your query\")"
	@echo "\033[36mrun-no-account-selection\033[0m Run the agent without interactive account selection"
	@echo ""
	@echo "🔧 SETUP & INSTALLATION"
	@echo "========================="
	@echo "\033[36msetup\033[0m                Complete setup: create venv, install deps, install MCP servers, install AgentCore"
	@echo "\033[36minstall\033[0m              Install dependencies (alias for setup)"
	@echo "\033[36mclean\033[0m                Clean up temporary files and virtual environment"
	@echo "\033[36mstatus\033[0m               Show project status"
	@echo ""
	@echo "🔌 MCP SERVER MANAGEMENT"
	@echo "========================="
	@echo "\033[36mmcp-check\033[0m            Check if MCP servers are installed (AWS + GitHub)"
	@echo "\033[36mmcp-install\033[0m          Install AWS MCP servers + GitHub MCP server from source"
	@echo "\033[36mmcp-run\033[0m              Run MCP servers directly (development)"
	@echo "\033[36mmcp-stop\033[0m             Stop all running MCP servers"
	@echo "\033[36mmcp-test\033[0m             Test MCP server connections"
	@echo ""
	@echo "🧪 TESTING & DEVELOPMENT"
	@echo "========================="
	@echo "\033[36mtest\033[0m                 Run all tests (excludes integration tests)"
	@echo "\033[36mtest-terraform\033[0m       Run Terraform tests"
	@echo "\033[36mtest-integration\033[0m     Run integration tests (requires GitHub config)"
	@echo "\033[36mtest-complete-workflow\033[0m Run complete workflow test (requires GitHub config)"
	@echo "\033[36mformat\033[0m               Format code"
	@echo ""
	@echo "🚀 AGENTCORE DEPLOYMENT"
	@echo "========================"
	@echo "\033[36magentcore-env\033[0m        Create .env file for AgentCore (usage: make agentcore-env ENV=dev|prod|staging)"
	@echo "\033[36magentcore-configure\033[0m  Configure AgentCore for deployment"
	@echo "\033[36magentcore-validate\033[0m   Validate environment configuration"
	@echo "\033[36magentcore-build\033[0m      Build Docker image for AgentCore deployment"
	@echo "\033[36magentcore-test-local\033[0m Test AgentCore deployment locally"
	@echo "\033[36magentcore-deploy-verify\033[0m Human verification for production deployment"
	@echo "\033[36magentcore-deploy\033[0m     Deploy to Bedrock AgentCore (PRODUCTION)"
	@echo "\033[36magentcore-status\033[0m     Check AgentCore deployment status"
	@echo "\033[36magentcore-test\033[0m       Test deployed AgentCore agent"
	@echo "\033[36magentcore-rollback\033[0m   Rollback AgentCore deployment (with verification)"
	@echo "\033[36magentcore-monitor\033[0m    Monitor AgentCore deployment performance"
	@echo ""
	@echo "📚 EXAMPLES & DEMOS"
	@echo "===================="
	@echo "\033[36mexample\033[0m              Run example (usage: make example TYPE=cost|iac|compliance|cdk|terraform|security|data-sources|report)"
	@echo ""
	@echo "💡 Quick Start: make setup && make run"
	@echo "🔧 AgentCore: make agentcore-configure && make agentcore-deploy"
	@echo "📚 Examples: make example TYPE=cost"
	@echo ""
	@echo "ℹ️  Legacy commands (agentcore-env-dev, agentcore-env-prod, etc.) are still available"
	@echo "   but use the new consolidated commands above for better experience"

# =============================================================================
# MAIN COMMANDS
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
	.venv/bin/pip install bedrock-agentcore
	@echo "3️⃣ Installing AWS MCP servers..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "Installing MCP servers..."; \
		uv tool install awslabs.cost-explorer-mcp-server@latest || echo "⚠️  Failed to install cost-explorer-mcp-server"; \
		uv tool install awslabs.cloudwatch-mcp-server@latest || echo "⚠️  Failed to install cloudwatch-mcp-server"; \
		uv tool install awslabs.aws-pricing-mcp-server@latest || echo "⚠️  Failed to install aws-pricing-mcp-server"; \
		uv tool install awslabs.terraform-mcp-server@latest || echo "⚠️  Failed to install terraform-mcp-server"; \
		uv tool install awslabs.dynamodb-mcp-server@latest || echo "⚠️  Failed to install dynamodb-mcp-server"; \
		echo "Note: GitHub MCP server requires Docker (ghcr.io/github/github-mcp-server)"; \
		echo "✅ MCP installation attempt completed"; \
	else \
		echo "⚠️  uv not available. MCP servers not installed"; \
		echo "💡 Install uv with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
		echo "💡 Then run: make mcp-install"; \
	fi
	@echo "✅ Setup complete!"
	@echo "💡 Run 'source .venv/bin/activate' then 'make run'"
	@echo "🚀 For AgentCore deployment: 'make agentcore-configure' then 'make agentcore-deploy'"

install: setup ## Install dependencies (alias for setup)

# =============================================================================
# MCP SERVER MANAGEMENT
# =============================================================================

mcp-check: ## Check if MCP servers are installed (AWS + GitHub)
	@echo "🔌 Checking MCP servers..."
	@echo ""
	@if command -v uv >/dev/null 2>&1; then \
		echo "✅ uv is available"; \
		echo ""; \
		echo "Checking installed AWS MCP servers:"; \
		uv tool list 2>/dev/null | grep -E "(cost-explorer|cloudwatch|aws-pricing|terraform|dynamodb)" || echo "❌ No AWS MCP servers found"; \
		echo ""; \
		echo "🔍 Checking GitHub MCP Server status:"; \
		if [ -f github-mcp-server/github-mcp-server ]; then \
			echo "✅ GitHub MCP Server binary available at github-mcp-server/github-mcp-server"; \
		else \
			echo "❌ GitHub MCP Server binary not found"; \
		fi; \
	else \
		echo "❌ uv not available. Install with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
	fi

mcp-install: ## Install AWS MCP servers and GitHub MCP server
	@echo "🔌 Installing MCP servers (AWS + GitHub)..."
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
		echo ""; \
		echo "🐙 Installing GitHub MCP Server from source..."; \
		if [ -f src/aws_devops_agent/config/.env ]; then \
			. src/aws_devops_agent/config/.env; \
			if [ -n "$$GITHUB_PERSONAL_ACCESS_TOKEN" ] && command -v go >/dev/null 2>&1; then \
				if [ ! -d "./github-mcp-server" ]; then \
					echo "📥 Cloning GitHub MCP Server repository..."; \
					git clone https://github.com/github/github-mcp-server.git; \
				fi; \
				echo "🔨 Building GitHub MCP Server..."; \
				cd github-mcp-server/cmd/github-mcp-server && go build -o ../../github-mcp-server; \
				chmod +x ../../github-mcp-server; \
				echo "✅ GitHub MCP Server built successfully"; \
			else \
				echo "⚠️  GitHub MCP Server skipped - requires Go and GITHUB_PERSONAL_ACCESS_TOKEN in .env"; \
			fi; \
		else \
			echo "⚠️  GitHub MCP Server skipped - configuration file not found"; \
		fi; \
		echo ""; \
		echo "✅ MCP installation completed"; \
		echo "💡 Run 'make mcp-check' to verify installation"; \
	else \
		echo "❌ uv not available. Install with: curl -LsSf https://astral.sh/uv/install.sh \| sh"; \
		exit 1; \
	fi

mcp-run: ## Run MCP servers directly (development)
	@echo "🚀 Running MCP servers directly (AWS + GitHub)..."
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
		echo ""; \
		echo "🐙 Starting GitHub MCP Server..."; \
		if [ -f github-mcp-server/github-mcp-server ] && [ -f src/aws_devops_agent/config/.env ]; then \
			. src/aws_devops_agent/config/.env; \
			if [ -n "$$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then \
				cd github-mcp-server && GITHUB_PERSONAL_ACCESS_TOKEN=$$GITHUB_PERSONAL_ACCESS_TOKEN ./github-mcp-server stdio & \
				cd ..; \
				echo "✅ GitHub MCP Server started"; \
			else \
				echo "⚠️  GitHub MCP Server not started - GITHUB_PERSONAL_ACCESS_TOKEN not found in .env"; \
			fi; \
		else \
			echo "⚠️  GitHub MCP Server not started - binary or .env file not found"; \
		fi; \
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
	@pkill -f "github-mcp-server" || true
	@echo "✅ MCP servers stopped"

mcp-test: ## Test MCP server connections
	@echo "🧪 Testing MCP server connections..."
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate && \
		python tests/integration/test_mcp_integration.py; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi


# =============================================================================
# DEVELOPMENT & TESTING
# =============================================================================

test: ## 🧪 Run core tests (unit + document generation)
	@echo "🧪 Running core tests..."
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate && \
		PYTHONPATH=src python -m pytest tests/unit/ tests/document_generation/ -v --ignore=tests/unit/test_aws_devops_agent.py --ignore=tests/document_generation/test_agent_document_generation.py; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

test-terraform: ## 🏗️ Run Terraform tests
	@echo "🏗️ Running Terraform tests..."
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate && \
		PYTHONPATH=src python -m pytest tests/terraform/ -v; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

test-integration: ## 🔗 Run integration tests (requires GitHub config)
	@echo "🔗 Running integration tests..."
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate && \
		PYTHONPATH=src python -m pytest tests/integration/ -v; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

test-complete-workflow: ## 🚀 Run complete workflow test (requires GitHub config)
	@echo "🚀 Running complete workflow test..."
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate && \
		PYTHONPATH=src python -m pytest tests/integration/test_complete_workflow.py -v; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

test-all: ## 🧪 Run all tests (core + terraform + integration)
	@echo "🧪 Running all tests..."
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate && \
		PYTHONPATH=src python -m pytest tests/ -v; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi

format: ## Format code
	@echo "🎨 Formatting code..."
	@if [ -f .venv/bin/activate ]; then \
		source .venv/bin/activate && \
		black src/ tests/ --line-length=100; \
		isort src/ tests/ --profile black; \
	else \
		echo "❌ Virtual environment not found. Run 'make setup' first"; \
		exit 1; \
	fi
	@echo "✅ Code formatted"

# =============================================================================
# AGENTCORE DEPLOYMENT
# =============================================================================

agentcore-env: ## Create .env file for AgentCore (usage: make agentcore-env ENV=dev|prod|staging)
	@echo "🔧 Creating $(ENV:-dev) .env file..."
	@cd deployment/bedrock && \
	cp env.example .env && \
	if [ "$(ENV)" = "prod" ]; then \
		sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=false/' .env && \
		sed -i.bak 's/LOG_LEVEL=INFO/LOG_LEVEL=WARNING/' .env && \
		sed -i.bak 's/HOST=0.0.0.0/HOST=0.0.0.0/' .env; \
	elif [ "$(ENV)" = "staging" ]; then \
		sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=false/' .env && \
		sed -i.bak 's/LOG_LEVEL=INFO/LOG_LEVEL=INFO/' .env && \
		sed -i.bak 's/HOST=0.0.0.0/HOST=0.0.0.0/' .env; \
	else \
		sed -i.bak 's/DEBUG_MODE=false/DEBUG_MODE=true/' .env && \
		sed -i.bak 's/LOG_LEVEL=INFO/LOG_LEVEL=DEBUG/' .env && \
		sed -i.bak 's/HOST=0.0.0.0/HOST=localhost/' .env; \
	fi && \
	rm .env.bak 2>/dev/null || true && \
	echo "✅ $(ENV:-dev) .env file created"

agentcore-configure: ## Configure AgentCore for deployment
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

agentcore-test-local: ## Test AgentCore deployment locally
	@echo "🧪 Testing AgentCore deployment locally..."
	@if [ -f .venv/bin/activate ]; then \
		cd deployment/bedrock && \
		if [ ! -f .env ]; then \
			echo "📋 Creating .env file for local testing..."; \
			make agentcore-env ENV=dev; \
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
			make agentcore-env ENV=prod; \
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
# EXAMPLES (Consolidated)
# =============================================================================

example: ## Run example (usage: make example TYPE=cost|iac|compliance|cdk|terraform|security|data-sources|report)
	@if [ -z "$(TYPE)" ]; then \
		echo "❌ Please provide example type: make example TYPE=cost"; \
		echo "Available types: cost, iac, compliance, cdk, terraform, security, data-sources, report"; \
		exit 1; \
	fi
	@case "$(TYPE)" in \
		cost) \
			echo "💰 Running cost analysis example..."; \
			make query QUERY="Analyze my AWS costs and provide optimization recommendations"; \
			;; \
		iac) \
			echo "🏗️ Running IaC analysis example..."; \
			make query QUERY="Analyze my Terraform configuration for security and cost optimization"; \
			;; \
		compliance) \
			echo "🔒 Running compliance check example..."; \
			make query QUERY="Check my AWS infrastructure for SOC2 compliance"; \
			;; \
		cdk) \
			echo "🏗️ Running CDK analysis example..."; \
			make query QUERY="Analyze my CDK project for optimization opportunities and security issues"; \
			;; \
		terraform) \
			echo "🏗️ Running Terraform analysis example..."; \
			make query QUERY="Analyze my Terraform project for cost optimization and security issues"; \
			;; \
		security) \
			echo "🛡️ Running AWS security analysis example..."; \
			python docs/demos/demo_aws_security_analysis.py; \
			;; \
		data-sources) \
			echo "📊 Running data sources focused demo..."; \
			python docs/demos/demo_data_sources_simple.py; \
			;; \
		report) \
			echo "📄 Running document generation example..."; \
			make query QUERY="Generate a cost analysis report for my AWS infrastructure"; \
			;; \
		*) \
			echo "❌ Unknown example type: $(TYPE)"; \
			echo "Available types: cost, iac, compliance, cdk, terraform, security, data-sources, report"; \
			exit 1; \
			;; \
	esac

# Legacy aliases for backward compatibility
deploy: agentcore-deploy ## Deploy to Bedrock Agent Core (legacy - use agentcore-deploy)
agentcore-install: setup ## Install Bedrock AgentCore CLI (legacy - use setup)
agentcore-env-dev: ## Create development .env file (legacy - use agentcore-env ENV=dev)
	@make agentcore-env ENV=dev
agentcore-env-prod: ## Create production .env file (legacy - use agentcore-env ENV=prod)
	@make agentcore-env ENV=prod
agentcore-env-staging: ## Create staging .env file (legacy - use agentcore-env ENV=staging)
	@make agentcore-env ENV=staging
agentcore-health: ## Check AgentCore health status (legacy - use agentcore-test)
	@echo "🏥 Checking AgentCore health status..."
	@curl -f http://localhost:8080/health || echo "❌ Health check failed - agent may not be running"
agentcore-metrics: ## Get AgentCore metrics (legacy - use agentcore-test)
	@echo "📊 Getting AgentCore metrics..."
	@curl -s http://localhost:8080/metrics | python3 -m json.tool || echo "❌ Metrics endpoint not available"
agentcore-logs: ## View AgentCore deployment logs (legacy - use agentcore-test-local)
	@echo "📝 AgentCore logs are displayed in the console when running"
	@echo "💡 To see logs, run the agent with: make agentcore-test-local or make agentcore-deploy"
