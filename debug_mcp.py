#!/usr/bin/env python3
"""Debug MCP Connection"""

import asyncio
import os
from mcp import ClientSession, StdioServerParameters  
from mcp.client.stdio import stdio_client

async def test_cost_explorer():
    """Test direct Cost Explorer MCP connection"""
    try:
        print("🔬 Testing Cost Explorer MCP server connection...")
        
        # Set up environment
        env = os.environ.copy()
        env.update({
            "AWS_REGION": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            "AWS_PROFILE": os.getenv("AWS_PROFILE", "default"),
            "FASTMCP_LOG_LEVEL": "ERROR"
        })
        
        # Create server parameters
        server_params = StdioServerParameters(
            command="/root/.local/bin/awslabs.cost-explorer-mcp-server",
            env=env
        )
        
        print(f"📡 Connecting to: {server_params.command}")
        
        # Connect with timeout
        async with asyncio.timeout(10):
            async with stdio_client(server_params) as (read, write):
                print("✅ Transport established")
                
                session = ClientSession(read, write)
                print("✅ Session created")
                
                await session.initialize()
                print("✅ Session initialized")
                
                # List available tools
                result = await session.list_tools()
                print(f"🛠️  Available tools: {[tool.name for tool in result.tools]}")
                
                # Try a simple cost query
                print("💰 Testing cost query...")
                cost_result = await session.call_tool("get_cost_and_usage", {
                    "time_period": {
                        "start": "2024-09-01", 
                        "end": "2024-09-04"
                    },
                    "granularity": "DAILY",
                    "metrics": ["BlendedCost"]
                })
                
                print(f"💰 Cost query result: {cost_result.content[:200] if cost_result.content else 'No content'}")
                
    except Exception as e:
        print(f"❌ Cost Explorer test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_cost_explorer())