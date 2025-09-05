"""
Real MCP Client for AWS MCP Servers
Uses the official MCP Python SDK to connect to AWS MCP servers
"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Import official MCP SDK
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("⚠️  MCP SDK not available. Please install: pip install mcp")
    # Fallback imports for development
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None


class AWSMCPClient:
    """
    Official MCP Client for AWS MCP Servers
    Uses the official MCP Python SDK instead of subprocess calls
    """
    
    def __init__(self):
        self.aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.aws_profile = os.getenv("AWS_PROFILE", "default")
        self.sessions: Dict[str, Any] = {}
        self._transports: Dict[str, Any] = {}
        
        # Configure environment for MCP servers
        self.env = os.environ.copy()
        self.env.update({
            "AWS_REGION": self.aws_region,
            "AWS_PROFILE": self.aws_profile,
            "AWS_DEFAULT_REGION": self.aws_region,
            "PATH": f"/root/.local/bin:{self.env.get('PATH', '')}"
        })
    
    async def get_cost_explorer_session(self) -> Optional[ClientSession]:
        """Get or create Cost Explorer MCP session"""
        if "cost_explorer" not in self.sessions:
            try:
                # Create stdio server parameters for Cost Explorer MCP
                server_params = StdioServerParameters(
                    command="/root/.local/bin/awslabs.cost-explorer-mcp-server",
                    env=self.env
                )
                
                # Create client session - stdio_client returns async context manager
                transport = stdio_client(server_params)
                read, write = await transport.__aenter__()
                session = ClientSession(read, write)
                await session.initialize()
                self.sessions["cost_explorer"] = session
                # Store transport for cleanup
                self._transports["cost_explorer"] = transport
                
            except Exception as e:
                print(f"❌ Failed to create Cost Explorer MCP session: {e}")
                return None
        
        return self.sessions.get("cost_explorer")
    
    async def get_cloudwatch_session(self) -> Optional[ClientSession]:
        """Get or create CloudWatch MCP session"""
        if "cloudwatch" not in self.sessions:
            try:
                # Create stdio server parameters for CloudWatch MCP
                server_params = StdioServerParameters(
                    command="/root/.local/bin/awslabs.cloudwatch-mcp-server",
                    env=self.env
                )
                
                # Create client session - stdio_client returns async context manager
                transport = stdio_client(server_params)
                read, write = await transport.__aenter__()
                session = ClientSession(read, write)
                await session.initialize()
                self.sessions["cloudwatch"] = session
                # Store transport for cleanup
                self._transports["cloudwatch"] = transport
                
            except Exception as e:
                print(f"❌ Failed to create CloudWatch MCP session: {e}")
                return None
        
        return self.sessions.get("cloudwatch")
    
    async def call_cost_explorer_tool(self, tool_name: str, arguments: Dict = None) -> Dict[str, Any]:
        """
        Call AWS Cost Explorer MCP Server tool using official MCP client
        
        Args:
            tool_name: Name of the MCP tool to call
            arguments: Tool arguments
            
        Returns:
            Dict containing MCP response
        """
        try:
            session = await self.get_cost_explorer_session()
            if not session:
                return {
                    "status": "error",
                    "error": "Could not establish Cost Explorer MCP session"
                }
            
            # Call the tool via MCP client
            result = await session.call_tool(tool_name, arguments or {})
            
            return {
                "status": "success",
                "data": result.content,
                "source": "AWS Cost Explorer MCP Server (Official Client)",
                "tool_called": tool_name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Cost Explorer MCP call failed: {str(e)}",
                "tool": tool_name
            }
    
    async def call_cloudwatch_tool(self, tool_name: str, arguments: Dict = None) -> Dict[str, Any]:
        """
        Call AWS CloudWatch MCP Server tool using official MCP client
        
        Args:
            tool_name: Name of the MCP tool to call
            arguments: Tool arguments
            
        Returns:
            Dict containing MCP response
        """
        try:
            session = await self.get_cloudwatch_session()
            if not session:
                return {
                    "status": "error",
                    "error": "Could not establish CloudWatch MCP session"
                }
            
            # Call the tool via MCP client
            result = await session.call_tool(tool_name, arguments or {})
            
            return {
                "status": "success",
                "data": result.content,
                "source": "AWS CloudWatch MCP Server (Official Client)",
                "tool_called": tool_name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"CloudWatch MCP call failed: {str(e)}",
                "tool": tool_name
            }
    
    async def get_cost_and_usage(
        self,
        start_date: str,
        end_date: str,
        granularity: str = "DAILY",
        group_by: List[str] = None,
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get AWS cost and usage data using official MCP client
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            granularity: DAILY, MONTHLY, or HOURLY
            group_by: List of dimensions to group by
            metrics: List of metrics to retrieve
            
        Returns:
            Dict containing cost and usage data
        """
        if group_by is None:
            group_by = ["SERVICE"]
        
        if metrics is None:
            metrics = ["BlendedCost", "UsageQuantity"]
        
        arguments = {
            "time_period": {
                "start": start_date,
                "end": end_date
            },
            "granularity": granularity,
            "metrics": metrics,
            "group_by": [{"type": "DIMENSION", "key": gb} for gb in group_by]
        }
        
        return await self.call_cost_explorer_tool("get_cost_and_usage", arguments)
    
    async def get_cost_forecast(
        self,
        start_date: str,
        end_date: str,
        metric: str = "BLENDED_COST",
        granularity: str = "DAILY"
    ) -> Dict[str, Any]:
        """
        Get AWS cost forecast using official MCP client
        
        Args:
            start_date: Forecast start date (YYYY-MM-DD)
            end_date: Forecast end date (YYYY-MM-DD)
            metric: Metric to forecast
            granularity: DAILY or MONTHLY
            
        Returns:
            Dict containing forecast data
        """
        arguments = {
            "time_period": {
                "start": start_date,
                "end": end_date
            },
            "metric": metric,
            "granularity": granularity
        }
        
        return await self.call_cost_explorer_tool("get_cost_forecast", arguments)
    
    async def get_metric_data(
        self,
        namespace: str,
        metric_name: str,
        dimensions: List[Dict] = None,
        start_time: str = None,
        end_time: str = None,
        period: int = 300
    ) -> Dict[str, Any]:
        """
        Get CloudWatch metric data using official MCP client
        
        Args:
            namespace: CloudWatch namespace (e.g., AWS/EC2)
            metric_name: Name of the metric
            dimensions: List of dimension filters
            start_time: Start time (ISO format)
            end_time: End time (ISO format)
            period: Period in seconds
            
        Returns:
            Dict containing metric data
        """
        if start_time is None:
            start_time = (datetime.now() - timedelta(hours=1)).isoformat()
        
        if end_time is None:
            end_time = datetime.now().isoformat()
        
        arguments = {
            "namespace": namespace,
            "metric_name": metric_name,
            "start_time": start_time,
            "end_time": end_time,
            "period": period
        }
        
        if dimensions:
            arguments["dimensions"] = dimensions
        
        return await self.call_cloudwatch_tool("get_metric_data", arguments)
    
    async def get_active_alarms(
        self,
        state_value: str = "ALARM",
        max_records: int = 100
    ) -> Dict[str, Any]:
        """
        Get active CloudWatch alarms using official MCP client
        
        Args:
            state_value: Alarm state to filter (ALARM, OK, INSUFFICIENT_DATA)
            max_records: Maximum number of alarms to return
            
        Returns:
            Dict containing alarm data
        """
        arguments = {
            "state_value": state_value,
            "max_records": max_records
        }
        
        return await self.call_cloudwatch_tool("get_active_alarms", arguments)
    
    async def execute_log_insights_query(
        self,
        log_group_name: str,
        query_string: str,
        start_time: int = None,
        end_time: int = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Execute CloudWatch Logs Insights query using official MCP client
        
        Args:
            log_group_name: Name of the log group
            query_string: CloudWatch Insights query
            start_time: Start time (Unix timestamp)
            end_time: End time (Unix timestamp)
            limit: Maximum number of results
            
        Returns:
            Dict containing query results
        """
        if start_time is None:
            start_time = int((datetime.now() - timedelta(hours=1)).timestamp())
        
        if end_time is None:
            end_time = int(datetime.now().timestamp())
        
        arguments = {
            "log_group_name": log_group_name,
            "query_string": query_string,
            "start_time": start_time,
            "end_time": end_time,
            "limit": limit
        }
        
        return await self.call_cloudwatch_tool("execute_log_insights_query", arguments)
    
    async def list_available_tools(self, server_type: str = "cost_explorer") -> Dict[str, Any]:
        """
        List available tools from MCP server
        
        Args:
            server_type: "cost_explorer" or "cloudwatch"
            
        Returns:
            Dict containing available tools
        """
        try:
            if server_type == "cost_explorer":
                session = await self.get_cost_explorer_session()
            elif server_type == "cloudwatch":
                session = await self.get_cloudwatch_session()
            else:
                return {
                    "status": "error",
                    "error": f"Unknown server type: {server_type}"
                }
            
            if not session:
                return {
                    "status": "error",
                    "error": f"Could not establish {server_type} MCP session"
                }
            
            # List tools available in the session
            tools = session.list_tools()
            
            return {
                "status": "success",
                "server_type": server_type,
                "tools": [tool.name for tool in tools],
                "source": f"AWS {server_type.replace('_', ' ').title()} MCP Server"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to list tools from {server_type}: {str(e)}"
            }
    
    async def close_sessions(self):
        """Close all MCP sessions"""
        for session_name, session in self.sessions.items():
            try:
                if hasattr(session, 'close'):
                    await session.close()
                elif hasattr(session, '__aexit__'):
                    await session.__aexit__(None, None, None)
            except Exception as e:
                print(f"⚠️  Error closing {session_name} session: {e}")
        
        self.sessions.clear()
        print("✅ All MCP sessions closed")


# Create global MCP client instance
mcp_client = AWSMCPClient()


# Utility functions for easier usage
async def get_aws_costs_mcp(days_back: int = 30, granularity: str = "DAILY") -> Dict[str, Any]:
    """Utility function to get AWS costs using MCP client"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)
    
    return await mcp_client.get_cost_and_usage(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d'),
        granularity
    )


async def get_ec2_metrics_mcp(instance_ids: List[str] = None, hours_back: int = 24) -> Dict[str, Any]:
    """Utility function to get EC2 metrics using MCP client"""
    dimensions = []
    if instance_ids:
        dimensions = [{"Name": "InstanceId", "Value": iid} for iid in instance_ids]
    
    return await mcp_client.get_metric_data(
        namespace="AWS/EC2",
        metric_name="CPUUtilization", 
        dimensions=dimensions,
        start_time=(datetime.now() - timedelta(hours=hours_back)).isoformat(),
        end_time=datetime.now().isoformat()
    )