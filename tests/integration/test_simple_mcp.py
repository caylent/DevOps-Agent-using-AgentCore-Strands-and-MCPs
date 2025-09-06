#!/usr/bin/env python3
"""Simple MCP Test - Direct from Strands Documentation"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
import os

print("🚀 Testing Simple MCP Integration (Linux)")

# Prepare environment with AWS credentials
aws_env = os.environ.copy()
aws_env.update({
    "AWS_PROFILE": os.getenv("AWS_PROFILE", "default"),
    "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
})

# For Linux - Cost Explorer with AWS credentials
print("💰 Testing Cost Explorer MCP Server...")
cost_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.cost-explorer-mcp-server@latest"],
        env=aws_env
    )
))

try:
    with cost_mcp_client:
        print("✅ Cost Explorer MCP client connected")
        
        # Get the tools from the MCP server
        tools = cost_mcp_client.list_tools_sync()
        print(f"🛠️  Available tools: {[getattr(tool, 'name', str(tool)) for tool in tools]}")
        
        # Create an agent with these tools
        agent = Agent(tools=tools)
        print("✅ Agent created with MCP tools")
        
        # Test a real AWS cost query
        print("💰 Asking agent for AWS costs...")
        response = agent("Get my AWS costs for the last 3 days")
        print(f"🎉 SUCCESS! Agent response: {str(response)[:200]}...")
        
except Exception as e:
    print(f"❌ Cost Explorer test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)

# Test CloudWatch too with AWS credentials
print("📊 Testing CloudWatch MCP Server...")
cw_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.cloudwatch-mcp-server@latest"],
        env=aws_env
    )
))

try:
    with cw_mcp_client:
        print("✅ CloudWatch MCP client connected")
        
        # Get the tools from the MCP server
        tools = cw_mcp_client.list_tools_sync()
        print(f"🛠️  Available CloudWatch tools: {[getattr(tool, 'name', str(tool)) for tool in tools]}")
        
        # Create an agent with these tools
        agent = Agent(tools=tools)
        print("✅ CloudWatch Agent created with MCP tools")
        
        # Test a CloudWatch query
        print("📊 Asking agent about CloudWatch...")
        response = agent("List any CloudWatch alarms that are currently in ALARM state")
        print(f"🎉 SUCCESS! CloudWatch response: {str(response)[:200]}...")
        
except Exception as e:
    print(f"❌ CloudWatch test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 MCP Integration Test Complete!")