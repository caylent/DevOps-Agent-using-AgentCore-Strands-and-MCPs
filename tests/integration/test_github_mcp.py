#!/usr/bin/env python3
"""Test GitHub MCP Integration"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
import os

def load_github_config():
    """Load GitHub configuration from .env.github file"""
    config = {}
    try:
        with open('config/.env.github', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value
        return config
    except Exception as e:
        print(f"❌ Error loading GitHub config: {e}")
        return {}

print("🚀 Testing GitHub MCP Integration")

# Load GitHub configuration
github_config = load_github_config()
github_token = github_config.get('GITHUB_PERSONAL_ACCESS_TOKEN')
github_username = github_config.get('GITHUB_USERNAME', '')
default_repo = github_config.get('GITHUB_DEFAULT_REPO', '')

if not github_token:
    print("⚠️  GitHub token not found - skipping GitHub MCP tests")
    print("   To enable GitHub tests, create config/.env.github with GITHUB_PERSONAL_ACCESS_TOKEN")
    # Skip GitHub-dependent tests instead of exiting
    import pytest
    pytest.skip("GitHub configuration not available", allow_module_level=True)

print(f"✅ GitHub token loaded (user: {github_username})")
print(f"✅ Default repo: {default_repo}")

# Prepare environment with GitHub token
github_env = os.environ.copy()
github_env.update({
    "GITHUB_PERSONAL_ACCESS_TOKEN": github_token
})

# GitHub MCP Server using Docker
print("🐙 Testing GitHub MCP Server...")
try:
    # Use GitHub MCP Server with Docker
    github_mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", 
                  "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={github_token}",
                  "ghcr.io/github/github-mcp-server"],
            env=github_env
        )
    ))

    with github_mcp_client:
        print("✅ GitHub MCP client connected")
        
        # Get the tools from the MCP server
        tools = github_mcp_client.list_tools_sync()
        print(f"🛠️  Available GitHub tools: {len(tools)} tools")
        for i, tool in enumerate(tools[:5]):  # Show first 5 tools
            tool_name = getattr(tool, 'name', str(tool))
            print(f"   {i+1}. {tool_name}")
        
        if len(tools) > 5:
            print(f"   ... and {len(tools) - 5} more tools")
        
        # Create an agent with these tools
        agent = Agent(tools=tools)
        print("✅ GitHub Agent created with MCP tools")
        
        # Test GitHub operations
        print("\n🧪 Testing GitHub operations...")
        
        # Test 1: Repository info
        print("📁 Getting repository information...")
        response1 = agent(f"Get information about the repository {default_repo}")
        print(f"📁 Repo info: {str(response1)[:200]}...")
        
        # Test 2: List issues
        print("📝 Listing repository issues...")
        response2 = agent(f"List the open issues in {default_repo}")
        print(f"📝 Issues: {str(response2)[:200]}...")
        
        # Test 3: Check if we can analyze files
        print("🔍 Checking repository files...")
        response3 = agent(f"What files are in the root of {default_repo}?")
        print(f"🔍 Files: {str(response3)[:200]}...")
        
except Exception as e:
    print(f"❌ GitHub MCP test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 GitHub MCP Integration Test Complete!")