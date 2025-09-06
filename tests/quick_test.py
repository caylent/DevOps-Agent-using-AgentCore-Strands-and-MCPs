#!/usr/bin/env python3
"""
Quick Test - AWS DevOps Agent
Test main functionality quickly
"""

import sys, asyncio
from pathlib import Path

project_root = Path(__file__).parent
sys.path.append(str(project_root / "config"))
sys.path.append(str(project_root / "tools" / "aws-devops"))

from aws_devops_agent_v2 import AWSDevOpsAgentV2

def main():
    """Quick test scenarios"""
    print("🧪 Quick Test - AWS DevOps Agent")
    print("=" * 40)
    
    # Initialize agent
    agent = AWSDevOpsAgentV2()
    
    # Test scenarios
    scenarios = [
        "¿Cuál es el costo de una instancia t3.medium en us-east-1?",
        "Validate security for an EC2 with public IP",
        "Compare pricing between t3.medium and m5.large"
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎯 Test {i}: {scenario}")
        print("-" * 30)
        
        try:
            response = asyncio.run(agent.chat(scenario))
            # Show first 200 chars of response
            preview = response[:200] + "..." if len(response) > 200 else response
            print(f"✅ Response: {preview}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Quick test complete!")

if __name__ == "__main__":
    main()