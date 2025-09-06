"""
Unified MCP Client for AWS DevOps Agent
Follows Strands SDK best practices and naming conventions
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Import Strands MCP SDK - this is the recommended approach
try:
    from mcp import stdio_client, StdioServerParameters
    from strands.tools.mcp import MCPClient
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️  Strands MCP SDK not available")
    MCP_AVAILABLE = False


class DevOpsMCPClient:
    """
    Unified MCP Client for AWS DevOps operations
    Follows Strands SDK patterns and best practices
    """
    
    def __init__(self):
        self.aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.aws_profile = os.getenv("AWS_PROFILE", "default")
        self.clients: Dict[str, MCPClient] = {}
        
        if not MCP_AVAILABLE:
            raise ImportError("Strands MCP SDK not available")
    
    def get_cost_explorer_client(self) -> Optional[MCPClient]:
        """Get or create Cost Explorer MCP client using Strands pattern"""
        if "cost_explorer" not in self.clients:
            try:
                # Follow Strands documentation pattern exactly
                mcp_client = MCPClient(lambda: stdio_client(
                    StdioServerParameters(
                        command="uvx",
                        args=["awslabs.cost-explorer-mcp-server@latest"],
                        env={
                            "AWS_REGION": self.aws_region,
                            "AWS_PROFILE": self.aws_profile,
                            "AWS_DEFAULT_REGION": self.aws_region,
                            "FASTMCP_LOG_LEVEL": "ERROR"
                        }
                    )
                ))
                
                self.clients["cost_explorer"] = mcp_client
                print("✅ Cost Explorer MCP client created")
                
            except Exception as e:
                print(f"❌ Failed to create Cost Explorer MCP client: {e}")
                return None
        
        return self.clients.get("cost_explorer")
    
    def get_cloudwatch_client(self) -> Optional[MCPClient]:
        """Get or create CloudWatch MCP client using Strands pattern"""
        if "cloudwatch" not in self.clients:
            try:
                mcp_client = MCPClient(lambda: stdio_client(
                    StdioServerParameters(
                        command="uvx",
                        args=["awslabs.cloudwatch-mcp-server@latest"],
                        env={
                            "AWS_REGION": self.aws_region,
                            "AWS_PROFILE": self.aws_profile,
                            "AWS_DEFAULT_REGION": self.aws_region,
                            "FASTMCP_LOG_LEVEL": "ERROR"
                        }
                    )
                ))
                
                self.clients["cloudwatch"] = mcp_client
                print("✅ CloudWatch MCP client created")
                
            except Exception as e:
                print(f"❌ Failed to create CloudWatch MCP client: {e}")
                return None
        
        return self.clients.get("cloudwatch")
    
    def get_pricing_client(self) -> Optional[MCPClient]:
        """Get or create AWS Pricing MCP client using Strands pattern"""
        if "pricing" not in self.clients:
            try:
                mcp_client = MCPClient(lambda: stdio_client(
                    StdioServerParameters(
                        command="uvx",
                        args=["awslabs.aws-pricing-mcp-server@latest"],
                        env={
                            "AWS_REGION": self.aws_region,
                            "AWS_PROFILE": self.aws_profile,
                            "AWS_DEFAULT_REGION": self.aws_region,
                            "FASTMCP_LOG_LEVEL": "ERROR"
                        }
                    )
                ))
                
                self.clients["pricing"] = mcp_client
                print("✅ AWS Pricing MCP client created")
                
            except Exception as e:
                print(f"❌ Failed to create AWS Pricing MCP client: {e}")
                return None
        
        return self.clients.get("pricing")
    
    def get_github_client(self) -> Optional[MCPClient]:
        """Get or create GitHub MCP client using Strands pattern"""
        if "github" not in self.clients:
            try:
                github_token = os.getenv("GITHUB_TOKEN")
                if not github_token:
                    print("⚠️  GITHUB_TOKEN not found in environment")
                    return None
                
                mcp_client = MCPClient(lambda: stdio_client(
                    StdioServerParameters(
                        command="uvx",
                        args=["github.github-mcp-server@latest"],
                        env={
                            "GITHUB_TOKEN": github_token,
                            "FASTMCP_LOG_LEVEL": "ERROR"
                        }
                    )
                ))
                
                self.clients["github"] = mcp_client
                print("✅ GitHub MCP client created")
                
            except Exception as e:
                print(f"❌ Failed to create GitHub MCP client: {e}")
                return None
        
        return self.clients.get("github")
    
    def get_all_clients(self) -> Dict[str, MCPClient]:
        """Get all available MCP clients"""
        return {
            "cost_explorer": self.get_cost_explorer_client(),
            "cloudwatch": self.get_cloudwatch_client(),
            "pricing": self.get_pricing_client(),
            "github": self.get_github_client()
        }
    
    def close_all_clients(self):
        """Close all MCP clients"""
        for name, client in self.clients.items():
            if client:
                try:
                    client.close()
                    print(f"✅ Closed {name} MCP client")
                except Exception as e:
                    print(f"⚠️  Error closing {name} MCP client: {e}")
        
        self.clients.clear()


# Create a singleton instance following Strands patterns
mcp_client = DevOpsMCPClient()
