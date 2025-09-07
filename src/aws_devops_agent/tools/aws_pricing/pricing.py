"""
AWS Pricing Tools
Real-time AWS pricing data via MCP servers
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from strands import tool

# Import MCP client for real AWS data
import sys
from pathlib import Path
# MCP clients are now in the same package structure

try:
    from ...mcp_clients.mcp_client import mcp_client
except ImportError:
    print("Warning: MCP client not available, using mock data")
    mcp_client = None


@tool
def get_real_aws_pricing(service: str, instance_type: str = None, region: str = "us-east-1") -> Dict[str, Any]:
    """
    Get real-time AWS pricing data via MCP servers
    
    Args:
        service: AWS service name (e.g., 'EC2', 'RDS', 'Lambda')
        instance_type: Specific instance type (e.g., 't3.medium', 'db.r5.large')
        region: AWS region (default: us-east-1)
    
    Returns:
        Dict containing real AWS pricing data from Pricing API
    """
    try:
        if mcp_client:
            # Use real MCP client for live AWS pricing
            pricing_client = mcp_client.get_pricing_client()
            if pricing_client:
                with pricing_client:
                    # Use Strands MCP pattern to get pricing data
                    tools = pricing_client.list_tools_sync()
                    # Find pricing tool and call it
                    for tool in tools:
                        if hasattr(tool, 'name') and 'pricing' in tool.name.lower():
                            result = pricing_client.call_tool_sync(
                                tool_use_id="pricing-query",
                                name=tool.name,
                                arguments={
                                    "service": service,
                                    "instance_type": instance_type,
                                    "region": region
                                }
                            )
            
            if result.get("status") == "success":
                return {
                    "status": "success",
                    "service": service,
                    "instance_type": instance_type,
                    "region": region,
                    "pricing_data": result.get("pricing", {}),
                    "source": "AWS Pricing API (Real-time)",
                    "last_updated": datetime.now().isoformat(),
                    "savings_opportunities": _calculate_savings_opportunities(result.get("pricing", {}))
                }
            else:
                return {"status": "error", "error": result.get("error", "Pricing query failed")}
        else:
            # Fallback mock data for testing
            return _get_mock_pricing_data(service, instance_type, region)
            
    except Exception as e:
        return {"status": "error", "error": f"Failed to get AWS pricing: {str(e)}"}


@tool
def calculate_reserved_instance_savings(instance_types: List[str], usage_hours_per_month: int = 730, region: str = "us-east-1") -> Dict[str, Any]:
    """
    Calculate potential savings with Reserved Instances
    
    Args:
        instance_types: List of EC2 instance types
        usage_hours_per_month: Expected monthly usage hours (default: 730 = 24/7)
        region: AWS region
    
    Returns:
        Dict containing Reserved Instance savings analysis
    """
    try:
        ri_analysis = []
        total_on_demand_cost = 0
        total_reserved_cost = 0
        
        for instance_type in instance_types:
            pricing_result = get_real_aws_pricing("EC2", instance_type, region)
            
            if pricing_result.get("status") == "success":
                pricing_data = pricing_result.get("pricing_data", {})
                
                hourly_on_demand = pricing_data.get("on_demand", {}).get("hourly", 0)
                hourly_reserved = pricing_data.get("reserved_1year", {}).get("hourly", 0)
                
                monthly_on_demand = hourly_on_demand * usage_hours_per_month
                monthly_reserved = hourly_reserved * usage_hours_per_month
                monthly_savings = monthly_on_demand - monthly_reserved
                
                total_on_demand_cost += monthly_on_demand
                total_reserved_cost += monthly_reserved
                
                ri_analysis.append({
                    "instance_type": instance_type,
                    "hourly_on_demand": hourly_on_demand,
                    "hourly_reserved_1year": hourly_reserved,
                    "monthly_on_demand": round(monthly_on_demand, 2),
                    "monthly_reserved_1year": round(monthly_reserved, 2),
                    "monthly_savings": round(monthly_savings, 2),
                    "annual_savings": round(monthly_savings * 12, 2),
                    "savings_percentage": round((monthly_savings / monthly_on_demand) * 100, 1) if monthly_on_demand > 0 else 0
                })
        
        total_monthly_savings = total_on_demand_cost - total_reserved_cost
        
        return {
            "status": "success",
            "analysis_region": region,
            "usage_hours_per_month": usage_hours_per_month,
            "instance_analysis": ri_analysis,
            "summary": {
                "total_monthly_on_demand_cost": round(total_on_demand_cost, 2),
                "total_monthly_reserved_cost": round(total_reserved_cost, 2),
                "total_monthly_savings": round(total_monthly_savings, 2),
                "total_annual_savings": round(total_monthly_savings * 12, 2),
                "overall_savings_percentage": round((total_monthly_savings / total_on_demand_cost) * 100, 1) if total_on_demand_cost > 0 else 0
            },
            "recommendation": "Consider Reserved Instances for consistent workloads running 24/7" if total_monthly_savings > 100 else "Reserved Instances may not provide significant savings for current usage pattern",
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "Real AWS Pricing API"
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Reserved Instance analysis failed: {str(e)}"}


@tool
def get_service_pricing_overview(service: str, region: str = "us-east-1") -> Dict[str, Any]:
    """
    Get comprehensive pricing overview for an AWS service
    
    Args:
        service: AWS service name (e.g., 'EC2', 'RDS', 'Lambda')
        region: AWS region (default: us-east-1)
    
    Returns:
        Dict containing service pricing overview
    """
    try:
        if mcp_client:
            # Use real MCP client for service pricing overview
            pricing_client = mcp_client.get_pricing_client()
            if pricing_client:
                with pricing_client:
                    tools = pricing_client.list_tools_sync()
                    for tool in tools:
                        if hasattr(tool, 'name') and 'service_pricing' in tool.name.lower():
                            result = pricing_client.call_tool_sync(
                                tool_use_id="service-pricing-overview",
                                name=tool.name,
                                arguments={
                                    "service": service,
                                    "region": region
                                }
                            )
            
            if result.get("status") == "success":
                return {
                    "status": "success",
                    "service": service,
                    "region": region,
                    "pricing_overview": result.get("overview", {}),
                    "popular_configurations": result.get("popular_configs", []),
                    "source": "AWS Pricing API (Real-time)",
                    "last_updated": datetime.now().isoformat()
                }
            else:
                return {"status": "error", "error": result.get("error", "Service pricing query failed")}
        else:
            # Fallback mock data for testing
            return _get_mock_service_overview(service, region)
            
    except Exception as e:
        return {"status": "error", "error": f"Failed to get service pricing overview: {str(e)}"}


# Helper functions
def _calculate_savings_opportunities(pricing_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Calculate potential savings opportunities from pricing data"""
    opportunities = []
    
    if "on_demand" in pricing_data and "reserved_1year" in pricing_data:
        on_demand_monthly = pricing_data["on_demand"].get("monthly", 0)
        reserved_monthly = pricing_data["reserved_1year"].get("monthly", 0)
        
        if on_demand_monthly > reserved_monthly:
            opportunities.append({
                "opportunity": "Reserved Instance (1-year)",
                "monthly_savings": round(on_demand_monthly - reserved_monthly, 2),
                "annual_savings": round((on_demand_monthly - reserved_monthly) * 12, 2),
                "savings_percentage": round(((on_demand_monthly - reserved_monthly) / on_demand_monthly) * 100, 1)
            })
    
    return opportunities


def _get_mock_pricing_data(service: str, instance_type: str, region: str) -> Dict[str, Any]:
    """Mock pricing data for testing when MCP client is not available"""
    mock_pricing = {
        "on_demand": {"hourly": 0.096, "monthly": 70.08},
        "reserved_1year": {"hourly": 0.062, "monthly": 45.26},
        "currency": "USD"
    }
    
    return {
        "status": "success",
        "service": service,
        "instance_type": instance_type,
        "region": region,
        "pricing_data": mock_pricing,
        "source": "Mock data for testing",
        "last_updated": datetime.now().isoformat(),
        "savings_opportunities": _calculate_savings_opportunities(mock_pricing)
    }


def _get_mock_service_overview(service: str, region: str) -> Dict[str, Any]:
    """Mock service overview for testing"""
    return {
        "status": "success",
        "service": service,
        "region": region,
        "pricing_overview": {
            "pricing_model": "Pay-as-you-go",
            "minimum_charge": "$0.00",
            "billing_granularity": "Per second"
        },
        "popular_configurations": [
            {"type": "t3.micro", "monthly_cost": "$8.47"},
            {"type": "t3.small", "monthly_cost": "$16.93"},
            {"type": "t3.medium", "monthly_cost": "$33.87"}
        ],
        "source": "Mock data for testing",
        "last_updated": datetime.now().isoformat()
    }