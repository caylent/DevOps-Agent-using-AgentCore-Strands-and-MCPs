"""
Centralized Environment Configuration for AWS DevOps Agent
Single source of truth for all environment variables across agentcore and strands
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from pathlib import Path


@dataclass
class EnvironmentConfig:
    """Centralized environment configuration with validation"""
    
    # =============================================================================
    # REQUIRED VARIABLES (NO DEFAULTS - MUST BE SET)
    # =============================================================================
    aws_region: str
    bedrock_model_id: str
    port: int
    host: str
    
    # =============================================================================
    # OPTIONAL VARIABLES (WITH SENSIBLE DEFAULTS)
    # =============================================================================
    aws_profile: str = "default"
    bedrock_region: Optional[str] = None
    debug_mode: bool = False
    log_level: str = "INFO"
    
    # MCP Configuration
    mcp_timeout: int = 30
    mcp_max_workers: int = 10
    
    # Multi-Account Support
    cross_account_roles: Dict[str, str] = field(default_factory=dict)
    aws_account_id: Optional[str] = None
    aws_account_name: Optional[str] = None
    aws_role_arn: Optional[str] = None
    
    # Security Configuration
    github_token: Optional[str] = None
    github_repo: Optional[str] = None
    
    # Advanced Configuration
    aws_default_region: Optional[str] = None
    
    @classmethod
    def from_env(cls, strict_validation: bool = True) -> 'EnvironmentConfig':
        """Load configuration from environment variables"""
        
        # Required variables (no defaults)
        required_vars = {
            'AWS_REGION': 'AWS region (e.g., us-east-1)',
            'BEDROCK_MODEL_ID': 'Bedrock model ID (e.g., claude-3.5-sonnet)',
            'PORT': 'Server port (e.g., 8080)',
            'HOST': 'Server host (e.g., 0.0.0.0 or localhost)'
        }
        
        # Validate required variables
        missing_vars = []
        for var, description in required_vars.items():
            if not os.getenv(var):
                missing_vars.append(f"  - {var}: {description}")
        
        if missing_vars and strict_validation:
            raise EnvironmentError(
                f"Missing required environment variables:\n" + 
                "\n".join(missing_vars) +
                "\n\nSet these variables or use EnvironmentConfig.from_env(strict_validation=False) for development"
            )
        
        # Load configuration
        config = cls(
            # Required
            aws_region=os.getenv('AWS_REGION', 'us-east-1'),
            bedrock_model_id=os.getenv('BEDROCK_MODEL_ID', 'claude-3.5-sonnet'),
            port=int(os.getenv('PORT', '8080')),
            host=os.getenv('HOST', '0.0.0.0'),
            
            # Optional with defaults
            aws_profile=os.getenv('AWS_PROFILE', 'default'),
            bedrock_region=os.getenv('BEDROCK_REGION'),
            debug_mode=os.getenv('DEBUG_MODE', 'false').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            
            # MCP Configuration
            mcp_timeout=int(os.getenv('MCP_TIMEOUT', '30')),
            mcp_max_workers=int(os.getenv('MCP_MAX_WORKERS', '10')),
            
            # Security
            github_token=os.getenv('GITHUB_TOKEN'),
            github_repo=os.getenv('GITHUB_REPO'),
            
            # AWS Account
            aws_account_id=os.getenv('AWS_ACCOUNT_ID'),
            aws_account_name=os.getenv('AWS_ACCOUNT_NAME'),
            aws_role_arn=os.getenv('AWS_ROLE_ARN'),
            
            # Advanced
            aws_default_region=os.getenv('AWS_DEFAULT_REGION')
        )
        
        # Parse cross-account roles
        if os.getenv('CROSS_ACCOUNT_ROLES'):
            for account_role in os.getenv('CROSS_ACCOUNT_ROLES', '').split(','):
                if ':' in account_role:
                    account, role = account_role.strip().split(':', 1)
                    config.cross_account_roles[account] = role
        
        # Set bedrock_region to aws_region if not specified
        if not config.bedrock_region:
            config.bedrock_region = config.aws_region
            
        # Set aws_default_region to aws_region if not specified
        if not config.aws_default_region:
            config.aws_default_region = config.aws_region
        
        return config
    
    def get_model_id(self) -> str:
        """Get the actual model ID, resolving friendly names"""
        model_mapping = {
            "claude-4": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "claude-3.5-sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            "nova-micro": "us.amazon.nova-micro-v1:0",
            "nova-lite": "us.amazon.nova-lite-v1:0"
        }
        
        return model_mapping.get(self.bedrock_model_id, self.bedrock_model_id)
    
    def get_aws_env(self) -> Dict[str, str]:
        """Get AWS environment variables for MCP servers"""
        return {
            "AWS_REGION": self.aws_region,
            "AWS_PROFILE": self.aws_profile,
            "AWS_DEFAULT_REGION": self.aws_default_region,
            "PATH": f"/root/.local/bin:{os.environ.get('PATH', '')}"
        }
    
    def validate_configuration(self) -> List[str]:
        """Validate configuration and return list of warnings/errors"""
        warnings = []
        
        # Validate AWS region
        common_regions = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
        if self.aws_region not in common_regions:
            warnings.append(f"AWS_REGION '{self.aws_region}' is not a common production region")
        
        # Validate model ID
        if "claude" not in self.bedrock_model_id.lower() and "nova" not in self.bedrock_model_id.lower():
            warnings.append(f"BEDROCK_MODEL_ID '{self.bedrock_model_id}' doesn't look like a standard model")
        
        # Validate port
        if not (1 <= self.port <= 65535):
            warnings.append(f"PORT '{self.port}' is not a valid port number")
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            warnings.append(f"LOG_LEVEL '{self.log_level}' is not valid. Use one of: {valid_log_levels}")
        
        return warnings
    
    def to_dict(self) -> Dict[str, Union[str, int, bool, Dict]]:
        """Convert configuration to dictionary for serialization"""
        return {
            "aws_region": self.aws_region,
            "bedrock_model_id": self.bedrock_model_id,
            "port": self.port,
            "host": self.host,
            "aws_profile": self.aws_profile,
            "bedrock_region": self.bedrock_region,
            "debug_mode": self.debug_mode,
            "log_level": self.log_level,
            "mcp_timeout": self.mcp_timeout,
            "mcp_max_workers": self.mcp_max_workers,
            "cross_account_roles": self.cross_account_roles,
            "github_token": "***" if self.github_token else None,
            "github_repo": self.github_repo,
            "aws_default_region": self.aws_default_region
        }


def load_env_file(env_file_path: Optional[Path] = None) -> None:
    """Load environment variables from .env file with proper precedence"""
    if env_file_path is None:
        # Try to find .env file in common locations
        possible_paths = [
            Path.cwd() / ".env",
            Path(__file__).parent.parent.parent.parent / "deployment" / "bedrock" / ".env",
            Path.home() / ".aws-devops-agent" / ".env"
        ]
        
        for path in possible_paths:
            if path.exists():
                env_file_path = path
                break
    
    if env_file_path and env_file_path.exists():
        try:
            with open(env_file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip('"\'')
                        
                        # Only set if not already in environment (system env takes precedence)
                        if key not in os.environ:
                            os.environ[key] = value
                        else:
                            print(f"💡 Skipping {key} from .env (already set in system environment)")
            
            print(f"✅ Loaded .env file from {env_file_path}")
        except Exception as e:
            print(f"⚠️  Warning: Error loading .env file: {e}")
            print("💡 Continuing with system environment variables only")
    else:
        print(f"💡 No .env file found - using system environment variables only")


def get_env_config(strict_validation: bool = True) -> EnvironmentConfig:
    """Get environment configuration with optional strict validation"""
    return EnvironmentConfig.from_env(strict_validation=strict_validation)
