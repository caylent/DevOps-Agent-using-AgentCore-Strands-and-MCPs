"""
AWS Pricing Comparisons
Side-by-side pricing comparisons between different configurations
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from strands import tool

from .pricing import get_real_aws_pricing


@tool
def generate_cost_comparison_report(configurations: List[Dict[str, Any]], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Generate comprehensive cost comparison report for different configurations
    
    Args:
        configurations: List of configuration options to compare
        region: AWS region
    
    Returns:
        Dict containing detailed cost comparison report
    """
    try:
        comparison_results = []
        
        for i, config in enumerate(configurations):
            # Get pricing for each configuration
            pricing_result = get_real_aws_pricing(
                config.get("service", "EC2"),
                config.get("instance_type"),
                region
            )
            
            if pricing_result.get("status") == "success":
                pricing_data = pricing_result.get("pricing_data", {})
                
                comparison_results.append({
                    "configuration_id": f"config_{i+1}",
                    "configuration": config,
                    "pricing": pricing_data,
                    "monthly_cost_on_demand": pricing_data.get("on_demand", {}).get("monthly", 0),
                    "monthly_cost_reserved_1year": pricing_data.get("reserved_1year", {}).get("monthly", 0),
                    "annual_savings_with_reserved": (
                        pricing_data.get("on_demand", {}).get("monthly", 0) - 
                        pricing_data.get("reserved_1year", {}).get("monthly", 0)
                    ) * 12
                })
        
        # Find most cost-effective option
        best_option = min(comparison_results, key=lambda x: x["monthly_cost_on_demand"]) if comparison_results else None
        
        return {
            "status": "success",
            "region": region,
            "total_configurations_analyzed": len(configurations),
            "comparison_results": comparison_results,
            "recommended_configuration": best_option,
            "report_generated": datetime.now().isoformat(),
            "data_source": "Real AWS Pricing API",
            "executive_summary": _generate_executive_summary(comparison_results)
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Cost comparison report generation failed: {str(e)}"}


@tool
def compare_instance_types(instance_types: List[str], service: str = "EC2", region: str = "us-east-1") -> Dict[str, Any]:
    """
    Compare pricing between different instance types
    
    Args:
        instance_types: List of instance types to compare
        service: AWS service (default: EC2)
        region: AWS region
    
    Returns:
        Dict containing instance type comparison
    """
    try:
        comparisons = []
        
        for instance_type in instance_types:
            pricing_result = get_real_aws_pricing(service, instance_type, region)
            
            if pricing_result.get("status") == "success":
                pricing_data = pricing_result.get("pricing_data", {})
                
                comparisons.append({
                    "instance_type": instance_type,
                    "hourly_on_demand": pricing_data.get("on_demand", {}).get("hourly", 0),
                    "monthly_on_demand": pricing_data.get("on_demand", {}).get("monthly", 0),
                    "hourly_reserved_1year": pricing_data.get("reserved_1year", {}).get("hourly", 0),
                    "monthly_reserved_1year": pricing_data.get("reserved_1year", {}).get("monthly", 0),
                    "annual_savings_reserved": (
                        pricing_data.get("on_demand", {}).get("monthly", 0) - 
                        pricing_data.get("reserved_1year", {}).get("monthly", 0)
                    ) * 12,
                    "specifications": _get_instance_specs(instance_type)
                })
        
        # Sort by monthly on-demand cost
        comparisons.sort(key=lambda x: x["monthly_on_demand"])
        
        # Calculate cost differences
        for i, comp in enumerate(comparisons):
            if i > 0:
                comp["cost_increase_from_cheapest"] = comp["monthly_on_demand"] - comparisons[0]["monthly_on_demand"]
                comp["percentage_increase_from_cheapest"] = round(
                    ((comp["monthly_on_demand"] - comparisons[0]["monthly_on_demand"]) / comparisons[0]["monthly_on_demand"]) * 100, 1
                ) if comparisons[0]["monthly_on_demand"] > 0 else 0
            else:
                comp["cost_increase_from_cheapest"] = 0
                comp["percentage_increase_from_cheapest"] = 0
        
        return {
            "status": "success",
            "service": service,
            "region": region,
            "instance_type_comparisons": comparisons,
            "cheapest_option": comparisons[0] if comparisons else None,
            "most_expensive_option": comparisons[-1] if comparisons else None,
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "Real AWS Pricing API",
            "summary": _generate_instance_comparison_summary(comparisons)
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Instance type comparison failed: {str(e)}"}


@tool
def compare_pricing_models(service: str, instance_type: str, region: str = "us-east-1") -> Dict[str, Any]:
    """
    Compare different pricing models for the same resource
    
    Args:
        service: AWS service name
        instance_type: Specific instance type
        region: AWS region
    
    Returns:
        Dict containing pricing model comparison
    """
    try:
        pricing_result = get_real_aws_pricing(service, instance_type, region)
        
        if pricing_result.get("status") != "success":
            return pricing_result
        
        pricing_data = pricing_result.get("pricing_data", {})
        
        # Extract different pricing models
        pricing_models = []
        
        if "on_demand" in pricing_data:
            pricing_models.append({
                "model": "On-Demand",
                "commitment": "None",
                "upfront_cost": 0,
                "hourly_rate": pricing_data["on_demand"].get("hourly", 0),
                "monthly_cost": pricing_data["on_demand"].get("monthly", 0),
                "annual_cost": pricing_data["on_demand"].get("monthly", 0) * 12,
                "flexibility": "High",
                "use_case": "Variable workloads, short-term needs"
            })
        
        if "reserved_1year" in pricing_data:
            monthly_reserved = pricing_data["reserved_1year"].get("monthly", 0)
            pricing_models.append({
                "model": "Reserved Instance (1-year)",
                "commitment": "1 year",
                "upfront_cost": pricing_data["reserved_1year"].get("upfront", 0),
                "hourly_rate": pricing_data["reserved_1year"].get("hourly", 0),
                "monthly_cost": monthly_reserved,
                "annual_cost": monthly_reserved * 12,
                "flexibility": "Medium",
                "use_case": "Predictable workloads, cost optimization",
                "savings_vs_on_demand": {
                    "monthly": pricing_data.get("on_demand", {}).get("monthly", 0) - monthly_reserved,
                    "annual": (pricing_data.get("on_demand", {}).get("monthly", 0) - monthly_reserved) * 12,
                    "percentage": round(
                        ((pricing_data.get("on_demand", {}).get("monthly", 0) - monthly_reserved) / 
                         pricing_data.get("on_demand", {}).get("monthly", 1)) * 100, 1
                    )
                }
            })
        
        if "reserved_3year" in pricing_data:
            monthly_reserved_3y = pricing_data["reserved_3year"].get("monthly", 0)
            pricing_models.append({
                "model": "Reserved Instance (3-year)",
                "commitment": "3 years",
                "upfront_cost": pricing_data["reserved_3year"].get("upfront", 0),
                "hourly_rate": pricing_data["reserved_3year"].get("hourly", 0),
                "monthly_cost": monthly_reserved_3y,
                "annual_cost": monthly_reserved_3y * 12,
                "flexibility": "Low",
                "use_case": "Long-term stable workloads, maximum savings",
                "savings_vs_on_demand": {
                    "monthly": pricing_data.get("on_demand", {}).get("monthly", 0) - monthly_reserved_3y,
                    "annual": (pricing_data.get("on_demand", {}).get("monthly", 0) - monthly_reserved_3y) * 12,
                    "percentage": round(
                        ((pricing_data.get("on_demand", {}).get("monthly", 0) - monthly_reserved_3y) / 
                         pricing_data.get("on_demand", {}).get("monthly", 1)) * 100, 1
                    )
                }
            })
        
        # Sort by annual cost
        pricing_models.sort(key=lambda x: x["annual_cost"])
        
        return {
            "status": "success",
            "service": service,
            "instance_type": instance_type,
            "region": region,
            "pricing_models": pricing_models,
            "most_economical": pricing_models[0] if pricing_models else None,
            "most_flexible": next((pm for pm in pricing_models if pm["model"] == "On-Demand"), None),
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "Real AWS Pricing API",
            "recommendation": _generate_pricing_model_recommendation(pricing_models)
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Pricing model comparison failed: {str(e)}"}


@tool
def compare_regions_pricing(service: str, instance_type: str, regions: List[str]) -> Dict[str, Any]:
    """
    Compare pricing across different AWS regions
    
    Args:
        service: AWS service name
        instance_type: Specific instance type
        regions: List of AWS regions to compare
    
    Returns:
        Dict containing regional pricing comparison
    """
    try:
        regional_comparisons = []
        
        for region in regions:
            pricing_result = get_real_aws_pricing(service, instance_type, region)
            
            if pricing_result.get("status") == "success":
                pricing_data = pricing_result.get("pricing_data", {})
                
                regional_comparisons.append({
                    "region": region,
                    "region_name": _get_region_name(region),
                    "hourly_on_demand": pricing_data.get("on_demand", {}).get("hourly", 0),
                    "monthly_on_demand": pricing_data.get("on_demand", {}).get("monthly", 0),
                    "hourly_reserved_1year": pricing_data.get("reserved_1year", {}).get("hourly", 0),
                    "monthly_reserved_1year": pricing_data.get("reserved_1year", {}).get("monthly", 0),
                    "currency": pricing_data.get("currency", "USD")
                })
        
        # Sort by monthly on-demand cost
        regional_comparisons.sort(key=lambda x: x["monthly_on_demand"])
        
        # Calculate cost differences from cheapest region
        cheapest_cost = regional_comparisons[0]["monthly_on_demand"] if regional_comparisons else 0
        
        for comp in regional_comparisons:
            comp["cost_difference_from_cheapest"] = comp["monthly_on_demand"] - cheapest_cost
            comp["percentage_increase_from_cheapest"] = round(
                ((comp["monthly_on_demand"] - cheapest_cost) / cheapest_cost) * 100, 1
            ) if cheapest_cost > 0 else 0
        
        return {
            "status": "success",
            "service": service,
            "instance_type": instance_type,
            "regional_comparisons": regional_comparisons,
            "cheapest_region": regional_comparisons[0] if regional_comparisons else None,
            "most_expensive_region": regional_comparisons[-1] if regional_comparisons else None,
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "Real AWS Pricing API",
            "summary": _generate_regional_comparison_summary(regional_comparisons)
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Regional pricing comparison failed: {str(e)}"}


# Helper functions
def _generate_executive_summary(comparison_results: List[Dict[str, Any]]) -> str:
    """Generate executive summary for cost comparison"""
    if not comparison_results:
        return "No configurations to compare."
    
    best_config = min(comparison_results, key=lambda x: x["monthly_cost_on_demand"])
    worst_config = max(comparison_results, key=lambda x: x["monthly_cost_on_demand"])
    
    savings = worst_config["monthly_cost_on_demand"] - best_config["monthly_cost_on_demand"]
    
    return f"Configuration {best_config['configuration_id']} offers the best value at ${best_config['monthly_cost_on_demand']:.2f}/month. Switching from the most expensive option could save ${savings:.2f}/month (${savings*12:.2f}/year)."


def _get_instance_specs(instance_type: str) -> Dict[str, Any]:
    """Get basic specifications for instance type (simplified mock data)"""
    # This would typically call AWS API or maintain a database of instance specs
    specs_map = {
        "t3.micro": {"vcpu": 2, "memory_gb": 1, "network": "Low to Moderate"},
        "t3.small": {"vcpu": 2, "memory_gb": 2, "network": "Low to Moderate"},
        "t3.medium": {"vcpu": 2, "memory_gb": 4, "network": "Low to Moderate"},
        "t3.large": {"vcpu": 2, "memory_gb": 8, "network": "Low to Moderate"},
        "m5.large": {"vcpu": 2, "memory_gb": 8, "network": "Up to 10 Gbps"},
        "m5.xlarge": {"vcpu": 4, "memory_gb": 16, "network": "Up to 10 Gbps"},
        "c5.large": {"vcpu": 2, "memory_gb": 4, "network": "Up to 10 Gbps"},
        "c5.xlarge": {"vcpu": 4, "memory_gb": 8, "network": "Up to 10 Gbps"},
    }
    
    return specs_map.get(instance_type, {"vcpu": "N/A", "memory_gb": "N/A", "network": "N/A"})


def _generate_instance_comparison_summary(comparisons: List[Dict[str, Any]]) -> str:
    """Generate summary for instance type comparison"""
    if not comparisons:
        return "No instance types to compare."
    
    cheapest = comparisons[0]
    most_expensive = comparisons[-1]
    
    return f"Cheapest: {cheapest['instance_type']} at ${cheapest['monthly_on_demand']:.2f}/month. Most expensive: {most_expensive['instance_type']} at ${most_expensive['monthly_on_demand']:.2f}/month. Price range: ${most_expensive['monthly_on_demand'] - cheapest['monthly_on_demand']:.2f}/month difference."


def _generate_pricing_model_recommendation(pricing_models: List[Dict[str, Any]]) -> str:
    """Generate recommendation for pricing models"""
    if not pricing_models:
        return "No pricing models available."
    
    on_demand = next((pm for pm in pricing_models if pm["model"] == "On-Demand"), None)
    reserved_1y = next((pm for pm in pricing_models if "1-year" in pm["model"]), None)
    
    if on_demand and reserved_1y:
        savings = reserved_1y.get("savings_vs_on_demand", {})
        monthly_savings = savings.get("monthly", 0)
        if monthly_savings > 50:
            return f"Recommended: Reserved Instance (1-year) for consistent workloads. Saves ${monthly_savings:.2f}/month ({savings.get('percentage', 0)}%) vs On-Demand."
        else:
            return "Recommended: On-Demand for variable workloads. Reserved Instance savings are minimal for current usage pattern."
    
    return "Consider Reserved Instances for predictable, long-running workloads to maximize savings."


def _generate_regional_comparison_summary(regional_comparisons: List[Dict[str, Any]]) -> str:
    """Generate summary for regional pricing comparison"""
    if not regional_comparisons:
        return "No regions to compare."
    
    cheapest = regional_comparisons[0]
    most_expensive = regional_comparisons[-1]
    
    savings = most_expensive["monthly_on_demand"] - cheapest["monthly_on_demand"]
    
    return f"Cheapest region: {cheapest['region_name']} ({cheapest['region']}) at ${cheapest['monthly_on_demand']:.2f}/month. Most expensive: {most_expensive['region_name']} ({most_expensive['region']}) at ${most_expensive['monthly_on_demand']:.2f}/month. Potential savings: ${savings:.2f}/month by choosing optimal region."


def _get_region_name(region_code: str) -> str:
    """Convert region code to human-readable name"""
    region_names = {
        "us-east-1": "US East (N. Virginia)",
        "us-east-2": "US East (Ohio)",
        "us-west-1": "US West (N. California)",
        "us-west-2": "US West (Oregon)",
        "eu-west-1": "Europe (Ireland)",
        "eu-west-2": "Europe (London)",
        "eu-central-1": "Europe (Frankfurt)",
        "ap-southeast-1": "Asia Pacific (Singapore)",
        "ap-southeast-2": "Asia Pacific (Sydney)",
        "ap-northeast-1": "Asia Pacific (Tokyo)"
    }
    
    return region_names.get(region_code, region_code)