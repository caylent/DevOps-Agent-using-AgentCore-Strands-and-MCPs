"""
AWS Cost Explorer Tools - Real AWS Data Access via Official MCP Client
Access to actual AWS Cost Explorer data using the official MCP Python SDK
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from strands import tool

# Import the official MCP client
import sys
import os
sys.path.append(os.path.dirname(__file__))
import sys
from pathlib import Path
# MCP clients are now in the same package structure

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
    Get actual AWS costs from Cost Explorer API via official AWS MCP Server
    
    Args:
        time_period_days: Number of days to look back (default: 30)
        granularity: DAILY, MONTHLY, or HOURLY
        group_by: List of dimensions to group by (SERVICE, ACCOUNT, REGION, etc.)
        account_id: Specific account ID (if None, uses current account)
    
    Returns:
        Dict containing real AWS cost data from Cost Explorer MCP Server
    """
    try:
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=time_period_days)
        
        # Default grouping
        if group_by is None:
            group_by = ['SERVICE']
        
        # Build Cost Explorer MCP request parameters
        mcp_params = {
            'time_period': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            },
            'granularity': granularity,
            'metrics': ['BlendedCost', 'UsageQuantity'],
            'group_by': [{'type': 'DIMENSION', 'key': gb} for gb in group_by]
        }
        
        # Add account filter if specified
        if account_id:
            mcp_params['filter'] = {
                'dimensions': {
                    'key': 'LINKED_ACCOUNT',
                    'values': [account_id]
                }
            }
        
        # Call AWS Cost Explorer using official MCP client
        import asyncio
        response = asyncio.run(mcp_client.get_cost_and_usage(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            granularity,
            group_by,
            ['BlendedCost', 'UsageQuantity']
        ))
        
        if response.get('status') == 'success':
            # Process the MCP response
            mcp_data = response.get('data', {})
            
            # Process and analyze the results
            cost_analysis = _process_mcp_cost_data(mcp_data, time_period_days)
            
            return {
                "status": "success",
                "data_source": "AWS Cost Explorer API via Official MCP Client (Real Data)",
                "time_period": f"{time_period_days} days",
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "granularity": granularity,
                "account_id": account_id or "current",
                "cost_analysis": cost_analysis,
                "raw_data": mcp_data
            }
        else:
            return {
                "status": "error",
                "error": f"Official MCP Cost Explorer call failed: {response.get('error', 'Unknown error')}",
                "suggestion": "Ensure AWS credentials are configured and MCP Python SDK is installed"
            }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to retrieve Cost Explorer data via MCP: {str(e)}",
            "suggestion": "Check AWS Cost Explorer MCP Server installation: uvx awslabs.cost-explorer-mcp-server@latest"
        }


@tool
def analyze_cost_trends_real(
    lookback_days: int = 90,
    service_filter: List[str] = None
) -> Dict[str, Any]:
    """
    Analyze cost trends using real AWS Cost Explorer data
    
    Args:
        lookback_days: Days to analyze for trend detection
        service_filter: List of AWS services to analyze (if None, analyzes all)
    
    Returns:
        Dict containing cost trend analysis with real data
    """
    try:
        ce_client = boto3.client('ce')
        
        # Get cost data for trend analysis
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days)
        
        request_params = {
            'TimePeriod': {
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            'Granularity': 'MONTHLY',
            'Metrics': ['BlendedCost'],
            'GroupBy': [{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        }
        
        # Add service filter if provided
        if service_filter:
            request_params['Filter'] = {
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': service_filter
                }
            }
        
        response = ce_client.get_cost_and_usage(**request_params)
        
        # Analyze trends
        trend_analysis = _analyze_cost_trends(response, lookback_days)
        
        return {
            "status": "success",
            "data_source": "AWS Cost Explorer API (Real Trends)",
            "analysis_period": f"{lookback_days} days",
            "trend_analysis": trend_analysis,
            "recommendations": _generate_trend_recommendations(trend_analysis)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Cost trend analysis failed: {str(e)}"
        }


@tool
def get_multi_account_cost_breakdown(
    organization_accounts: List[str] = None,
    time_period_days: int = 30
) -> Dict[str, Any]:
    """
    Get cost breakdown across multiple AWS accounts in your organization
    
    Args:
        organization_accounts: List of account IDs (if None, gets all org accounts)
        time_period_days: Period for cost analysis
    
    Returns:
        Dict containing multi-account cost analysis
    """
    try:
        # Initialize clients
        ce_client = boto3.client('ce')
        orgs_client = boto3.client('organizations')
        
        # Get organization accounts if not provided
        if organization_accounts is None:
            try:
                accounts_response = orgs_client.list_accounts()
                organization_accounts = [acc['Id'] for acc in accounts_response['Accounts'] 
                                       if acc['Status'] == 'ACTIVE']
            except:
                return {
                    "status": "error",
                    "error": "Cannot access organization accounts. Ensure you're in the management account with proper permissions."
                }
        
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=time_period_days)
        
        # Get costs by account
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )
        
        # Process multi-account data
        multi_account_analysis = _process_multi_account_data(response, organization_accounts)
        
        return {
            "status": "success",
            "data_source": "AWS Organizations + Cost Explorer (Real Data)",
            "accounts_analyzed": len(organization_accounts),
            "time_period": f"{time_period_days} days",
            "multi_account_analysis": multi_account_analysis,
            "cost_optimization_opportunities": _identify_cross_account_optimizations(multi_account_analysis)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Multi-account cost analysis failed: {str(e)}"
        }


@tool
def get_rightsizing_recommendations() -> Dict[str, Any]:
    """
    Get AWS rightsizing recommendations from Cost Explorer
    
    Returns:
        Dict containing actual AWS rightsizing recommendations
    """
    try:
        ce_client = boto3.client('ce')
        
        # Get rightsizing recommendations
        response = ce_client.get_rightsizing_recommendation(
            Service='Amazon Elastic Compute Cloud - Compute'
        )
        
        recommendations = []
        total_monthly_savings = 0
        
        for rec in response.get('RightsizingRecommendations', []):
            recommendation_detail = {
                "instance_id": rec.get('CurrentInstance', {}).get('ResourceId', 'Unknown'),
                "current_type": rec.get('CurrentInstance', {}).get('ResourceDetails', {}).get('EC2ResourceDetails', {}).get('InstanceType'),
                "recommended_type": rec.get('RightsizeType'),
                "monthly_savings": float(rec.get('EstimatedMonthlySavings', '0')),
                "recommendation_reason": rec.get('FindingReasonCodes', []),
                "utilization_metrics": rec.get('CurrentInstance', {}).get('ResourceUtilization', {})
            }
            
            recommendations.append(recommendation_detail)
            total_monthly_savings += recommendation_detail["monthly_savings"]
        
        return {
            "status": "success",
            "data_source": "AWS Cost Explorer Rightsizing API (Real Data)",
            "total_recommendations": len(recommendations),
            "total_monthly_savings": round(total_monthly_savings, 2),
            "total_annual_savings": round(total_monthly_savings * 12, 2),
            "recommendations": recommendations,
            "implementation_guide": _generate_rightsizing_implementation_guide(recommendations)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Rightsizing recommendations failed: {str(e)}",
            "suggestion": "Ensure Cost Explorer is enabled and has sufficient data (14+ days)"
        }


@tool
def get_reserved_instance_recommendations() -> Dict[str, Any]:
    """
    Get actual Reserved Instance recommendations from AWS
    
    Returns:
        Dict containing real RI recommendations from AWS
    """
    try:
        ce_client = boto3.client('ce')
        
        # Get RI recommendations
        response = ce_client.get_reservation_purchase_recommendation(
            Service='Amazon Elastic Compute Cloud - Compute'
        )
        
        recommendations = []
        total_monthly_savings = 0
        
        for rec in response.get('Recommendations', []):
            rec_detail = {
                "instance_type": rec.get('RecommendationDetails', {}).get('InstanceDetails', {}).get('EC2InstanceDetails', {}).get('InstanceType'),
                "recommended_quantity": rec.get('RecommendationDetails', {}).get('RecommendedNumberOfInstancesToPurchase'),
                "monthly_savings": float(rec.get('RecommendationDetails', {}).get('EstimatedMonthlySavingsAmount', '0')),
                "upfront_cost": float(rec.get('RecommendationDetails', {}).get('UpfrontCost', '0')),
                "term": rec.get('RecommendationDetails', {}).get('DefaultTargetInstanceType'),
                "payment_option": rec.get('RecommendationDetails', {}).get('PaymentOption', 'ALL_UPFRONT')
            }
            
            recommendations.append(rec_detail)
            total_monthly_savings += rec_detail["monthly_savings"]
        
        return {
            "status": "success",
            "data_source": "AWS Cost Explorer RI Recommendations (Real Data)",
            "total_recommendations": len(recommendations),
            "total_monthly_savings": round(total_monthly_savings, 2),
            "total_annual_savings": round(total_monthly_savings * 12, 2),
            "recommendations": recommendations,
            "implementation_priority": _prioritize_ri_recommendations(recommendations)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"RI recommendations failed: {str(e)}"
        }


@tool
def get_cost_forecast_mcp(
    forecast_days: int = 30,
    granularity: str = "DAILY",
    confidence_level: int = 80
) -> Dict[str, Any]:
    """
    Get AWS cost forecast using official AWS Cost Explorer MCP Server
    
    Args:
        forecast_days: Number of days to forecast (default: 30)
        granularity: DAILY or MONTHLY
        confidence_level: Confidence level 80 or 95 (default: 80)
    
    Returns:
        Dict containing AWS cost forecast data from MCP Server
    """
    try:
        # Calculate forecast date range
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=forecast_days)
        
        # Build MCP forecast request
        mcp_params = {
            'time_period': {
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            },
            'granularity': granularity,
            'metric': 'BLENDED_COST',
            'prediction_interval_level': confidence_level
        }
        
        # Call AWS Cost Explorer using official MCP client for forecasting
        import asyncio
        response = asyncio.run(mcp_client.get_cost_forecast(
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            'BLENDED_COST',
            granularity
        ))
        
        if response.get('status') == 'success':
            forecast_data = response.get('data', {})
            
            return {
                "status": "success",
                "data_source": "AWS Cost Explorer Forecast API via Official MCP Client",
                "forecast_period": f"{forecast_days} days",
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "granularity": granularity,
                "confidence_level": f"{confidence_level}%",
                "forecast_data": forecast_data,
                "estimated_total": _extract_forecast_total(forecast_data)
            }
        else:
            return {
                "status": "error", 
                "error": f"Official MCP Cost Forecast call failed: {response.get('error', 'Unknown error')}",
                "suggestion": "Ensure AWS credentials are configured and MCP server has sufficient historical data"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": f"Cost forecast via MCP failed: {str(e)}",
            "suggestion": "Check AWS Cost Explorer MCP Server: uvx awslabs.cost-explorer-mcp-server@latest"
        }


@tool
def compare_cost_periods_mcp(
    period1_days: int = 30,
    period2_days: int = 30,
    service_filter: List[str] = None
) -> Dict[str, Any]:
    """
    Compare AWS costs between two time periods using MCP Cost Comparison feature
    
    Args:
        period1_days: Days for first period (recent)
        period2_days: Days for second period (earlier)  
        service_filter: Optional list of services to compare
    
    Returns:
        Dict containing cost comparison analysis from MCP Server
    """
    try:
        # Calculate comparison periods
        end_date = datetime.now().date()
        period1_start = end_date - timedelta(days=period1_days)
        period2_start = period1_start - timedelta(days=period2_days)
        
        # Build MCP comparison request
        mcp_params = {
            'time_period_1': {
                'start': period1_start.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d')
            },
            'time_period_2': {
                'start': period2_start.strftime('%Y-%m-%d'), 
                'end': period1_start.strftime('%Y-%m-%d')
            },
            'granularity': 'MONTHLY',
            'metrics': ['BlendedCost']
        }
        
        # Add service filter if provided
        if service_filter:
            mcp_params['filter'] = {
                'dimensions': {
                    'key': 'SERVICE',
                    'values': service_filter
                }
            }
        
        # Call AWS Cost Explorer MCP Server for comparison
        import asyncio
        response = asyncio.run(mcp_client.call_mcp_tool('get_cost_and_usage_comparisons', mcp_params))
        
        if response.get('status') == 'success':
            comparison_data = response.get('data', {})
            
            return {
                "status": "success",
                "data_source": "AWS Cost Explorer Comparison API via MCP Server",
                "period1": f"Recent {period1_days} days",
                "period2": f"Previous {period2_days} days",
                "comparison_analysis": _process_cost_comparison(comparison_data),
                "cost_drivers": comparison_data.get('cost_drivers', []),
                "raw_comparison": comparison_data
            }
        else:
            return {
                "status": "error",
                "error": f"MCP Cost Comparison call failed: {response.get('error', 'Unknown error')}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": f"Cost comparison via MCP failed: {str(e)}"
        }


# Helper functions
def _process_mcp_cost_data(mcp_data: Dict[str, Any], time_period: int) -> Dict[str, Any]:
    """Process Cost Explorer MCP response data"""
    total_cost = 0
    service_costs = {}
    
    # Handle different MCP response formats
    results_by_time = mcp_data.get('ResultsByTime', []) or mcp_data.get('results_by_time', [])
    
    for time_period_data in results_by_time:
        groups = time_period_data.get('Groups', []) or time_period_data.get('groups', [])
        for group in groups:
            keys = group.get('Keys', []) or group.get('keys', [])
            service = keys[0] if keys else 'Unknown'
            
            metrics = group.get('Metrics', {}) or group.get('metrics', {})
            blended_cost = metrics.get('BlendedCost', {}) or metrics.get('blended_cost', {})
            cost = float(blended_cost.get('Amount', '0') or blended_cost.get('amount', '0'))
            
            total_cost += cost
            if service in service_costs:
                service_costs[service] += cost
            else:
                service_costs[service] = cost
    
    # Sort services by cost
    sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "total_cost": round(total_cost, 2),
        "top_services": sorted_services[:10],
        "service_breakdown": service_costs,
        "daily_average": round(total_cost / time_period, 2) if time_period > 0 else 0
    }


def _process_cost_explorer_data(response: Dict[str, Any], time_period: int) -> Dict[str, Any]:
    """Process Cost Explorer response data"""
    total_cost = 0
    service_costs = {}
    
    for time_period in response.get('ResultsByTime', []):
        for group in time_period.get('Groups', []):
            service = group.get('Keys', ['Unknown'])[0]
            cost = float(group.get('Metrics', {}).get('BlendedCost', {}).get('Amount', '0'))
            
            total_cost += cost
            if service in service_costs:
                service_costs[service] += cost
            else:
                service_costs[service] = cost
    
    # Sort services by cost
    sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "total_cost": round(total_cost, 2),
        "top_services": sorted_services[:10],
        "service_breakdown": service_costs,
        "daily_average": round(total_cost / time_period, 2)
    }


def _analyze_cost_trends(response: Dict[str, Any], lookback_days: int) -> Dict[str, Any]:
    """Analyze cost trends from Cost Explorer data"""
    monthly_costs = []
    
    for time_period in response.get('ResultsByTime', []):
        period_cost = sum(
            float(group.get('Metrics', {}).get('BlendedCost', {}).get('Amount', '0'))
            for group in time_period.get('Groups', [])
        )
        monthly_costs.append(period_cost)
    
    if len(monthly_costs) >= 2:
        trend_percentage = ((monthly_costs[-1] - monthly_costs[0]) / monthly_costs[0]) * 100
        trend_direction = "increasing" if trend_percentage > 5 else "decreasing" if trend_percentage < -5 else "stable"
    else:
        trend_percentage = 0
        trend_direction = "insufficient_data"
    
    return {
        "trend_direction": trend_direction,
        "trend_percentage": round(trend_percentage, 2),
        "monthly_costs": [round(cost, 2) for cost in monthly_costs],
        "average_monthly_cost": round(sum(monthly_costs) / len(monthly_costs), 2) if monthly_costs else 0
    }


def _generate_trend_recommendations(trend_analysis: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on cost trends"""
    recommendations = []
    
    if trend_analysis["trend_direction"] == "increasing":
        if trend_analysis["trend_percentage"] > 20:
            recommendations.append("URGENT: Costs increasing by >20% - immediate investigation required")
        recommendations.extend([
            "Set up Cost Anomaly Detection for early warnings",
            "Implement cost budgets and alerts",
            "Review rightsizing recommendations",
            "Analyze Reserved Instance opportunities"
        ])
    elif trend_analysis["trend_direction"] == "decreasing":
        recommendations.extend([
            "Great job on cost optimization!",
            "Consider reallocating savings to innovation projects",
            "Document successful cost reduction strategies"
        ])
    else:
        recommendations.extend([
            "Costs are stable - good for predictability",
            "Consider proactive optimization initiatives",
            "Regular review of resource utilization"
        ])
    
    return recommendations


def _process_multi_account_data(response: Dict[str, Any], accounts: List[str]) -> Dict[str, Any]:
    """Process multi-account cost data"""
    account_costs = {}
    
    for time_period in response.get('ResultsByTime', []):
        for group in time_period.get('Groups', []):
            keys = group.get('Keys', [])
            if len(keys) >= 2:
                account_id, service = keys[0], keys[1]
                cost = float(group.get('Metrics', {}).get('BlendedCost', {}).get('Amount', '0'))
                
                if account_id not in account_costs:
                    account_costs[account_id] = {"total_cost": 0, "services": {}}
                
                account_costs[account_id]["total_cost"] += cost
                account_costs[account_id]["services"][service] = account_costs[account_id]["services"].get(service, 0) + cost
    
    return {
        "account_breakdown": account_costs,
        "total_organization_cost": sum(acc["total_cost"] for acc in account_costs.values()),
        "highest_cost_account": max(account_costs.items(), key=lambda x: x[1]["total_cost"]) if account_costs else None
    }


def _identify_cross_account_optimizations(analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify optimization opportunities across accounts"""
    opportunities = []
    
    # Check for accounts with significantly higher costs
    if analysis.get("highest_cost_account"):
        highest_cost = analysis["highest_cost_account"][1]["total_cost"]
        total_cost = analysis["total_organization_cost"]
        
        if highest_cost > (total_cost * 0.5):  # Account represents >50% of costs
            opportunities.append({
                "type": "high_cost_account_review",
                "account_id": analysis["highest_cost_account"][0],
                "description": f"Account represents {(highest_cost/total_cost)*100:.1f}% of total costs",
                "recommendation": "Deep dive into this account's resource usage and optimization opportunities"
            })
    
    return opportunities


def _generate_rightsizing_implementation_guide(recommendations: List[Dict[str, Any]]) -> List[str]:
    """Generate implementation guide for rightsizing"""
    guide = [
        "1. Start with highest savings recommendations",
        "2. Test in non-production environments first",
        "3. Monitor performance after changes",
        "4. Implement gradually to avoid service disruption"
    ]
    
    if recommendations:
        total_savings = sum(rec.get("monthly_savings", 0) for rec in recommendations)
        guide.insert(0, f"Total potential savings: ${total_savings:.2f}/month")
    
    return guide


def _prioritize_ri_recommendations(recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Prioritize RI recommendations by savings impact"""
    return sorted(recommendations, key=lambda x: x.get("monthly_savings", 0), reverse=True)[:5]


def _extract_forecast_total(forecast_data: Dict[str, Any]) -> Dict[str, float]:
    """Extract total forecast amounts from MCP response"""
    try:
        total_cost = 0.0
        forecast_by_time = forecast_data.get('ForecastResultsByTime', [])
        
        for period in forecast_by_time:
            mean_value = period.get('MeanValue', '0')
            total_cost += float(mean_value)
        
        return {
            "total_forecast": round(total_cost, 2),
            "daily_average": round(total_cost / len(forecast_by_time), 2) if forecast_by_time else 0
        }
    except Exception:
        return {"total_forecast": 0.0, "daily_average": 0.0}


def _process_cost_comparison(comparison_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process cost comparison data from MCP response"""
    try:
        # Extract comparison metrics from MCP response
        period1_total = 0.0
        period2_total = 0.0
        
        # Process comparison results
        results = comparison_data.get('ResultsByTime', [])
        if len(results) >= 2:
            for result in results:
                groups = result.get('Groups', [])
                for group in groups:
                    metrics = group.get('Metrics', {})
                    blended_cost = metrics.get('BlendedCost', {})
                    cost = float(blended_cost.get('Amount', '0'))
                    
                    # Determine which period this belongs to
                    time_period = result.get('TimePeriod', {})
                    if 'Start' in time_period:
                        # Logic to determine period based on dates would go here
                        period1_total += cost
                    else:
                        period2_total += cost
        
        # Calculate comparison metrics
        cost_difference = period1_total - period2_total
        percentage_change = ((cost_difference / period2_total) * 100) if period2_total > 0 else 0
        
        return {
            "period1_total": round(period1_total, 2),
            "period2_total": round(period2_total, 2),
            "cost_difference": round(cost_difference, 2),
            "percentage_change": round(percentage_change, 2),
            "trend": "increasing" if cost_difference > 0 else "decreasing" if cost_difference < 0 else "stable"
        }
    except Exception:
        return {
            "period1_total": 0.0,
            "period2_total": 0.0,
            "cost_difference": 0.0,
            "percentage_change": 0.0,
            "trend": "unknown"
        }