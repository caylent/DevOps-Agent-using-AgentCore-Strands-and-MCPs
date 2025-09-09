"""
AWS Pricing Optimization
Price-based optimization recommendations and cost-effective alternatives
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from strands import tool

from .pricing import get_real_aws_pricing
from .comparisons import compare_instance_types, compare_pricing_models


@tool
def analyze_price_optimization_opportunities(resource_type: str, current_configuration: Dict[str, Any], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Analyze price-based optimization opportunities for AWS resources
    
    Args:
        resource_type: Type of AWS resource (EC2, RDS, Lambda, etc.)
        current_configuration: Current resource configuration
        region: AWS region
    
    Returns:
        Dict containing price-based optimization recommendations
    """
    try:
        optimization_opportunities = []
        total_potential_savings = 0.0
        
        if resource_type.upper() == "EC2":
            opportunities = _analyze_ec2_price_optimization(current_configuration, region)
            optimization_opportunities.extend(opportunities)
        elif resource_type.upper() == "RDS":
            opportunities = _analyze_rds_price_optimization(current_configuration, region)
            optimization_opportunities.extend(opportunities)
        elif resource_type.upper() == "LAMBDA":
            opportunities = _analyze_lambda_price_optimization(current_configuration, region)
            optimization_opportunities.extend(opportunities)
        elif resource_type.upper() == "EBS":
            opportunities = _analyze_ebs_price_optimization(current_configuration, region)
            optimization_opportunities.extend(opportunities)
        
        # Calculate total potential savings
        for opp in optimization_opportunities:
            total_potential_savings += opp.get("monthly_savings", 0)
        
        return {
            "status": "success",
            "resource_type": resource_type,
            "region": region,
            "current_configuration": current_configuration,
            "total_opportunities": len(optimization_opportunities),
            "optimization_opportunities": optimization_opportunities,
            "total_potential_monthly_savings": round(total_potential_savings, 2),
            "total_potential_annual_savings": round(total_potential_savings * 12, 2),
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "AWS Pricing API + Price Analysis",
            "recommendations_summary": _generate_optimization_summary(optimization_opportunities)
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Price optimization analysis failed: {str(e)}"}


@tool
def suggest_cost_effective_alternatives(service: str, instance_type: str, requirements: Dict[str, Any], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Suggest cost-effective alternatives based on requirements
    
    Args:
        service: AWS service name
        instance_type: Current instance type
        requirements: Resource requirements (cpu, memory, network, etc.)
        region: AWS region
    
    Returns:
        Dict containing cost-effective alternative suggestions
    """
    try:
        current_pricing = get_real_aws_pricing(service, instance_type, region)
        
        if current_pricing.get("status") != "success":
            return current_pricing
        
        current_monthly_cost = current_pricing.get("pricing_data", {}).get("on_demand", {}).get("monthly", 0)
        
        # Get alternative instance types based on requirements
        alternative_types = _get_alternative_instance_types(instance_type, requirements)
        
        alternatives = []
        for alt_type in alternative_types:
            alt_pricing = get_real_aws_pricing(service, alt_type, region)
            
            if alt_pricing.get("status") == "success":
                alt_pricing_data = alt_pricing.get("pricing_data", {})
                alt_monthly_cost = alt_pricing_data.get("on_demand", {}).get("monthly", 0)
                
                monthly_savings = current_monthly_cost - alt_monthly_cost
                savings_percentage = (monthly_savings / current_monthly_cost * 100) if current_monthly_cost > 0 else 0
                
                alternatives.append({
                    "instance_type": alt_type,
                    "monthly_cost": alt_monthly_cost,
                    "monthly_savings": round(monthly_savings, 2),
                    "annual_savings": round(monthly_savings * 12, 2),
                    "savings_percentage": round(savings_percentage, 1),
                    "specifications": _get_instance_specifications(alt_type),
                    "compatibility_score": _calculate_compatibility_score(instance_type, alt_type, requirements),
                    "recommendation_reason": _get_recommendation_reason(instance_type, alt_type, monthly_savings)
                })
        
        # Filter and sort alternatives
        cost_effective_alternatives = [alt for alt in alternatives if alt["monthly_savings"] > 0]
        cost_effective_alternatives.sort(key=lambda x: x["monthly_savings"], reverse=True)
        
        return {
            "status": "success",
            "service": service,
            "current_instance_type": instance_type,
            "current_monthly_cost": current_monthly_cost,
            "region": region,
            "requirements": requirements,
            "cost_effective_alternatives": cost_effective_alternatives,
            "best_alternative": cost_effective_alternatives[0] if cost_effective_alternatives else None,
            "total_alternatives_found": len(cost_effective_alternatives),
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "AWS Pricing API + Instance Analysis",
            "recommendation": _generate_alternative_recommendation(cost_effective_alternatives, current_monthly_cost)
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Alternative suggestion analysis failed: {str(e)}"}


@tool
def calculate_savings_potential(configurations: List[Dict[str, Any]], optimization_strategies: List[str], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Calculate total savings potential across multiple configurations and strategies
    
    Args:
        configurations: List of current resource configurations
        optimization_strategies: List of optimization strategies to apply
        region: AWS region
    
    Returns:
        Dict containing comprehensive savings potential analysis
    """
    try:
        total_current_cost = 0
        total_optimized_cost = 0
        configuration_analyses = []
        
        for config in configurations:
            service = config.get("service", "EC2")
            instance_type = config.get("instance_type")
            quantity = config.get("quantity", 1)
            
            # Get current pricing
            current_pricing = get_real_aws_pricing(service, instance_type, region)
            
            if current_pricing.get("status") == "success":
                current_monthly_cost = current_pricing.get("pricing_data", {}).get("on_demand", {}).get("monthly", 0) * quantity
                total_current_cost += current_monthly_cost
                
                # Apply optimization strategies
                optimized_cost = current_monthly_cost
                applied_strategies = []
                
                for strategy in optimization_strategies:
                    if strategy == "reserved_instances":
                        reserved_cost = current_pricing.get("pricing_data", {}).get("reserved_1year", {}).get("monthly", 0) * quantity
                        if reserved_cost > 0 and reserved_cost < optimized_cost:
                            optimized_cost = reserved_cost
                            applied_strategies.append({
                                "strategy": "Reserved Instances (1-year)",
                                "monthly_savings": current_monthly_cost - reserved_cost,
                                "savings_percentage": round(((current_monthly_cost - reserved_cost) / current_monthly_cost) * 100, 1)
                            })
                    
                    elif strategy == "right_sizing":
                        # Simulate right-sizing savings (would use actual utilization data in real implementation)
                        right_sized_cost = current_monthly_cost * 0.7  # Assume 30% savings from right-sizing
                        if right_sized_cost < optimized_cost:
                            optimized_cost = right_sized_cost
                            applied_strategies.append({
                                "strategy": "Right-sizing",
                                "monthly_savings": current_monthly_cost - right_sized_cost,
                                "savings_percentage": round(((current_monthly_cost - right_sized_cost) / current_monthly_cost) * 100, 1)
                            })
                    
                    elif strategy == "spot_instances":
                        # Simulate spot instance savings (up to 90% for suitable workloads)
                        spot_cost = current_monthly_cost * 0.3  # Assume 70% savings from spot instances
                        if config.get("workload_type") == "fault_tolerant" and spot_cost < optimized_cost:
                            optimized_cost = spot_cost
                            applied_strategies.append({
                                "strategy": "Spot Instances",
                                "monthly_savings": current_monthly_cost - spot_cost,
                                "savings_percentage": round(((current_monthly_cost - spot_cost) / current_monthly_cost) * 100, 1)
                            })
                
                total_optimized_cost += optimized_cost
                
                configuration_analyses.append({
                    "configuration": config,
                    "current_monthly_cost": round(current_monthly_cost, 2),
                    "optimized_monthly_cost": round(optimized_cost, 2),
                    "monthly_savings": round(current_monthly_cost - optimized_cost, 2),
                    "applied_strategies": applied_strategies
                })
        
        total_monthly_savings = total_current_cost - total_optimized_cost
        savings_percentage = (total_monthly_savings / total_current_cost * 100) if total_current_cost > 0 else 0
        
        return {
            "status": "success",
            "region": region,
            "optimization_strategies": optimization_strategies,
            "configuration_analyses": configuration_analyses,
            "summary": {
                "total_current_monthly_cost": round(total_current_cost, 2),
                "total_optimized_monthly_cost": round(total_optimized_cost, 2),
                "total_monthly_savings": round(total_monthly_savings, 2),
                "total_annual_savings": round(total_monthly_savings * 12, 2),
                "overall_savings_percentage": round(savings_percentage, 1)
            },
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "AWS Pricing API + Optimization Analysis",
            "recommendations": _generate_savings_recommendations(total_monthly_savings, configuration_analyses)
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Savings potential calculation failed: {str(e)}"}


@tool
def optimize_terraform_plan_costs(terraform_plan: Dict[str, Any], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Analyze Terraform plan for cost optimization opportunities
    
    Args:
        terraform_plan: Parsed Terraform plan JSON
        region: AWS region
    
    Returns:
        Dict containing cost optimization recommendations for Terraform plan
    """
    try:
        if not terraform_plan or "planned_values" not in terraform_plan:
            return {
                "status": "error",
                "error": "Invalid Terraform plan format",
                "suggestion": "Provide a valid Terraform plan JSON with planned_values"
            }
        
        planned_values = terraform_plan.get("planned_values", {})
        root_module = planned_values.get("root_module", {})
        resources = root_module.get("resources", [])
        
        total_estimated_cost = 0
        total_optimized_cost = 0
        resource_optimizations = []
        
        for resource in resources:
            resource_type = resource.get("type", "")
            resource_name = resource.get("name", "")
            resource_values = resource.get("values", {})
            
            # Analyze EC2 instances
            if resource_type == "aws_instance":
                instance_type = resource_values.get("instance_type", "")
                if instance_type:
                    pricing_result = get_real_aws_pricing("EC2", instance_type, region)
                    
                    if pricing_result.get("status") == "success":
                        pricing_data = pricing_result.get("pricing_data", {})
                        current_monthly_cost = pricing_data.get("on_demand", {}).get("monthly", 0)
                        total_estimated_cost += current_monthly_cost
                        
                        # Suggest optimizations
                        optimizations = _suggest_instance_optimizations(instance_type, resource_values, region)
                        
                        optimized_cost = current_monthly_cost
                        best_optimization = None
                        
                        for opt in optimizations:
                            if opt["optimized_monthly_cost"] < optimized_cost:
                                optimized_cost = opt["optimized_monthly_cost"]
                                best_optimization = opt
                        
                        total_optimized_cost += optimized_cost
                        
                        resource_optimizations.append({
                            "resource_type": resource_type,
                            "resource_name": resource_name,
                            "current_instance_type": instance_type,
                            "current_monthly_cost": round(current_monthly_cost, 2),
                            "optimized_monthly_cost": round(optimized_cost, 2),
                            "monthly_savings": round(current_monthly_cost - optimized_cost, 2),
                            "optimization_applied": best_optimization,
                            "all_optimization_options": optimizations
                        })
            
            # Analyze RDS instances
            elif resource_type == "aws_db_instance":
                instance_class = resource_values.get("instance_class", "")
                if instance_class:
                    pricing_result = get_real_aws_pricing("RDS", instance_class, region)
                    
                    if pricing_result.get("status") == "success":
                        pricing_data = pricing_result.get("pricing_data", {})
                        current_monthly_cost = pricing_data.get("on_demand", {}).get("monthly", 0)
                        total_estimated_cost += current_monthly_cost
                        
                        # For RDS, mainly suggest Reserved Instances
                        reserved_cost = pricing_data.get("reserved_1year", {}).get("monthly", current_monthly_cost)
                        optimized_cost = min(current_monthly_cost, reserved_cost)
                        total_optimized_cost += optimized_cost
                        
                        resource_optimizations.append({
                            "resource_type": resource_type,
                            "resource_name": resource_name,
                            "current_instance_class": instance_class,
                            "current_monthly_cost": round(current_monthly_cost, 2),
                            "optimized_monthly_cost": round(optimized_cost, 2),
                            "monthly_savings": round(current_monthly_cost - optimized_cost, 2),
                            "optimization_applied": {
                                "strategy": "Reserved Instance (1-year)",
                                "description": "Switch to Reserved Instance for predictable database workloads"
                            } if reserved_cost < current_monthly_cost else None
                        })
        
        total_monthly_savings = total_estimated_cost - total_optimized_cost
        savings_percentage = (total_monthly_savings / total_estimated_cost * 100) if total_estimated_cost > 0 else 0
        
        return {
            "status": "success",
            "region": region,
            "terraform_plan_analysis": {
                "total_resources_analyzed": len(resource_optimizations),
                "total_estimated_monthly_cost": round(total_estimated_cost, 2),
                "total_optimized_monthly_cost": round(total_optimized_cost, 2),
                "total_monthly_savings": round(total_monthly_savings, 2),
                "total_annual_savings": round(total_monthly_savings * 12, 2),
                "savings_percentage": round(savings_percentage, 1)
            },
            "resource_optimizations": resource_optimizations,
            "analysis_timestamp": datetime.now().isoformat(),
            "data_source": "Terraform Plan + AWS Pricing API",
            "recommendations": _generate_terraform_optimization_recommendations(resource_optimizations, total_monthly_savings),
            "next_steps": [
                "Review suggested optimizations for each resource",
                "Update Terraform configuration with recommended instance types",
                "Consider Reserved Instances for stable workloads",
                "Run terraform plan again to validate changes"
            ]
        }
        
    except Exception as e:
        return {"status": "error", "error": f"Terraform plan cost optimization failed: {str(e)}"}


# Helper functions
def _analyze_ec2_price_optimization(config: Dict[str, Any], region: str) -> List[Dict[str, Any]]:
    """Analyze EC2-specific price optimization opportunities"""
    opportunities = []
    
    instance_type = config.get("instance_type", "")
    
    # Suggest smaller instance types if appropriate
    smaller_types = _get_smaller_instance_types(instance_type)
    for smaller_type in smaller_types:
        pricing_result = get_real_aws_pricing("EC2", smaller_type, region)
        if pricing_result.get("status") == "success":
            current_cost = config.get("current_monthly_cost", 0)
            smaller_cost = pricing_result.get("pricing_data", {}).get("on_demand", {}).get("monthly", 0)
            
            if smaller_cost < current_cost:
                opportunities.append({
                    "optimization_type": "Instance Right-sizing",
                    "description": f"Consider downsizing from {instance_type} to {smaller_type}",
                    "current_instance": instance_type,
                    "suggested_instance": smaller_type,
                    "monthly_savings": round(current_cost - smaller_cost, 2),
                    "annual_savings": round((current_cost - smaller_cost) * 12, 2),
                    "confidence": "medium",
                    "requirements": "Verify CPU and memory requirements before switching"
                })
    
    # Suggest Reserved Instances
    current_cost = config.get("current_monthly_cost", 0)
    if current_cost > 50:  # Only suggest RI for resources with significant cost
        opportunities.append({
            "optimization_type": "Reserved Instances",
            "description": "Use Reserved Instances for predictable workloads",
            "potential_action": "Purchase 1-year Reserved Instance",
            "monthly_savings": round(current_cost * 0.3, 2),  # Assume 30% savings
            "annual_savings": round(current_cost * 0.3 * 12, 2),
            "confidence": "high",
            "requirements": "Workload must run consistently for at least 1 year"
        })
    
    return opportunities


def _analyze_rds_price_optimization(config: Dict[str, Any], region: str) -> List[Dict[str, Any]]:
    """Analyze RDS-specific price optimization opportunities"""
    opportunities = []
    
    # Suggest Reserved Instances for RDS
    current_cost = config.get("current_monthly_cost", 0)
    if current_cost > 100:
        opportunities.append({
            "optimization_type": "RDS Reserved Instances",
            "description": "Use Reserved Instances for production databases",
            "potential_action": "Purchase 1-year RDS Reserved Instance",
            "monthly_savings": round(current_cost * 0.4, 2),  # RDS RI typically saves more
            "annual_savings": round(current_cost * 0.4 * 12, 2),
            "confidence": "high",
            "requirements": "Database must run consistently for at least 1 year"
        })
    
    # Suggest Aurora Serverless for variable workloads
    opportunities.append({
        "optimization_type": "Aurora Serverless",
        "description": "Consider Aurora Serverless for variable database workloads",
        "potential_action": "Migrate to Aurora Serverless v2",
        "monthly_savings": round(current_cost * 0.2, 2),  # Conservative estimate
        "annual_savings": round(current_cost * 0.2 * 12, 2),
        "confidence": "medium",
        "requirements": "Suitable for applications with variable database load"
    })
    
    return opportunities


def _analyze_lambda_price_optimization(config: Dict[str, Any], region: str) -> List[Dict[str, Any]]:
    """Analyze Lambda-specific price optimization opportunities"""
    opportunities = []
    
    # Suggest memory optimization
    opportunities.append({
        "optimization_type": "Lambda Memory Optimization",
        "description": "Optimize Lambda memory allocation for cost/performance balance",
        "potential_action": "Use AWS Lambda Power Tuning tool",
        "monthly_savings": 15.0,  # This would be calculated from actual usage
        "annual_savings": 180.0,
        "confidence": "high",
        "requirements": "Analyze execution duration vs memory allocation"
    })
    
    return opportunities


def _analyze_ebs_price_optimization(config: Dict[str, Any], region: str) -> List[Dict[str, Any]]:
    """Analyze EBS-specific price optimization opportunities"""
    opportunities = []
    
    volume_type = config.get("volume_type", "gp2")
    
    if volume_type == "gp2":
        opportunities.append({
            "optimization_type": "EBS Volume Type Upgrade",
            "description": "Upgrade from gp2 to gp3 for better price/performance",
            "potential_action": "Migrate to gp3 volumes",
            "monthly_savings": 20.0,  # gp3 is typically 20% cheaper than gp2
            "annual_savings": 240.0,
            "confidence": "high",
            "requirements": "No downtime required for migration"
        })
    
    return opportunities


def _get_alternative_instance_types(current_type: str, requirements: Dict[str, Any]) -> List[str]:
    """Get alternative instance types based on requirements"""
    # This would use a comprehensive instance type database
    # For now, return some common alternatives
    alternatives_map = {
        "m5.large": ["t3.large", "m5a.large", "m4.large"],
        "m5.xlarge": ["t3.xlarge", "m5a.xlarge", "m4.xlarge"],
        "c5.large": ["c5a.large", "c4.large", "m5.large"],
        "c5.xlarge": ["c5a.xlarge", "c4.xlarge", "m5.xlarge"],
        "r5.large": ["r5a.large", "r4.large", "m5.large"],
        "t3.medium": ["t3a.medium", "t2.medium", "t3.small"],
        "t3.large": ["t3a.large", "t2.large", "m5.large"]
    }
    
    return alternatives_map.get(current_type, [])


def _get_smaller_instance_types(current_type: str) -> List[str]:
    """Get smaller instance types for right-sizing"""
    size_hierarchy = {
        "xlarge": ["large", "medium"],
        "large": ["medium", "small"],
        "medium": ["small", "micro"],
        "small": ["micro"]
    }
    
    for size, smaller_sizes in size_hierarchy.items():
        if size in current_type:
            return [current_type.replace(size, smaller) for smaller in smaller_sizes]
    
    return []


def _get_instance_specifications(instance_type: str) -> Dict[str, Any]:
    """Get instance specifications (simplified)"""
    # This would call AWS API or maintain a comprehensive database
    specs_map = {
        "t3.micro": {"vcpu": 2, "memory_gb": 1, "network": "Low to Moderate", "ebs_optimized": True},
        "t3.small": {"vcpu": 2, "memory_gb": 2, "network": "Low to Moderate", "ebs_optimized": True},
        "t3.medium": {"vcpu": 2, "memory_gb": 4, "network": "Low to Moderate", "ebs_optimized": True},
        "t3.large": {"vcpu": 2, "memory_gb": 8, "network": "Low to Moderate", "ebs_optimized": True},
        "m5.large": {"vcpu": 2, "memory_gb": 8, "network": "Up to 10 Gbps", "ebs_optimized": True},
        "m5.xlarge": {"vcpu": 4, "memory_gb": 16, "network": "Up to 10 Gbps", "ebs_optimized": True},
        "c5.large": {"vcpu": 2, "memory_gb": 4, "network": "Up to 10 Gbps", "ebs_optimized": True},
        "c5.xlarge": {"vcpu": 4, "memory_gb": 8, "network": "Up to 10 Gbps", "ebs_optimized": True},
    }
    
    return specs_map.get(instance_type, {"vcpu": "N/A", "memory_gb": "N/A", "network": "N/A", "ebs_optimized": "N/A"})


def _calculate_compatibility_score(current_type: str, alternative_type: str, requirements: Dict[str, Any]) -> int:
    """Calculate compatibility score between instance types"""
    # Simplified compatibility scoring (0-100)
    current_specs = _get_instance_specifications(current_type)
    alt_specs = _get_instance_specifications(alternative_type)
    
    score = 100
    
    # Penalize for reduced CPU
    if alt_specs["vcpu"] < current_specs["vcpu"]:
        score -= 20
    
    # Penalize for reduced memory
    if alt_specs["memory_gb"] < current_specs["memory_gb"]:
        score -= 30
    
    # Bonus for same family
    if current_type.split('.')[0] == alternative_type.split('.')[0]:
        score += 10
    
    return max(0, min(100, score))


def _get_recommendation_reason(current_type: str, alternative_type: str, savings: float) -> str:
    """Generate recommendation reason"""
    if savings > 100:
        return f"Significant cost savings (${savings:.2f}/month) with similar performance characteristics"
    elif savings > 50:
        return f"Moderate cost savings (${savings:.2f}/month) - good value optimization"
    elif savings > 10:
        return f"Small cost savings (${savings:.2f}/month) - consider if performance is adequate"
    else:
        return "Minimal savings - evaluate based on specific requirements"


def _generate_optimization_summary(opportunities: List[Dict[str, Any]]) -> str:
    """Generate optimization summary"""
    if not opportunities:
        return "No price optimization opportunities found."
    
    total_savings = sum(opp.get("monthly_savings", 0) for opp in opportunities)
    high_impact = len([opp for opp in opportunities if opp.get("monthly_savings", 0) > 100])
    
    return f"Found {len(opportunities)} optimization opportunities with potential monthly savings of ${total_savings:.2f}. {high_impact} high-impact opportunities (>$100/month savings) identified."


def _generate_alternative_recommendation(alternatives: List[Dict[str, Any]], current_cost: float) -> str:
    """Generate recommendation for alternatives"""
    if not alternatives:
        return "No cost-effective alternatives found for current configuration."
    
    best_alt = alternatives[0]
    savings = best_alt["monthly_savings"]
    savings_pct = best_alt["savings_percentage"]
    
    return f"Recommended: Switch to {best_alt['instance_type']} to save ${savings:.2f}/month ({savings_pct}%). Total annual savings: ${savings * 12:.2f}."


def _generate_savings_recommendations(total_savings: float, analyses: List[Dict[str, Any]]) -> List[str]:
    """Generate savings recommendations"""
    recommendations = []
    
    if total_savings > 500:
        recommendations.append("High savings potential identified - prioritize implementation")
    
    reserved_strategies = [analysis for analysis in analyses 
                         if any(strategy["strategy"] == "Reserved Instances (1-year)" 
                               for strategy in analysis.get("applied_strategies", []))]
    
    if len(reserved_strategies) > 0:
        recommendations.append(f"Consider Reserved Instances for {len(reserved_strategies)} resources")
    
    if total_savings > 1000:
        recommendations.append("Consider dedicated cost optimization review with AWS")
    
    recommendations.append("Implement monitoring to track actual savings after optimization")
    
    return recommendations


def _suggest_instance_optimizations(instance_type: str, resource_values: Dict[str, Any], region: str) -> List[Dict[str, Any]]:
    """Suggest optimizations for a specific instance"""
    optimizations = []
    
    # Get current pricing
    current_pricing = get_real_aws_pricing("EC2", instance_type, region)
    if current_pricing.get("status") != "success":
        return optimizations
    
    current_cost = current_pricing.get("pricing_data", {}).get("on_demand", {}).get("monthly", 0)
    
    # Suggest Reserved Instance
    reserved_cost = current_pricing.get("pricing_data", {}).get("reserved_1year", {}).get("monthly", 0)
    if reserved_cost > 0 and reserved_cost < current_cost:
        optimizations.append({
            "strategy": "Reserved Instance (1-year)",
            "description": f"Switch to Reserved Instance pricing",
            "optimized_monthly_cost": reserved_cost,
            "monthly_savings": current_cost - reserved_cost,
            "implementation": "Purchase Reserved Instance through AWS Console"
        })
    
    # Suggest right-sizing
    smaller_types = _get_smaller_instance_types(instance_type)
    for smaller_type in smaller_types[:1]:  # Only check the next smaller size
        smaller_pricing = get_real_aws_pricing("EC2", smaller_type, region)
        if smaller_pricing.get("status") == "success":
            smaller_cost = smaller_pricing.get("pricing_data", {}).get("on_demand", {}).get("monthly", 0)
            if smaller_cost < current_cost:
                optimizations.append({
                    "strategy": "Right-sizing",
                    "description": f"Downsize to {smaller_type}",
                    "optimized_monthly_cost": smaller_cost,
                    "monthly_savings": current_cost - smaller_cost,
                    "implementation": f"Update Terraform: instance_type = \"{smaller_type}\""
                })
                break
    
    return optimizations


def _generate_terraform_optimization_recommendations(resource_optimizations: List[Dict[str, Any]], total_savings: float) -> List[str]:
    """Generate Terraform-specific optimization recommendations"""
    recommendations = []
    
    if total_savings > 100:
        recommendations.append(f"Implement suggested optimizations to save ${total_savings:.2f}/month")
    
    ri_opportunities = len([opt for opt in resource_optimizations 
                           if opt.get("optimization_applied", {}).get("strategy") == "Reserved Instance (1-year)"])
    
    if ri_opportunities > 0:
        recommendations.append(f"Consider Reserved Instances for {ri_opportunities} resources after deployment")
    
    recommendations.append("Use Terraform variables for instance types to easily implement changes")
    recommendations.append("Add cost tags to resources for better cost tracking")
    
    return recommendations