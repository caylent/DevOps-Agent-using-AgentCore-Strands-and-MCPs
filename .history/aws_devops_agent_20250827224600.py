#!/usr/bin/env python3
"""
AWS DevOps Agent - Production Ready
Uses Strands SDK + Official AWS MCP Servers

This is the clean, production-ready implementation.
No mocks, no demo code - only real AWS integrations.
"""

import asyncio
import os
from typing import Dict, List, Any

# Real Strands imports - will fail if not available
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient


class AWSDevOpsAgent:
    """Production AWS DevOps Agent using Official MCP Servers"""
    
    def __init__(self):
        print("🚀 AWS DevOps Agent - Production Ready")
        print("   Using Strands SDK + Official AWS MCP Servers")
        
        self.mcp_clients: Dict[str, MCPClient] = {}
        self.agent: Agent = None
        
        # Official AWS MCP Servers
        self.aws_mcp_servers = {
            "pricing": "awslabs.aws-pricing-mcp-server@latest",
            "dynamodb": "awslabs.dynamodb-mcp-server@latest",
            "cost_explorer": "awslabs.cost-explorer-mcp-server@latest"
        }
    
    async def setup_mcp_server(self, name: str, package: str) -> List[Any]:
        """Setup individual AWS MCP Server"""
        try:
            print(f"🔧 Setting up {name} MCP server...")
            
            mcp_client = MCPClient(lambda: stdio_client(
                StdioServerParameters(
                    command="uvx",
                    args=[package]
                )
            ))
            
            mcp_client.start()
            tools = mcp_client.list_tools_sync()
            
            if tools:
                self.mcp_clients[name] = mcp_client
                print(f"✅ {name}: {len(tools)} tools loaded")
                return tools
            else:
                print(f"⚠️ {name}: No tools available")
                return []
                
        except Exception as e:
            print(f"❌ {name} setup failed: {e}")
            return []
    
    async def setup_agent(self) -> bool:
        """Setup Strands Agent with AWS MCP tools"""
        try:
            print("\n🤖 Initializing Strands Agent...")
            
            # Setup all AWS MCP servers
            all_tools = []
            for name, package in self.aws_mcp_servers.items():
                tools = await self.setup_mcp_server(name, package)
                all_tools.extend(tools)
            
            if not all_tools:
                print("❌ No AWS MCP tools available")
                return False
            
            # Create Strands Agent
            self.agent = Agent(
                model="us.anthropic.claude-sonnet-4-20250514-v1:0",
                tools=all_tools,
                system_prompt="""You are a production AWS DevOps agent with access to official AWS MCP servers.

REAL AWS CAPABILITIES:
• AWS Pricing API: Real-time pricing data for all AWS services
• DynamoDB Operations: Create, manage, query tables and data
• Cost Analysis: Live cost comparisons and optimization recommendations
• Multi-region Support: Pricing and operations across all AWS regions

RESPONSE GUIDELINES:
• Always specify data comes from real AWS APIs
• Provide specific, actionable recommendations
• Include current pricing and cost implications
• Suggest AWS best practices based on real data

EXAMPLES:
• "According to the current AWS Pricing API..."
• "Real DynamoDB operation shows..."
• "Live pricing data indicates..."

You have access to real AWS services through official MCP servers."""
            )
            
            print(f"✅ Agent ready with {len(all_tools)} AWS tools")
            return True
            
        except Exception as e:
            print(f"❌ Agent setup failed: {e}")
            return False
    
    async def query(self, message: str) -> str:
        """Query AWS systems through the agent"""
        if not self.agent:
            return "❌ Agent not initialized. Run setup_agent() first."
        
        try:
            print(f"🔍 Processing AWS query: {message}")
            response = self.agent(message)
            return response
        except Exception as e:
            return f"❌ Query failed: {str(e)}"
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "mcp_servers_active": len(self.mcp_clients),
            "connected_services": list(self.mcp_clients.keys()),
            "agent_ready": self.agent is not None
        }
    
    def cleanup(self):
        """Cleanup all MCP connections"""
        for name, client in self.mcp_clients.items():
            try:
                if hasattr(client, '__exit__'):
                    # Use as context manager
                    client.__exit__(None, None, None)
                    print(f"✅ Stopped {name} MCP client")
                elif hasattr(client, 'close'):
                    # Use close method if available
                    client.close()
                    print(f"✅ Closed {name} MCP client")
                else:
                    print(f"✅ {name} MCP client cleanup skipped")
            except Exception as e:
                print(f"⚠️ Error stopping {name}: {e}")
        
        self.mcp_clients.clear()


# Pre-defined production scenarios
PRODUCTION_SCENARIOS = [
    {
        "name": "Real-time Pricing Analysis",
        "query": "Get current AWS pricing for EC2 m5.large and t3.medium in us-east-1, compare costs for 24/7 usage"
    },
    {
        "name": "DynamoDB Table Management",
        "query": "Create a DynamoDB table called 'user-sessions' with 'sessionId' as primary key"
    },
    {
        "name": "Cost Optimization",
        "query": "Analyze cost differences between EC2 instance families for web application workloads"
    },
    {
        "name": "Multi-service Analysis",
        "query": "Compare costs: DynamoDB vs RDS for a high-traffic user database"
    }
]


async def run_production_demo():
    """Run production demo with real AWS MCP servers"""
    agent = AWSDevOpsAgent()
    
    try:
        # Setup agent
        success = await agent.setup_agent()
        if not success:
            print("❌ Production setup failed")
            return
        
        print(f"\n🎯 Production Demo - Real AWS Data")
        print("=" * 60)
        
        # Run production scenarios
        for i, scenario in enumerate(PRODUCTION_SCENARIOS, 1):
            print(f"\n📋 Scenario {i}: {scenario['name']}")
            print(f"Query: {scenario['query']}")
            print("-" * 50)
            
            response = await agent.query(scenario['query'])
            print(f"🤖 AWS Response:\n{response}")
            
            # Pause between scenarios
            await asyncio.sleep(1)
            print("\n" + "=" * 60)
        
        # Show status
        status = agent.get_status()
        print(f"\n📊 Final Status:")
        print(f"   • Active MCP servers: {status['mcp_servers_active']}")
        print(f"   • Connected services: {', '.join(status['connected_services'])}")
        
    except Exception as e:
        print(f"❌ Production demo failed: {e}")
    finally:
        agent.cleanup()


async def interactive_mode():
    """Interactive production mode"""
    agent = AWSDevOpsAgent()
    
    try:
        # Setup
        success = await agent.setup_agent()
        if not success:
            return
        
        print(f"\n💡 AWS DevOps Agent Ready!")
        print(f"   Connected to real AWS APIs via official MCP servers")
        print(f"\nTry these queries:")
        print(f"   • 'Get EC2 t3.large pricing in us-west-2'")
        print(f"   • 'Create DynamoDB table for analytics data'")
        print(f"   • 'Compare RDS vs DynamoDB costs'")
        print(f"   • Type 'exit' to quit")
        print()
        
        while True:
            try:
                user_input = input("👤 AWS> ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                response = await agent.query(user_input)
                print(f"🤖 {response}\n")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    except Exception as e:
        print(f"❌ Interactive mode failed: {e}")
    finally:
        agent.cleanup()
        print("\n👋 AWS DevOps Agent shutdown")


async def main():
    """Main entry point"""
    import sys
    
    # Check AWS credentials
    if not (os.getenv("AWS_PROFILE") or os.getenv("AWS_ACCESS_KEY_ID")):
        print("⚠️ AWS credentials not found")
        print("   Configure with: aws configure")
        print("   Or set AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY")
        print()
    
    # Check arguments
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        await run_production_demo()
    else:
        await interactive_mode()


if __name__ == "__main__":
    asyncio.run(main())