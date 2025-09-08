#!/usr/bin/env python3
"""
Test AWS Account Manager functionality
"""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from aws_devops_agent.config.aws_account_manager import AWSAccountManager, AWSAccountInfo


def test_account_manager_creation():
    """Test creating an AWS account manager"""
    print("🧪 Testing AWS Account Manager creation...")
    
    manager = AWSAccountManager(region="us-east-1", profile="default")
    
    assert manager.region == "us-east-1"
    assert manager.profile == "default"
    assert len(manager.accounts) == 0
    assert manager.current_account is None
    
    print("✅ Account manager created successfully")


def test_account_info_creation():
    """Test creating AWS account info"""
    print("🧪 Testing AWS Account Info creation...")
    
    account = AWSAccountInfo(
        account_id="123456789012",
        account_name="Test Account",
        region="us-east-1",
        is_current=True
    )
    
    assert account.account_id == "123456789012"
    assert account.account_name == "Test Account"
    assert account.region == "us-east-1"
    assert account.is_current is True
    
    print("✅ Account info created successfully")


def test_add_account():
    """Test adding an account to the manager"""
    print("🧪 Testing account addition...")
    
    manager = AWSAccountManager()
    
    # Add account without role
    account1 = manager.add_account("123456789012", "Test Account 1")
    assert account1.account_id == "123456789012"
    assert account1.account_name == "Test Account 1"
    assert "123456789012" in manager.accounts
    
    # Add account with role
    account2 = manager.add_account(
        "987654321098", 
        "Test Account 2", 
        "arn:aws:iam::987654321098:role/DevOpsRole"
    )
    assert account2.account_id == "987654321098"
    assert account2.role_arn == "arn:aws:iam::987654321098:role/DevOpsRole"
    
    print("✅ Account addition works correctly")


def test_account_summary():
    """Test account summary generation"""
    print("🧪 Testing account summary...")
    
    manager = AWSAccountManager()
    
    # Add some test accounts
    manager.add_account("123456789012", "Test Account 1")
    manager.add_account("987654321098", "Test Account 2")
    
    summary = manager.get_account_summary()
    
    assert summary["total_accounts"] == 2
    assert len(summary["accounts"]) == 2
    assert summary["current_account"] is None  # No current account set
    
    print("✅ Account summary works correctly")


def test_model_id_mapping():
    """Test model ID mapping functionality"""
    print("🧪 Testing model ID mapping...")
    
    from aws_devops_agent.config.env_config import EnvironmentConfig
    
    # Test friendly name mapping
    config = EnvironmentConfig(
        aws_region="us-east-1",
        bedrock_model_id="claude-3.5-sonnet",
        port=8080,
        host="0.0.0.0"
    )
    
    mapped_id = config.get_model_id()
    expected_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    assert mapped_id == expected_id
    
    # Test direct model ID (no mapping needed)
    config.bedrock_model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    mapped_id = config.get_model_id()
    assert mapped_id == "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    print("✅ Model ID mapping works correctly")


def run_tests():
    """Run all tests"""
    print("🚀 Running AWS Account Manager Tests")
    print("=" * 50)
    
    try:
        test_account_manager_creation()
        test_account_info_creation()
        test_add_account()
        test_account_summary()
        test_model_id_mapping()
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
