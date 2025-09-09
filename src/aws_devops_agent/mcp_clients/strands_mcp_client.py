"""
Strands MCP Client for AWS MCP Servers
Uses the Strands MCPClient pattern for proper connection management
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

# Import Strands MCP SDK
try:
    from mcp import stdio_client, StdioServerParameters
    from strands.tools.mcp import MCPClient
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️  Strands MCP SDK not available")
    MCP_AVAILABLE = False


class StrandsMCPClient:
    """
    Strands MCP Client for AWS MCP Servers
    Uses the proper Strands MCPClient pattern
    """
    
    def __init__(self):
        self.aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.aws_profile = os.getenv("AWS_PROFILE", "default")
        self.clients: Dict[str, MCPClient] = {}
        
        if not MCP_AVAILABLE:
            raise ImportError("Strands MCP SDK not available")
    
    def get_cost_explorer_client(self) -> Optional[MCPClient]:
        """Get or create Cost Explorer MCP client"""
        if "cost_explorer" not in self.clients:
            try:
                # Create MCPClient using Strands pattern (like the documentation)
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
                
                # Start the client
                mcp_client.start()
                self.clients["cost_explorer"] = mcp_client
                print("✅ Cost Explorer MCP client started")
                
            except Exception as e:
                print(f"❌ Failed to create Cost Explorer MCP client: {e}")
                return None
        
        return self.clients.get("cost_explorer")
    
    def get_cloudwatch_client(self) -> Optional[MCPClient]:
        """Get or create CloudWatch MCP client"""
        if "cloudwatch" not in self.clients:
            try:
                # Create MCPClient using Strands pattern (like the documentation)
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
                
                # Start the client
                mcp_client.start()
                self.clients["cloudwatch"] = mcp_client
                print("✅ CloudWatch MCP client started")
                
            except Exception as e:
                print(f"❌ Failed to create CloudWatch MCP client: {e}")
                return None
        
        return self.clients.get("cloudwatch")
    
    def get_terraform_client(self) -> Optional[MCPClient]:
        """Get or create Terraform MCP client"""
        if "terraform" not in self.clients:
            try:
                # Create MCPClient using Strands pattern (like the documentation)
                mcp_client = MCPClient(lambda: stdio_client(
                    StdioServerParameters(
                        command="uvx",
                        args=["awslabs.terraform-mcp-server@latest"],
                        env={
                            "AWS_REGION": self.aws_region,
                            "AWS_PROFILE": self.aws_profile,
                            "AWS_DEFAULT_REGION": self.aws_region,
                            "FASTMCP_LOG_LEVEL": "ERROR"
                        }
                    )
                ))
                
                # Start the client
                mcp_client.start()
                self.clients["terraform"] = mcp_client
                print("✅ Terraform MCP client started")
                
            except Exception as e:
                print(f"❌ Failed to create Terraform MCP client: {e}")
                return None
        
        return self.clients.get("terraform")
    
    def get_github_client(self) -> Optional[MCPClient]:
        """Get or create GitHub MCP client"""
        if "github" not in self.clients:
            try:
                # Create MCPClient using Docker approach (when available)
                # For now, we'll create a placeholder that can be implemented later
                print("⚠️  GitHub MCP Server requires Docker or GitHub token setup")
                print("   Configure GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
                print("   Or set up Docker to use ghcr.io/github/github-mcp-server")
                return None
                
                # Future implementation would be:
                # mcp_client = MCPClient(lambda: stdio_client(
                #     StdioServerParameters(
                #         command="docker",
                #         args=["run", "-i", "--rm", 
                #               "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={github_token}",
                #               "ghcr.io/github/github-mcp-server"],
                #         env={"GITHUB_PERSONAL_ACCESS_TOKEN": github_token}
                #     )
                # ))
                
            except Exception as e:
                print(f"❌ Failed to create GitHub MCP client: {e}")
                return None
        
        return self.clients.get("github")
    
    def list_cost_explorer_tools(self) -> List[str]:
        """List available Cost Explorer tools"""
        client = self.get_cost_explorer_client()
        if client:
            try:
                tools = client.list_tools_sync()
                return [tool.name for tool in tools]
            except Exception as e:
                print(f"❌ Failed to list Cost Explorer tools: {e}")
        return []
    
    def list_cloudwatch_tools(self) -> List[str]:
        """List available CloudWatch tools"""
        client = self.get_cloudwatch_client()
        if client:
            try:
                tools = client.list_tools_sync()
                return [tool.name for tool in tools]
            except Exception as e:
                print(f"❌ Failed to list CloudWatch tools: {e}")
        return []
    
    def list_terraform_tools(self) -> List[str]:
        """List available Terraform tools"""
        client = self.get_terraform_client()
        if client:
            try:
                tools = client.list_tools_sync()
                return [getattr(tool, 'name', str(tool)) for tool in tools]
            except Exception as e:
                print(f"❌ Failed to list Terraform tools: {e}")
        return []
    
    def call_cost_tool(self, tool_name: str, arguments: Dict = None) -> Dict[str, Any]:
        """Call a Cost Explorer tool"""
        client = self.get_cost_explorer_client()
        if not client:
            return {"error": "Cost Explorer client not available"}
        
        try:
            result = client.call_tool_sync(tool_name, arguments or {})
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def call_cloudwatch_tool(self, tool_name: str, arguments: Dict = None) -> Dict[str, Any]:
        """Call a CloudWatch tool"""
        client = self.get_cloudwatch_client()
        if not client:
            return {"error": "CloudWatch client not available"}
        
        try:
            result = client.call_tool_sync(tool_name, arguments or {})
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def call_terraform_tool(self, tool_name: str, arguments: Dict = None) -> Dict[str, Any]:
        """Call a Terraform tool"""
        client = self.get_terraform_client()
        if not client:
            return {"error": "Terraform client not available"}
        
        try:
            result = client.call_tool_sync(tool_name, arguments or {})
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_aws_costs(self, days: int = 7) -> Dict[str, Any]:
        """Get AWS costs for the last N days"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        return self.call_cost_tool("get_cost_and_usage", {
            "time_period": {
                "start": start_date,
                "end": end_date
            },
            "granularity": "DAILY",
            "metrics": ["BlendedCost"]
        })
    
    def get_cloudwatch_metrics(self, namespace: str, metric_name: str) -> Dict[str, Any]:
        """Get CloudWatch metrics"""
        return self.call_cloudwatch_tool("get_metric_data", {
            "namespace": namespace,
            "metric_name": metric_name
        })
    
    def analyze_terraform_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Terraform file for best practices and security"""
        return self.call_terraform_tool("analyze_terraform", {
            "file_path": file_path
        })
    
    def terraform_plan(self, directory: str) -> Dict[str, Any]:
        """Run terraform plan on a directory"""
        return self.call_terraform_tool("terraform_plan", {
            "directory": directory
        })
    
    def terraform_validate(self, directory: str) -> Dict[str, Any]:
        """Validate Terraform configuration"""
        return self.call_terraform_tool("terraform_validate", {
            "directory": directory
        })
    
    def checkov_scan(self, directory: str) -> Dict[str, Any]:
        """Run Checkov security scan on Terraform files"""
        return self.call_terraform_tool("checkov_scan", {
            "directory": directory
        })
    
    def cleanup(self):
        """Cleanup MCP client connections"""
        for name, client in self.clients.items():
            try:
                if hasattr(client, 'stop'):
                    client.stop()
                print(f"✅ {name} MCP client stopped")
            except Exception as e:
                print(f"⚠️  Error stopping {name} client: {e}")
        
        self.clients.clear()


# Global instance
strands_mcp_client = None

def get_mcp_client() -> StrandsMCPClient:
    """Get the global Strands MCP client instance"""
    global strands_mcp_client
    if strands_mcp_client is None:
        strands_mcp_client = StrandsMCPClient()
    return strands_mcp_client