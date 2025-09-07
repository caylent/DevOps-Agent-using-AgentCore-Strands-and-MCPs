"""
AWS Config Compliance Analysis Tools
Real compliance analysis using AWS Config APIs
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from strands import tool

# Rate limiting decorator
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    """Rate limiting decorator for AWS API calls"""
    def decorator(func):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 1.0 / calls_per_second - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator


@tool
@rate_limit(calls_per_second=2)
def analyze_config_compliance(
    config_rule_names: List[str] = None,
    compliance_types: List[str] = None,
    resource_types: List[str] = None
) -> Dict[str, Any]:
    """
    Analyze compliance status using AWS Config
    
    Args:
        config_rule_names: List of specific Config rule names to check
        compliance_types: List of compliance types to filter (COMPLIANT, NON_COMPLIANT, NOT_APPLICABLE, INSUFFICIENT_DATA)
        resource_types: List of resource types to filter
    
    Returns:
        Dict containing compliance analysis
    """
    try:
        config = boto3.client('config')
        
        # Get compliance details
        if config_rule_names:
            compliance_results = []
            for rule_name in config_rule_names:
                try:
                    response = config.get_compliance_details_by_config_rule(
                        ConfigRuleName=rule_name,
                        ComplianceTypes=compliance_types or ['COMPLIANT', 'NON_COMPLIANT']
                    )
                    compliance_results.extend(response.get('EvaluationResults', []))
                except Exception as e:
                    print(f"Warning: Could not get compliance for rule {rule_name}: {e}")
        else:
            # Get all compliance details
            response = config.get_compliance_details_by_config_rule(
                ComplianceTypes=compliance_types or ['COMPLIANT', 'NON_COMPLIANT']
            )
            compliance_results = response.get('EvaluationResults', [])
        
        # Filter by resource types if specified
        if resource_types:
            compliance_results = [
                result for result in compliance_results
                if result.get('EvaluationResultIdentifier', {}).get('EvaluationResultQualifier', {}).get('ResourceType') in resource_types
            ]
        
        # Analyze compliance
        analysis = _analyze_compliance_results(compliance_results)
        
        return {
            "status": "success",
            "data_source": "AWS Config (Real-time)",
            "total_evaluations": len(compliance_results),
            "analysis": analysis,
            "compliance_results": compliance_results[:10],  # Include first 10 results for reference
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Config compliance analysis failed: {str(e)}",
            "suggestion": "Ensure AWS Config is enabled and you have proper IAM permissions"
        }


@tool
@rate_limit(calls_per_second=2)
def get_compliance_details(
    config_rule_name: str,
    resource_id: str = None
) -> Dict[str, Any]:
    """
    Get detailed compliance information for a specific Config rule
    
    Args:
        config_rule_name: Name of the Config rule to check
        resource_id: Specific resource ID to check (optional)
    
    Returns:
        Dict containing detailed compliance information
    """
    try:
        config = boto3.client('config')
        
        # Get compliance details for the rule
        response = config.get_compliance_details_by_config_rule(
            ConfigRuleName=config_rule_name,
            ComplianceTypes=['COMPLIANT', 'NON_COMPLIANT', 'NOT_APPLICABLE', 'INSUFFICIENT_DATA']
        )
        
        evaluation_results = response.get('EvaluationResults', [])
        
        # Filter by resource ID if specified
        if resource_id:
            evaluation_results = [
                result for result in evaluation_results
                if result.get('EvaluationResultIdentifier', {}).get('EvaluationResultQualifier', {}).get('ResourceId') == resource_id
            ]
        
        # Analyze detailed compliance
        analysis = _analyze_detailed_compliance(evaluation_results, config_rule_name)
        
        return {
            "status": "success",
            "data_source": "AWS Config (Real-time)",
            "config_rule_name": config_rule_name,
            "resource_id": resource_id or "all",
            "total_evaluations": len(evaluation_results),
            "analysis": analysis,
            "evaluation_results": evaluation_results,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Compliance details retrieval failed: {str(e)}",
            "suggestion": "Ensure the Config rule exists and you have proper IAM permissions"
        }


@tool
@rate_limit(calls_per_second=2)
def check_resource_compliance(
    resource_type: str,
    resource_id: str = None
) -> Dict[str, Any]:
    """
    Check compliance status for specific resources
    
    Args:
        resource_type: Type of resource to check (e.g., 'AWS::EC2::Instance')
        resource_id: Specific resource ID to check (optional)
    
    Returns:
        Dict containing resource compliance information
    """
    try:
        config = boto3.client('config')
        
        # Get compliance details for all rules
        response = config.get_compliance_details_by_config_rule(
            ComplianceTypes=['COMPLIANT', 'NON_COMPLIANT', 'NOT_APPLICABLE', 'INSUFFICIENT_DATA']
        )
        
        evaluation_results = response.get('EvaluationResults', [])
        
        # Filter by resource type and ID
        filtered_results = []
        for result in evaluation_results:
            qualifier = result.get('EvaluationResultIdentifier', {}).get('EvaluationResultQualifier', {})
            if qualifier.get('ResourceType') == resource_type:
                if resource_id is None or qualifier.get('ResourceId') == resource_id:
                    filtered_results.append(result)
        
        # Analyze resource compliance
        analysis = _analyze_resource_compliance(filtered_results, resource_type, resource_id)
        
        return {
            "status": "success",
            "data_source": "AWS Config (Real-time)",
            "resource_type": resource_type,
            "resource_id": resource_id or "all",
            "total_evaluations": len(filtered_results),
            "analysis": analysis,
            "evaluation_results": filtered_results,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Resource compliance check failed: {str(e)}",
            "suggestion": "Ensure AWS Config is enabled and the resource type is supported"
        }


def _analyze_compliance_results(evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze compliance evaluation results"""
    if not evaluation_results:
        return {
            "compliance_summary": {},
            "non_compliant_resources": [],
            "compliance_score": 100,
            "recommendations": ["No compliance data available"]
        }
    
    # Count compliance types
    compliance_counts = {}
    non_compliant_resources = []
    
    for result in evaluation_results:
        compliance_type = result.get('ComplianceType', 'UNKNOWN')
        compliance_counts[compliance_type] = compliance_counts.get(compliance_type, 0) + 1
        
        if compliance_type == 'NON_COMPLIANT':
            qualifier = result.get('EvaluationResultIdentifier', {}).get('EvaluationResultQualifier', {})
            resource_id = qualifier.get('ResourceId', 'Unknown')
            resource_type = qualifier.get('ResourceType', 'Unknown')
            non_compliant_resources.append({
                "resource_id": resource_id,
                "resource_type": resource_type,
                "rule_name": result.get('EvaluationResultIdentifier', {}).get('ConfigRuleName', 'Unknown')
            })
    
    # Calculate compliance score
    total_evaluations = len(evaluation_results)
    compliant_count = compliance_counts.get('COMPLIANT', 0)
    compliance_score = (compliant_count / total_evaluations * 100) if total_evaluations > 0 else 100
    
    # Generate recommendations
    recommendations = []
    non_compliant_count = compliance_counts.get('NON_COMPLIANT', 0)
    if non_compliant_count > 0:
        recommendations.append(f"Address {non_compliant_count} non-compliant resources")
    
    insufficient_data_count = compliance_counts.get('INSUFFICIENT_DATA', 0)
    if insufficient_data_count > 0:
        recommendations.append(f"Investigate {insufficient_data_count} resources with insufficient data")
    
    not_applicable_count = compliance_counts.get('NOT_APPLICABLE', 0)
    if not_applicable_count > 0:
        recommendations.append(f"Review {not_applicable_count} resources marked as not applicable")
    
    if not recommendations:
        recommendations.append("All resources are compliant")
    
    return {
        "compliance_summary": compliance_counts,
        "non_compliant_resources": non_compliant_resources[:10],  # Limit to first 10
        "compliance_score": round(compliance_score, 2),
        "total_evaluations": total_evaluations,
        "recommendations": recommendations
    }


def _analyze_detailed_compliance(evaluation_results: List[Dict[str, Any]], config_rule_name: str) -> Dict[str, Any]:
    """Analyze detailed compliance for a specific rule"""
    if not evaluation_results:
        return {
            "rule_name": config_rule_name,
            "compliance_status": "No data available",
            "resource_breakdown": {},
            "issues": []
        }
    
    # Analyze by resource
    resource_breakdown = {}
    issues = []
    
    for result in evaluation_results:
        qualifier = result.get('EvaluationResultIdentifier', {}).get('EvaluationResultQualifier', {})
        resource_id = qualifier.get('ResourceId', 'Unknown')
        resource_type = qualifier.get('ResourceType', 'Unknown')
        compliance_type = result.get('ComplianceType', 'UNKNOWN')
        
        # Track resource compliance
        if resource_id not in resource_breakdown:
            resource_breakdown[resource_id] = {
                "resource_type": resource_type,
                "compliance_status": compliance_type,
                "last_evaluation_time": result.get('ResultRecordedTime', 'Unknown')
            }
        
        # Collect issues for non-compliant resources
        if compliance_type == 'NON_COMPLIANT':
            annotation = result.get('Annotation', 'No details available')
            issues.append({
                "resource_id": resource_id,
                "resource_type": resource_type,
                "issue": annotation,
                "evaluation_time": result.get('ResultRecordedTime', 'Unknown')
            })
    
    # Overall compliance status
    total_resources = len(resource_breakdown)
    compliant_resources = sum(1 for r in resource_breakdown.values() if r['compliance_status'] == 'COMPLIANT')
    
    if total_resources == 0:
        compliance_status = "No data available"
    elif compliant_resources == total_resources:
        compliance_status = "Fully compliant"
    elif compliant_resources > total_resources * 0.8:
        compliance_status = "Mostly compliant"
    else:
        compliance_status = "Non-compliant"
    
    return {
        "rule_name": config_rule_name,
        "compliance_status": compliance_status,
        "total_resources": total_resources,
        "compliant_resources": compliant_resources,
        "resource_breakdown": resource_breakdown,
        "issues": issues[:10],  # Limit to first 10 issues
        "compliance_percentage": round((compliant_resources / total_resources * 100), 2) if total_resources > 0 else 0
    }


def _analyze_resource_compliance(evaluation_results: List[Dict[str, Any]], resource_type: str, resource_id: str = None) -> Dict[str, Any]:
    """Analyze compliance for specific resources"""
    if not evaluation_results:
        return {
            "resource_type": resource_type,
            "resource_id": resource_id or "all",
            "compliance_status": "No data available",
            "rule_breakdown": {},
            "recommendations": ["No compliance data available for this resource type"]
        }
    
    # Analyze by rule
    rule_breakdown = {}
    recommendations = []
    
    for result in evaluation_results:
        rule_name = result.get('EvaluationResultIdentifier', {}).get('ConfigRuleName', 'Unknown')
        compliance_type = result.get('ComplianceType', 'UNKNOWN')
        
        if rule_name not in rule_breakdown:
            rule_breakdown[rule_name] = {
                "compliance_status": compliance_type,
                "evaluation_time": result.get('ResultRecordedTime', 'Unknown')
            }
        
        # Generate recommendations for non-compliant resources
        if compliance_type == 'NON_COMPLIANT':
            annotation = result.get('Annotation', 'No details available')
            recommendations.append(f"Rule {rule_name}: {annotation}")
    
    # Overall compliance status
    total_rules = len(rule_breakdown)
    compliant_rules = sum(1 for r in rule_breakdown.values() if r['compliance_status'] == 'COMPLIANT')
    
    if total_rules == 0:
        compliance_status = "No data available"
    elif compliant_rules == total_rules:
        compliance_status = "Fully compliant"
    elif compliant_rules > total_rules * 0.8:
        compliance_status = "Mostly compliant"
    else:
        compliance_status = "Non-compliant"
    
    if not recommendations:
        recommendations.append("Resource is compliant with all applicable rules")
    
    return {
        "resource_type": resource_type,
        "resource_id": resource_id or "all",
        "compliance_status": compliance_status,
        "total_rules": total_rules,
        "compliant_rules": compliant_rules,
        "rule_breakdown": rule_breakdown,
        "recommendations": recommendations,
        "compliance_percentage": round((compliant_rules / total_rules * 100), 2) if total_rules > 0 else 0
    }
