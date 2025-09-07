"""
AWS Cost Explorer Integration
Real AWS Cost Explorer data access via MCP servers
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from strands import tool

# Import MCP client for real AWS Cost Explorer data
try:
    from ...mcp_clients.mcp_client import mcp_client
except ImportError:
    print("Warning: MCP client not available, using mock data")
    mcp_client = None


@tool
def get_actual_aws_costs(
    time_period_days: int = 30,
    granularity: str = "DAILY",
    group_by: List[str] = None,
    account_id: str = None
) -> Dict[str, Any]:
    """
    Get actual AWS costs from Cost Explorer API via MCP server
    
    Args:
        time_period_days: Number of days to look back (default: 30)
        granularity: DAILY, MONTHLY, or HOURLY
        group_by: List of dimensions to group by (SERVICE, ACCOUNT, REGION, etc.)
        account_id: Specific account ID (if None, uses current account)
    
    Returns:
        Dict containing real AWS cost data from Cost Explorer
    """
    try:
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=time_period_days)
        
        if mcp_client:
            # Use real MCP client for Cost Explorer data
            cost_client = mcp_client.get_cost_explorer_client()
            if cost_client:
                with cost_client:
                    # Use Cost Explorer MCP pattern to get cost data
                    tools = cost_client.list_tools_sync()
                    
                    # Find cost and usage tool
                    for tool in tools:
                        if hasattr(tool, 'name') and 'cost_and_usage' in tool.name.lower():
                            result = cost_client.call_tool_sync(
                                tool_use_id="cost-query",
                                name=tool.name,
                                arguments={
                                    "time_period": {
                                        "start": start_date.strftime("%Y-%m-%d"),
                                        "end": end_date.strftime("%Y-%m-%d")
                                    },
                                    "granularity": granularity,
                                    "metrics": ["BlendedCost", "UnblendedCost", "UsageQuantity"],
                                    "group_by": group_by or [],
                                    "account_id": account_id
                                }
                            )
                            break
            
            if result and result.get("status") == "success":
                return {
                    "status": "success",
                    "time_period": {
                        "start": start_date.strftime("%Y-%m-%d"),
                        "end": end_date.strftime("%Y-%m-%d"),
                        "days": time_period_days
                    },
                    "granularity": granularity,
                    "group_by": group_by or [],
                    "cost_data": result.get("results", []),
                    "total_cost": result.get("total_cost", 0),
                    "currency": "USD",
                    "source": "AWS Cost Explorer API (Real-time)",
                    "retrieved_at": datetime.now().isoformat()
                }
            else:
                return {"status": "error", "error": result.get("error", "Cost query failed") if result else "No result from cost client"}
        else:
            # Fallback mock data for testing
            return _get_mock_cost_data(time_period_days, granularity, group_by)
            
    except Exception as e:
        return {"status": "error", "error": f"Failed to get AWS costs: {str(e)}"}


@tool
def get_cost_by_service(
    time_period_days: int = 30,
    top_n: int = 10,
    account_id: str = None
) -> Dict[str, Any]:
    """
    Get AWS costs broken down by service
    
    Args:
        time_period_days: Number of days to look back
        top_n: Number of top services to return
        account_id: Specific account ID
    
    Returns:
        Dict containing cost breakdown by AWS service
    """
    try:
        cost_data = get_actual_aws_costs(
            time_period_days=time_period_days,
            granularity="MONTHLY",
            group_by=["SERVICE"],
            account_id=account_id
        )
        
        if cost_data.get("status") != "success":
            return cost_data
        
        # Process and aggregate by service
        service_costs = {}
        for record in cost_data.get("cost_data", []):
            service_name = record.get("group", {}).get("SERVICE", "Unknown")
            cost = float(record.get("amount", 0))
            
            if service_name in service_costs:
                service_costs[service_name] += cost
            else:
                service_costs[service_name] = cost
        
        # Sort by cost and get top N
        sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
        top_services = sorted_services[:top_n]
        
        total_cost = sum(service_costs.values())
        
        return {
            "status": "success",
            "time_period_days": time_period_days,
            "total_cost": round(total_cost, 2),
            "currency": "USD",
            "top_services": [
                {
                    "service": service,
                    "cost": round(cost, 2),
                    "percentage": round((cost / total_cost) * 100, 1) if total_cost > 0 else 0
                }
                for service, cost in top_services
            ],
            "analysis_timestamp": datetime.now().isoformat(),
            "source": "AWS Cost Explorer API"
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Failed to get cost by service: {str(e)}"}


@tool
def get_cost_trends(
    time_period_days: int = 90,
    granularity: str = "DAILY"
) -> Dict[str, Any]:
    """
    Get cost trends over time
    
    Args:
        time_period_days: Number of days to analyze
        granularity: DAILY, WEEKLY, or MONTHLY
    
    Returns:
        Dict containing cost trend analysis
    """
    try:
        cost_data = get_actual_aws_costs(
            time_period_days=time_period_days,
            granularity=granularity,
            group_by=[]
        )
        
        if cost_data.get("status") != "success":
            return cost_data
        
        # Process trend data
        trends = []
        for record in cost_data.get("cost_data", []):
            trends.append({
                "date": record.get("time_period", {}).get("start"),
                "cost": float(record.get("amount", 0))
            })
        
        # Sort by date
        trends.sort(key=lambda x: x["date"])
        
        # Calculate trend analysis
        if len(trends) >= 2:
            recent_avg = sum(t["cost"] for t in trends[-7:]) / min(7, len(trends))
            older_avg = sum(t["cost"] for t in trends[:7]) / min(7, len(trends))
            trend_direction = "increasing" if recent_avg > older_avg else "decreasing"
            trend_percentage = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        else:
            trend_direction = "insufficient_data"
            trend_percentage = 0
        
        return {
            "status": "success",
            "time_period_days": time_period_days,
            "granularity": granularity,
            "trend_data": trends,
            "trend_analysis": {
                "direction": trend_direction,
                "percentage_change": round(trend_percentage, 1),
                "recent_7_day_avg": round(recent_avg, 2) if len(trends) >= 2 else 0,
                "older_7_day_avg": round(older_avg, 2) if len(trends) >= 2 else 0
            },
            "total_cost": round(sum(t["cost"] for t in trends), 2),
            "average_daily_cost": round(sum(t["cost"] for t in trends) / len(trends), 2) if trends else 0,
            "analysis_timestamp": datetime.now().isoformat(),
            "source": "AWS Cost Explorer API"
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Failed to get cost trends: {str(e)}"}


@tool
def get_rightsizing_recommendations() -> Dict[str, Any]:
    """
    Get AWS rightsizing recommendations from Cost Explorer
    
    Returns:
        Dict containing rightsizing recommendations
    """
    try:
        if mcp_client:
            # Use real MCP client for rightsizing recommendations
            cost_client = mcp_client.get_cost_explorer_client()
            if cost_client:
                with cost_client:
                    tools = cost_client.list_tools_sync()
                    
                    # Find rightsizing recommendations tool
                    for tool in tools:
                        if hasattr(tool, 'name') and 'rightsizing' in tool.name.lower():
                            result = cost_client.call_tool_sync(
                                tool_use_id="rightsizing-query",
                                name=tool.name,
                                arguments={
                                    "service": "EC2-Instance",
                                    "configuration": {
                                        "benefits_considered": True,
                                        "recommendation_target": "SAME_INSTANCE_FAMILY"
                                    }
                                }
                            )
                            break
            
            if result and result.get("status") == "success":
                recommendations = result.get("recommendations", [])
                
                # Process recommendations
                processed_recommendations = []
                total_savings = 0
                
                for rec in recommendations:
                    monthly_savings = float(rec.get("estimated_monthly_savings", 0))
                    total_savings += monthly_savings
                    
                    processed_recommendations.append({
                        "resource_id": rec.get("resource_id"),
                        "current_instance": rec.get("current_instance_type"),
                        "recommended_instance": rec.get("recommended_instance_type"),
                        "estimated_monthly_savings": round(monthly_savings, 2),
                        "estimated_annual_savings": round(monthly_savings * 12, 2),
                        "cpu_utilization": rec.get("resource_details", {}).get("cpu_utilization"),
                        "memory_utilization": rec.get("resource_details", {}).get("memory_utilization"),
                        "network_utilization": rec.get("resource_details", {}).get("network_utilization")
                    })
                
                return {
                    "status": "success",
                    "total_recommendations": len(processed_recommendations),
                    "total_estimated_monthly_savings": round(total_savings, 2),
                    "total_estimated_annual_savings": round(total_savings * 12, 2),
                    "recommendations": processed_recommendations,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "source": "AWS Cost Explorer Rightsizing Recommendations"
                }
            else:
                return {"status": "error", "error": result.get("error", "Rightsizing query failed") if result else "No result from cost client"}
        else:
            # Fallback mock data
            return _get_mock_rightsizing_recommendations()
            
    except Exception as e:
        return {"status": "error", "error": f"Failed to get rightsizing recommendations: {str(e)}"}


@tool
def get_reserved_instance_recommendations() -> Dict[str, Any]:
    """
    Get Reserved Instance recommendations from Cost Explorer
    
    Returns:
        Dict containing RI purchase recommendations
    """
    try:
        if mcp_client:
            # Use real MCP client for RI recommendations
            cost_client = mcp_client.get_cost_explorer_client()
            if cost_client:
                with cost_client:
                    tools = cost_client.list_tools_sync()
                    
                    # Find RI recommendations tool
                    for tool in tools:
                        if hasattr(tool, 'name') and 'reserved_instance' in tool.name.lower():
                            result = cost_client.call_tool_sync(
                                tool_use_id="ri-recommendations-query",
                                name=tool.name,
                                arguments={
                                    "service": "EC2-Instance",
                                    "account_scope": "PAYER",
                                    "lookback_period": "SEVEN_DAYS",
                                    "term_in_years": "ONE_YEAR",
                                    "payment_option": "PARTIAL_UPFRONT"
                                }
                            )
                            break
            
            if result and result.get("status") == "success":
                recommendations = result.get("recommendations", [])
                
                # Process RI recommendations
                processed_recommendations = []
                total_savings = 0
                
                for rec in recommendations:
                    monthly_savings = float(rec.get("estimated_monthly_savings", 0))
                    total_savings += monthly_savings
                    
                    processed_recommendations.append({
                        "instance_type": rec.get("instance_details", {}).get("instance_type"),
                        "platform": rec.get("instance_details", {}).get("platform"),
                        "region": rec.get("instance_details", {}).get("region"),
                        "recommended_quantity": rec.get("recommended_quantity_to_purchase"),
                        "estimated_monthly_savings": round(monthly_savings, 2),
                        "estimated_annual_savings": round(monthly_savings * 12, 2),
                        "upfront_cost": round(float(rec.get("upfront_cost", 0)), 2),
                        "monthly_recurring_cost": round(float(rec.get("recurring_standard_monthly_cost", 0)), 2),
                        "break_even_months": rec.get("estimated_break_even_months"),
                        "average_utilization": rec.get("average_utilization")
                    })
                
                return {
                    "status": "success",
                    "total_recommendations": len(processed_recommendations),
                    "total_estimated_monthly_savings": round(total_savings, 2),
                    "total_estimated_annual_savings": round(total_savings * 12, 2),
                    "recommendations": processed_recommendations,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "source": "AWS Cost Explorer RI Recommendations"
                }
            else:
                return {"status": "error", "error": result.get("error", "RI recommendations query failed") if result else "No result from cost client"}
        else:
            # Fallback mock data
            return _get_mock_ri_recommendations()
            
    except Exception as e:
        return {"status": "error", "error": f"Failed to get RI recommendations: {str(e)}"}


@tool
def analyze_cost_anomalies(
    time_period_days: int = 30,
    total_impact_threshold: float = 100.0
) -> Dict[str, Any]:
    """
    Analyze cost anomalies using Cost Anomaly Detection
    
    Args:
        time_period_days: Number of days to analyze
        total_impact_threshold: Minimum impact threshold for anomalies
    
    Returns:
        Dict containing cost anomaly analysis
    """
    try:
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=time_period_days)
        
        if mcp_client:
            # Use real MCP client for anomaly detection
            cost_client = mcp_client.get_cost_explorer_client()
            if cost_client:
                with cost_client:
                    tools = cost_client.list_tools_sync()
                    
                    # Find anomaly detection tool
                    for tool in tools:
                        if hasattr(tool, 'name') and 'anomal' in tool.name.lower():
                            result = cost_client.call_tool_sync(
                                tool_use_id="anomaly-query",
                                name=tool.name,
                                arguments={
                                    "date_interval": {
                                        "start_date": start_date.strftime("%Y-%m-%d"),
                                        "end_date": end_date.strftime("%Y-%m-%d")
                                    },
                                    "total_impact_threshold": total_impact_threshold
                                }
                            )
                            break
            
            if result and result.get("status") == "success":
                anomalies = result.get("anomalies", [])
                
                # Process anomalies
                processed_anomalies = []
                total_impact = 0
                
                for anomaly in anomalies:
                    impact = float(anomaly.get("impact", {}).get("total_impact", 0))
                    total_impact += impact
                    
                    processed_anomalies.append({
                        "anomaly_id": anomaly.get("anomaly_id"),
                        "anomaly_start_date": anomaly.get("anomaly_start_date"),
                        "anomaly_end_date": anomaly.get("anomaly_end_date"),
                        "dimension_key": anomaly.get("dimension_key"),
                        "total_impact": round(impact, 2),
                        "max_impact": round(float(anomaly.get("impact", {}).get("max_impact", 0)), 2),
                        "feedback_status": anomaly.get("feedback", "NO_FEEDBACK"),
                        "root_causes": anomaly.get("root_causes", [])
                    })
                
                return {
                    "status": "success",
                    "time_period": {
                        "start": start_date.strftime("%Y-%m-%d"),
                        "end": end_date.strftime("%Y-%m-%d"),
                        "days": time_period_days
                    },
                    "total_anomalies": len(processed_anomalies),
                    "total_impact": round(total_impact, 2),
                    "anomalies": processed_anomalies,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "source": "AWS Cost Anomaly Detection"
                }
            else:
                return {"status": "error", "error": result.get("error", "Anomaly query failed") if result else "No result from cost client"}
        else:
            # Fallback mock data
            return _get_mock_anomaly_data(time_period_days)
            
    except Exception as e:
        return {"status": "error", "error": f"Failed to analyze cost anomalies: {str(e)}"}


# Helper functions for mock data
def _get_mock_cost_data(time_period_days: int, granularity: str, group_by: List[str]) -> Dict[str, Any]:
    """Mock cost data for testing"""
    mock_results = []
    
    if granularity == "DAILY":
        for i in range(time_period_days):
            date = (datetime.now().date() - timedelta(days=i)).strftime("%Y-%m-%d")
            mock_results.append({
                "time_period": {"start": date, "end": date},
                "amount": round(50 + (i * 2.5), 2),
                "currency": "USD"
            })
    
    return {
        "status": "success",
        "time_period": {
            "start": (datetime.now().date() - timedelta(days=time_period_days)).strftime("%Y-%m-%d"),
            "end": datetime.now().date().strftime("%Y-%m-%d"),
            "days": time_period_days
        },
        "granularity": granularity,
        "cost_data": mock_results,
        "total_cost": sum(float(r["amount"]) for r in mock_results),
        "source": "Mock data for testing"
    }


def _get_mock_rightsizing_recommendations() -> Dict[str, Any]:
    """Mock rightsizing recommendations"""
    return {
        "status": "success",
        "total_recommendations": 3,
        "total_estimated_monthly_savings": 245.67,
        "total_estimated_annual_savings": 2948.04,
        "recommendations": [
            {
                "resource_id": "i-1234567890abcdef0",
                "current_instance": "m5.large",
                "recommended_instance": "t3.medium",
                "estimated_monthly_savings": 124.32,
                "estimated_annual_savings": 1491.84,
                "cpu_utilization": "15%",
                "memory_utilization": "45%",
                "network_utilization": "Low"
            },
            {
                "resource_id": "i-0987654321fedcba0",
                "current_instance": "c5.xlarge",
                "recommended_instance": "c5.large",
                "estimated_monthly_savings": 121.35,
                "estimated_annual_savings": 1456.20,
                "cpu_utilization": "25%",
                "memory_utilization": "60%",
                "network_utilization": "Medium"
            }
        ],
        "source": "Mock rightsizing data for testing"
    }


def _get_mock_ri_recommendations() -> Dict[str, Any]:
    """Mock RI recommendations"""
    return {
        "status": "success",
        "total_recommendations": 2,
        "total_estimated_monthly_savings": 189.45,
        "total_estimated_annual_savings": 2273.40,
        "recommendations": [
            {
                "instance_type": "m5.large",
                "platform": "Linux/UNIX",
                "region": "us-east-1",
                "recommended_quantity": 2,
                "estimated_monthly_savings": 98.73,
                "estimated_annual_savings": 1184.76,
                "upfront_cost": 1184.76,
                "monthly_recurring_cost": 45.62,
                "break_even_months": 12,
                "average_utilization": "85%"
            }
        ],
        "source": "Mock RI data for testing"
    }


def _get_mock_anomaly_data(time_period_days: int) -> Dict[str, Any]:
    """Mock anomaly data"""
    return {
        "status": "success",
        "total_anomalies": 1,
        "total_impact": 234.56,
        "anomalies": [
            {
                "anomaly_id": "anomaly-123",
                "anomaly_start_date": "2024-01-15",
                "anomaly_end_date": "2024-01-16",
                "dimension_key": "EC2-Instance",
                "total_impact": 234.56,
                "max_impact": 234.56,
                "feedback_status": "NO_FEEDBACK",
                "root_causes": ["Unusual spike in EC2 usage"]
            }
        ],
        "source": "Mock anomaly data for testing"
    }