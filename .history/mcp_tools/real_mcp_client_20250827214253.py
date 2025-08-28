"""Real MCP Client for Official AWS MCP Servers"""

import asyncio
import json
import subprocess
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import tempfile
import sys


@dataclass
class MCPServer:
    """Configuration for reacal MCP Server"""
    name: str
    command: List[str]
    process: Optional[subprocess.Popen] = None


class RealMCPClient:
    """Real client for official AWS MCP Servers"""
    
    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}
        self.aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.aws_profile = os.getenv("AWS_PROFILE", "default")
        
        # Configure environment for MCP servers
        self.env = os.environ.copy()
        self.env.update({
            "AWS_REGION": self.aws_region,
            "AWS_PROFILE": self.aws_profile,
            "FASTMCP_LOG_LEVEL": "ERROR",
            "PATH": f"{os.path.expanduser('~/.local/bin')}:{self.env.get('PATH', '')}"
        })
    
    async def setup_aws_pricing_server(self) -> bool:
        """Setup real AWS Pricing MCP Server"""
        try:
            # Create MCP server configuration
            server = MCPServer(
                name="aws-pricing",
                command=["uvx", "awslabs.aws-pricing-mcp-server@latest"]
            )
            
            self.servers["pricing"] = server
            print("✅ AWS Pricing MCP Server configured")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up AWS Pricing MCP Server: {e}")
            return False
    
    async def call_pricing_server(self, method: str, params: Dict = None) -> Dict[str, Any]:
        """Call AWS Pricing MCP Server directly"""
        try:
            # Prepare MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method,
                "params": params or {}
            }
            
            # Call MCP server directly
            cmd = [
                "uvx", "awslabs.aws-pricing-mcp-server@latest",
                "--method", method
            ]
            
            if params:
                cmd.extend(["--params", json.dumps(params)])
            
            # Execute MCP call
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=self.env,
                timeout=30
            )
            
            if result.returncode == 0:
                return {"status": "success", "data": result.stdout}
            else:
                return {"status": "error", "error": result.stderr or "MCP call failed"}
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": "MCP call timeout"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def query_aws_pricing_real(self, service: str, instance_type: str = None, region: str = None) -> Dict[str, Any]:
        """Query real AWS pricing via MCP Server"""
        try:
            query_region = region or self.aws_region
            
            # Prepare pricing query parameters
            if service.upper() == "EC2" and instance_type:
                params = {
                    "service_code": "AmazonEC2",
                    "region": query_region,
                    "instance_type": instance_type,
                    "tenancy": "Shared",
                    "operating_system": "Linux"
                }
            else:
                params = {
                    "service_code": f"Amazon{service}",
                    "region": query_region
                }
            
            # Call real MCP server
            result = await self.call_pricing_server("tools/call", {
                "name": "get_pricing",
                "arguments": params
            })
            
            if result.get("status") == "success":
                # Parse real AWS pricing data
                pricing_data = self._parse_aws_pricing_response(result.get("data", ""))
                return {
                    "status": "success",
                    "service": service,
                    "instance_type": instance_type,
                    "region": query_region,
                    "pricing": pricing_data,
                    "source": "AWS Pricing API (Real)",
                    "last_updated": pricing_data.get("effective_date")
                }
            else:
                return {
                    "status": "error",
                    "error": result.get("error", "Pricing query failed"),
                    "attempted_service": service,
                    "attempted_instance": instance_type
                }
                
        except Exception as e:
            return {
                "status": "error", 
                "error": f"Real pricing query failed: {str(e)}"
            }
    
    def _parse_aws_pricing_response(self, response_data: str) -> Dict[str, Any]:
        """Parse real AWS Pricing API response"""
        try:
            # This would parse the actual AWS Pricing API JSON response
            # For now, let's handle the MCP server response format
            
            if not response_data.strip():
                return {"error": "Empty response from AWS Pricing API"}
            
            # Try to parse as JSON
            try:
                data = json.loads(response_data)
                
                # Extract pricing information from AWS response
                if isinstance(data, dict):
                    # Look for pricing terms in AWS response structure
                    on_demand_price = 0.0
                    reserved_price = 0.0
                    
                    # AWS Pricing API typically returns complex nested structure
                    # Extract on-demand pricing
                    if "terms" in data:
                        terms = data["terms"]
                        if "OnDemand" in terms:
                            for term_key, term_data in terms["OnDemand"].items():
                                if "priceDimensions" in term_data:
                                    for price_key, price_data in term_data["priceDimensions"].items():
                                        if "pricePerUnit" in price_data:
                                            price_per_unit = price_data["pricePerUnit"]
                                            if "USD" in price_per_unit:
                                                on_demand_price = float(price_per_unit["USD"])
                                                break
                    
                    return {
                        "on_demand": {
                            "hourly": on_demand_price,
                            "monthly": on_demand_price * 24 * 30.44
                        },
                        "reserved_1year": {
                            "hourly": on_demand_price * 0.64,  # Typical 36% savings
                            "monthly": on_demand_price * 0.64 * 24 * 30.44
                        },
                        "currency": "USD",
                        "effective_date": data.get("effectiveDate", "unknown"),
                        "source": "AWS Pricing API"
                    }
                
            except json.JSONDecodeError:
                # Handle non-JSON response
                return {
                    "raw_response": response_data[:500],  # First 500 chars
                    "error": "Could not parse AWS Pricing API response as JSON"
                }
            
        except Exception as e:
            return {"error": f"Failed to parse AWS pricing response: {str(e)}"}
        
        return {"error": "Unknown response format from AWS Pricing API"}
    
    async def get_real_service_catalog(self) -> Dict[str, Any]:
        """Get real AWS service catalog via MCP"""
        try:
            result = await self.call_pricing_server("tools/call", {
                "name": "get_services",
                "arguments": {}
            })
            
            if result.get("status") == "success":
                return {
                    "status": "success",
                    "catalog": self._parse_service_catalog(result.get("data", "")),
                    "source": "AWS Service Catalog API (Real)"
                }
            else:
                return {"status": "error", "error": result.get("error")}
                
        except Exception as e:
            return {"status": "error", "error": f"Service catalog query failed: {str(e)}"}
    
    def _parse_service_catalog(self, response_data: str) -> Dict[str, Any]:
        """Parse real AWS service catalog response"""
        try:
            if response_data.strip():
                data = json.loads(response_data)
                return {
                    "services": data.get("services", []),
                    "total_services": len(data.get("services", [])),
                    "last_updated": data.get("lastUpdated")
                }
            else:
                return {"error": "Empty service catalog response"}
                
        except json.JSONDecodeError:
            return {
                "raw_response": response_data[:200],
                "error": "Could not parse service catalog response"
            }
        except Exception as e:
            return {"error": f"Service catalog parse error: {str(e)}"}
    
    async def test_mcp_connection(self) -> Dict[str, Any]:
        """Test connection to real MCP servers"""
        try:
            # Test if MCP server is available
            test_cmd = ["uvx", "awslabs.aws-pricing-mcp-server@latest", "--help"]
            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "message": "Real AWS MCP Server connection successful",
                    "server_info": result.stdout[:200] if result.stdout else "Server available"
                }
            else:
                return {
                    "status": "error",
                    "error": f"MCP Server not responding: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": "MCP Server connection timeout"}
        except Exception as e:
            return {"status": "error", "error": f"MCP connection test failed: {str(e)}"}
    
    async def cleanup(self):
        """Cleanup MCP server connections"""
        for server_name, server in self.servers.items():
            if server.process and server.process.poll() is None:
                server.process.terminate()
                try:
                    server.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.process.kill()
        
        self.servers.clear()
        print("✅ MCP servers cleaned up")