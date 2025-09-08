#!/usr/bin/env python3
"""
Environment Configuration Validation Script
Validates environment configuration for AgentCore deployment
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import only the env_config module directly
sys.path.insert(0, str(src_path / "aws_devops_agent" / "config"))
from env_config import load_env_file, get_env_config

def main():
    """Validate environment configuration"""
    try:
        print("🔍 Validating environment configuration...")
        
        # Load environment file
        load_env_file()
        
        # Get configuration with strict validation
        config = get_env_config(strict_validation=True)
        
        print("✅ Environment configuration is valid")
        print(f"   AWS Region: {config.aws_region}")
        print(f"   Model ID: {config.bedrock_model_id}")
        print(f"   Server: {config.host}:{config.port}")
        print(f"   Debug Mode: {config.debug_mode}")
        
        # Check for warnings
        warnings = config.validate_configuration()
        if warnings:
            print("\n⚠️  Configuration warnings:")
            for warning in warnings:
                print(f"   - {warning}")
        else:
            print("\n✅ No configuration warnings")
            
        print("\n🎉 Environment validation completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        print("\n💡 Solutions:")
        print("  1. Set required environment variables")
        print("  2. Create a .env file: make agentcore-env-dev")
        print("  3. Check configuration: make agentcore-configure")
        return 1

if __name__ == "__main__":
    exit(main())
