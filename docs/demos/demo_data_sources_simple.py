#!/usr/bin/env python3
"""
Demo: Data Source Indicators
Demonstrates clear data source indicators in tool responses
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aws_devops_agent.tools.aws_iac.terraform import analyze_terraform_configuration
from aws_devops_agent.tools.aws_compliance.security import validate_security_policies
from aws_devops_agent.tools.github.integration import create_optimization_pull_request
from aws_devops_agent.tools.reporting.document_generator import generate_document


def demo_data_sources_simple():
    """Simple, focused data sources demo"""
    print("📊 Data Source Indicators Demo")
    print("=" * 40)
    print("Purpose: Show clear data source indicators in tool responses")
    print("Scope: Different tool types and their data sources")
    print()
    
    # Test IaC Analysis
    print("🏗️ Infrastructure as Code Analysis:")
    print("-" * 40)
    try:
        result = analyze_terraform_configuration("/tmp", "production")
        data_source = result.get("data_source", "Not specified")
        print(f"   Data Source: {data_source}")
        print(f"   Status: {result.get('status', 'Unknown')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test Security Validation
    print("🔒 Security Policy Validation:")
    print("-" * 35)
    try:
        result = validate_security_policies("EC2", {"InstanceType": "t3.micro"})
        data_source = result.get("data_source", "Not specified")
        print(f"   Data Source: {data_source}")
        print(f"   Status: {result.get('status', 'Unknown')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test GitHub Integration (without consent)
    print("🐙 GitHub Integration (No Consent):")
    print("-" * 35)
    try:
        result = create_optimization_pull_request(
            "test/repo", 
            "cost", 
            {"changes": []}, 
            user_consent=False
        )
        data_source = result.get("data_source", "Not specified")
        print(f"   Data Source: {data_source}")
        print(f"   Status: {result.get('status', 'Unknown')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test Document Generation
    print("📄 Document Generation:")
    print("-" * 25)
    try:
        result = generate_document(
            "Test content", 
            "Test Document", 
            "general"
        )
        data_source = result.get("data_source", "Not specified")
        print(f"   Data Source: {data_source}")
        print(f"   Status: {result.get('status', 'Unknown')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    print("🎉 Demo completed!")
    print("This shows how all tools now include clear data source indicators.")


if __name__ == "__main__":
    demo_data_sources_simple()
