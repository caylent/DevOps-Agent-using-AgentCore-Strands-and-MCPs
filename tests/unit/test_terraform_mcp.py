#!/usr/bin/env python3
"""Test Terraform MCP Integration"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
import os

print("🚀 Testing Terraform MCP Integration")

# Prepare environment with AWS credentials
aws_env = os.environ.copy()
aws_env.update({
    "AWS_PROFILE": os.getenv("AWS_PROFILE", "default"),
    "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
})

# For Linux - Terraform MCP Server
print("🏗️ Testing Terraform MCP Server...")
terraform_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.terraform-mcp-server@latest"],
        env=aws_env
    )
))

try:
    with terraform_mcp_client:
        print("✅ Terraform MCP client connected")
        
        # Get the tools from the MCP server
        tools = terraform_mcp_client.list_tools_sync()
        print(f"🛠️  Available Terraform tools: {[getattr(tool, 'name', str(tool)) for tool in tools]}")
        
        # Create an agent with these tools
        agent = Agent(tools=tools)
        print("✅ Terraform Agent created with MCP tools")
        
        # Test Terraform analysis
        print("🏗️ Testing Terraform analysis...")
        
        # Test 1: Ask for Terraform best practices
        print("📋 Asking about Terraform best practices...")
        response1 = agent("What are the AWS Terraform best practices for security?")
        print(f"🎉 Best practices response: {str(response1)[:300]}...")
        
        # Test 2: Ask for cost optimization guidance
        print("💰 Asking about cost optimization...")
        response2 = agent("How can I optimize AWS costs in my Terraform configuration?")
        print(f"🎉 Cost optimization response: {str(response2)[:300]}...")
        
        # Test 3: Ask about security scanning
        print("🔒 Asking about security scanning...")
        response3 = agent("What security checks should I run on my Terraform code?")
        print(f"🎉 Security scanning response: {str(response3)[:300]}...")
        
except Exception as e:
    print(f"❌ Terraform MCP test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Terraform MCP Integration Test Complete!")