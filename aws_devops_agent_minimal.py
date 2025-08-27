#!/usr/bin/env python3
"""
AWS DevOps Agent - Minimal Demo
Demonstrates MCP integration without Strands SDK dependency
"""

import asyncio
import os
import json
from typing import Dict, List, Any

# MCP imports (now available)
from mcp import stdio_client, StdioServerParameters


class MinimalAWSDevOpsAgent:
    """Minimal AWS DevOps Agent using MCP Servers directly"""
    
    def __init__(self):
        print("🚀 AWS DevOps Agent - Minimal Demo")
        print("   Using Official AWS MCP Servers directly")
        
        self.mcp_clients: Dict[str, Any] = {}
        
        # Official AWS MCP Servers
        self.aws_mcp_servers = {
            "pricing": "awslabs.aws-pricing-mcp-server@latest",
            "dynamodb": "awslabs.dynamodb-mcp-server@latest"
        }
    
    async def test_mcp_server(self, name: str, package: str) -> bool:
        """Test if MCP server is available"""
        try:
            print(f"🔧 Testing {name} MCP server...")
            
            # Create MCP client
            client = stdio_client(
                StdioServerParameters(
                    command="uvx",
                    args=[package]
                )
            )
            
            # Test connection
            async with client as session:
                tools = await session.list_tools()
                if tools:
                    print(f"✅ {name}: {len(tools.tools)} tools available")
                    for tool in tools.tools[:3]:  # Show first 3 tools
                        print(f"   • {tool.name}: {tool.description}")
                    return True
                else:
                    print(f"⚠️ {name}: No tools available")
                    return False
                    
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            return False
    
    async def call_pricing_tool(self, service: str, instance_type: str = None) -> str:
        """Call AWS Pricing MCP server directly"""
        try:
            print(f"💰 Getting pricing for {service}...")
            
            client = stdio_client(
                StdioServerParameters(
                    command="uvx",
                    args=["awslabs.aws-pricing-mcp-server@latest"]
                )
            )
            
            async with client as session:
                # List available tools first
                tools = await session.list_tools()
                if not tools.tools:
                    return "❌ No pricing tools available"
                
                # Try to call a pricing tool
                tool_name = tools.tools[0].name
                print(f"🔧 Using tool: {tool_name}")
                
                # Call the tool with service parameter
                result = await session.call_tool(
                    tool_name,
                    {"service": service, "instanceType": instance_type} if instance_type else {"service": service}
                )
                
                return f"✅ Pricing data: {result.content}"
                
        except Exception as e:
            return f"❌ Pricing query failed: {str(e)}"
    
    async def run_demo(self):
        """Run minimal demo"""
        print(f"\n🎯 Minimal Demo - Testing AWS MCP Servers")
        print("=" * 60)
        
        # Test each MCP server
        for name, package in self.aws_mcp_servers.items():
            print(f"\n📋 Testing {name.upper()} MCP Server")
            print("-" * 40)
            
            success = await self.test_mcp_server(name, package)
            
            if success and name == "pricing":
                # Try a real pricing call
                print(f"\n🔍 Testing real pricing query...")
                result = await self.call_pricing_tool("EC2", "t3.medium")
                print(f"Result: {result}")
            
            print()
        
        print("=" * 60)
        print("✅ Demo complete!")
        print("\nNext steps:")
        print("1. Install Strands SDK for full functionality")
        print("2. Configure AWS credentials")
        print("3. Run: python3 aws_devops_agent.py")


async def main():
    """Main entry point"""
    # Check AWS credentials
    if not (os.getenv("AWS_PROFILE") or os.getenv("AWS_ACCESS_KEY_ID")):
        print("⚠️ AWS credentials not found")
        print("   Configure with: aws configure")
        print("   Or set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY")
        print()
    
    agent = MinimalAWSDevOpsAgent()
    await agent.run_demo()


if __name__ == "__main__":
    asyncio.run(main())