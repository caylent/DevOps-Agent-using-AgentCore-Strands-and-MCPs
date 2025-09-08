"""
Configuration for AWS DevOps Agent using Strands AI + Bedrock Agent Core
DEPRECATED: Use env_config.py for centralized environment configuration
This file is kept for backward compatibility
"""

import os
from dataclasses import dataclass
from typing import Dict, List
from .env_config import get_env_config, EnvironmentConfig


@dataclass
class BedrockModelConfig:
    """Configuration for Bedrock AI models."""

    model_id: str
    max_tokens: int = 4000
    temperature: float = 0.1
    region: str = "us-east-1"


@dataclass
class AWSMCPConfig:
    """Configuration for AWS MCP Servers."""
    
    pricing_server: str = "awslabs.aws-pricing-mcp-server@latest"
    dynamodb_server: str = "awslabs.dynamodb-mcp-server@latest"
    cost_explorer_server: str = "awslabs.cost-explorer-mcp-server@latest"
    terraform_server: str = "awslabs.terraform-mcp-server@latest"
    github_server: str = "github.github-mcp-server@latest"
    cloudwatch_server: str = "awslabs.cloudwatch-mcp-server@latest"
    
    # MCP Configuration
    timeout: int = 30
    max_workers: int = 10


@dataclass
class AWSDevOpsConfig:
    """Configuration for AWS DevOps Agent."""

    # Model Configuration
    model: BedrockModelConfig
    
    # AWS MCP Configuration
    mcp: AWSMCPConfig

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_profile: str = "default"

    # Application Settings
    reports_dir: str = "reports"
    cost_analysis_dir: str = "reports/cost-analysis"
    iac_analysis_dir: str = "reports/iac-analysis"
    
    # Multi-account support
    cross_account_roles: Dict[str, str] = None

    # Logging Configuration
    log_level: str = "INFO"
    debug_mode: bool = False


class ConfigManager:
    """Manages AWS DevOps Agent configuration."""

    AVAILABLE_MODELS = {
        "claude-4": BedrockModelConfig(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            max_tokens=4000,
            temperature=0.1,
        ),
        "claude-3.5-sonnet": BedrockModelConfig(
            model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            max_tokens=3000,
            temperature=0.1,
        ),
        "nova-micro": BedrockModelConfig(
            model_id="us.amazon.nova-micro-v1:0", 
            max_tokens=2000, 
            temperature=0.1
        ),
        "nova-lite": BedrockModelConfig(
            model_id="us.amazon.nova-lite-v1:0", 
            max_tokens=3000, 
            temperature=0.1
        ),
    }

    DEFAULT_MODEL = "claude-3.5-sonnet"

    def load_config(self) -> AWSDevOpsConfig:
        """Load configuration from environment using centralized config."""
        # Use centralized environment configuration
        env_config = get_env_config(strict_validation=False)  # Allow defaults for interactive mode
        
        # Map to legacy config structure
        model_name = os.getenv("STRANDS_MODEL", self.DEFAULT_MODEL)
        model_config = self.AVAILABLE_MODELS.get(model_name, self.AVAILABLE_MODELS[self.DEFAULT_MODEL])

        return AWSDevOpsConfig(
            model=model_config,
            mcp=AWSMCPConfig(
                timeout=env_config.mcp_timeout,
                max_workers=env_config.mcp_max_workers
            ),
            aws_region=env_config.aws_region,
            aws_profile=env_config.aws_profile,
            log_level=env_config.log_level,
            debug_mode=env_config.debug_mode,
            cross_account_roles=env_config.cross_account_roles or None,
        )


def get_config() -> AWSDevOpsConfig:
    """Get configuration."""
    config_manager = ConfigManager()
    return config_manager.load_config()