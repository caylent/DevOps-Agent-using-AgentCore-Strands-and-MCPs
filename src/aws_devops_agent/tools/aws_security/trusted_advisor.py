"""
AWS Trusted Advisor Analysis Tools
Real best practices analysis using AWS Trusted Advisor APIs
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
def get_trusted_advisor_checks(
    check_categories: List[str] = None,
    check_statuses: List[str] = None
) -> Dict[str, Any]:
    """
    Get Trusted Advisor checks and their status
    
    Args:
        check_categories: List of categories to filter (cost_optimizing, security, fault_tolerance, performance_optimizing, service_limits)
        check_statuses: List of statuses to filter (ok, warning, error, not_available)
    
    Returns:
        Dict containing Trusted Advisor checks
    """
    try:
        support = boto3.client('support')
        
        # Get all checks
        response = support.describe_trusted_advisor_checks(
            language='en'
        )
        
        checks = response.get('checks', [])
        
        # Filter by categories if specified
        if check_categories:
            checks = [check for check in checks if check.get('category') in check_categories]
        
        # Get check results
        check_ids = [check['id'] for check in checks]
        
        if check_ids:
            results_response = support.describe_trusted_advisor_check_result(
                checkId=check_ids[0]  # Get first check result as example
            )
            sample_result = results_response.get('result', {})
        else:
            sample_result = {}
        
        # Analyze checks
        analysis = _analyze_trusted_advisor_checks(checks, sample_result)
        
        return {
            "status": "success",
            "data_source": "AWS Trusted Advisor (Real-time)",
            "total_checks": len(checks),
            "analysis": analysis,
            "checks": checks[:10],  # Include first 10 checks for reference
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Trusted Advisor checks retrieval failed: {str(e)}",
            "suggestion": "Ensure you have AWS Support access and proper IAM permissions"
        }


@tool
@rate_limit(calls_per_second=2)
def analyze_trusted_advisor_recommendations(
    check_id: str = None,
    category: str = None
) -> Dict[str, Any]:
    """
    Analyze Trusted Advisor recommendations
    
    Args:
        check_id: Specific check ID to analyze
        category: Category to analyze (cost_optimizing, security, fault_tolerance, performance_optimizing, service_limits)
    
    Returns:
        Dict containing Trusted Advisor recommendations analysis
    """
    try:
        support = boto3.client('support')
        
        if check_id:
            # Get specific check result
            response = support.describe_trusted_advisor_check_result(
                checkId=check_id
            )
            check_result = response.get('result', {})
            
            # Get check details
            check_response = support.describe_trusted_advisor_checks(
                checkIds=[check_id]
            )
            check_details = check_response.get('checks', [])
            
            analysis = _analyze_specific_check(check_details[0] if check_details else {}, check_result)
            
            return {
                "status": "success",
                "data_source": "AWS Trusted Advisor (Real-time)",
                "check_id": check_id,
                "analysis": analysis,
                "check_result": check_result,
                "last_updated": datetime.now().isoformat()
            }
        else:
            # Get all checks in category
            response = support.describe_trusted_advisor_checks(
                language='en'
            )
            
            all_checks = response.get('checks', [])
            
            # Filter by category if specified
            if category:
                checks = [check for check in all_checks if check.get('category') == category]
            else:
                checks = all_checks
            
            # Get check summaries
            check_ids = [check['id'] for check in checks]
            
            if check_ids:
                summaries_response = support.describe_trusted_advisor_check_summaries(
                    checkIds=check_ids
                )
                summaries = summaries_response.get('summaries', [])
            else:
                summaries = []
            
            # Analyze recommendations
            analysis = _analyze_trusted_advisor_recommendations(checks, summaries)
            
            return {
                "status": "success",
                "data_source": "AWS Trusted Advisor (Real-time)",
                "category": category or "all",
                "total_checks": len(checks),
                "analysis": analysis,
                "checks": checks[:10],  # Include first 10 checks for reference
                "summaries": summaries[:10],  # Include first 10 summaries for reference
                "last_updated": datetime.now().isoformat()
            }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Trusted Advisor recommendations analysis failed: {str(e)}",
            "suggestion": "Ensure you have AWS Support access and proper IAM permissions"
        }


@tool
@rate_limit(calls_per_second=2)
def get_security_recommendations() -> Dict[str, Any]:
    """
    Get security-specific recommendations from Trusted Advisor
    
    Returns:
        Dict containing security recommendations
    """
    try:
        support = boto3.client('support')
        
        # Get security checks
        response = support.describe_trusted_advisor_checks(
            language='en'
        )
        
        all_checks = response.get('checks', [])
        security_checks = [check for check in all_checks if check.get('category') == 'security']
        
        # Get check summaries
        check_ids = [check['id'] for check in security_checks]
        
        if check_ids:
            summaries_response = support.describe_trusted_advisor_check_summaries(
                checkIds=check_ids
            )
            summaries = summaries_response.get('summaries', [])
        else:
            summaries = []
        
        # Analyze security recommendations
        analysis = _analyze_security_recommendations(security_checks, summaries)
        
        return {
            "status": "success",
            "data_source": "AWS Trusted Advisor (Real-time)",
            "total_security_checks": len(security_checks),
            "analysis": analysis,
            "security_checks": security_checks,
            "summaries": summaries,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Security recommendations retrieval failed: {str(e)}",
            "suggestion": "Ensure you have AWS Support access and proper IAM permissions"
        }


def _analyze_trusted_advisor_checks(checks: List[Dict[str, Any]], sample_result: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze Trusted Advisor checks"""
    if not checks:
        return {
            "category_breakdown": {},
            "status_breakdown": {},
            "summary": "No checks available"
        }
    
    # Category breakdown
    category_counts = {}
    for check in checks:
        category = check.get('category', 'unknown')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Status breakdown (from sample result)
    status_breakdown = {}
    if sample_result:
        status = sample_result.get('status', 'unknown')
        status_breakdown[status] = 1
    
    return {
        "category_breakdown": category_counts,
        "status_breakdown": status_breakdown,
        "total_checks": len(checks),
        "available_categories": list(category_counts.keys())
    }


def _analyze_specific_check(check_details: Dict[str, Any], check_result: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a specific Trusted Advisor check"""
    if not check_details:
        return {
            "check_name": "Unknown",
            "status": "No data available",
            "recommendations": []
        }
    
    check_name = check_details.get('name', 'Unknown')
    status = check_result.get('status', 'unknown')
    
    # Get flagged resources
    flagged_resources = check_result.get('flaggedResources', [])
    
    # Generate recommendations
    recommendations = []
    
    if status == 'ok':
        recommendations.append(f"Check '{check_name}' is passing - no action needed")
    elif status == 'warning':
        recommendations.append(f"Check '{check_name}' has warnings - review flagged resources")
        recommendations.append(f"Found {len(flagged_resources)} flagged resources")
    elif status == 'error':
        recommendations.append(f"Check '{check_name}' has errors - immediate action required")
        recommendations.append(f"Found {len(flagged_resources)} flagged resources")
    else:
        recommendations.append(f"Check '{check_name}' status is {status} - investigate further")
    
    # Add specific recommendations based on check type
    if 'security' in check_name.lower():
        recommendations.append("Review security configurations and access controls")
    elif 'cost' in check_name.lower():
        recommendations.append("Review cost optimization opportunities")
    elif 'performance' in check_name.lower():
        recommendations.append("Review performance optimization opportunities")
    
    return {
        "check_name": check_name,
        "status": status,
        "flagged_resources_count": len(flagged_resources),
        "flagged_resources": flagged_resources[:5],  # Include first 5 flagged resources
        "recommendations": recommendations,
        "check_description": check_details.get('description', 'No description available')
    }


def _analyze_trusted_advisor_recommendations(checks: List[Dict[str, Any]], summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze Trusted Advisor recommendations"""
    if not checks:
        return {
            "recommendation_summary": {},
            "priority_actions": [],
            "summary": "No checks available"
        }
    
    # Create summary by status
    status_summary = {}
    priority_actions = []
    
    for summary in summaries:
        check_id = summary.get('checkId', 'unknown')
        status = summary.get('status', 'unknown')
        
        # Find corresponding check details
        check_details = next((check for check in checks if check['id'] == check_id), {})
        check_name = check_details.get('name', 'Unknown')
        
        status_summary[status] = status_summary.get(status, 0) + 1
        
        # Add to priority actions if not OK
        if status != 'ok':
            priority_actions.append({
                "check_name": check_name,
                "status": status,
                "check_id": check_id
            })
    
    # Generate overall recommendations
    recommendations = []
    
    error_count = status_summary.get('error', 0)
    warning_count = status_summary.get('warning', 0)
    
    if error_count > 0:
        recommendations.append(f"Address {error_count} critical issues immediately")
    if warning_count > 0:
        recommendations.append(f"Review {warning_count} warning items")
    
    if error_count == 0 and warning_count == 0:
        recommendations.append("All checks are passing - maintain current configuration")
    
    return {
        "recommendation_summary": status_summary,
        "priority_actions": priority_actions[:10],  # Limit to first 10
        "total_checks": len(checks),
        "recommendations": recommendations
    }


def _analyze_security_recommendations(security_checks: List[Dict[str, Any]], summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze security-specific recommendations"""
    if not security_checks:
        return {
            "security_issues": [],
            "recommendations": ["No security checks available"],
            "summary": "No security checks found"
        }
    
    security_issues = []
    recommendations = []
    
    # Analyze each security check
    for summary in summaries:
        check_id = summary.get('checkId', 'unknown')
        status = summary.get('status', 'unknown')
        
        # Find corresponding check details
        check_details = next((check for check in security_checks if check['id'] == check_id), {})
        check_name = check_details.get('name', 'Unknown')
        
        if status != 'ok':
            security_issues.append({
                "check_name": check_name,
                "status": status,
                "check_id": check_id,
                "description": check_details.get('description', 'No description available')
            })
    
    # Generate security-specific recommendations
    if security_issues:
        recommendations.append(f"Found {len(security_issues)} security issues that need attention")
        
        # Categorize by check type
        iam_issues = [issue for issue in security_issues if 'iam' in issue['check_name'].lower()]
        if iam_issues:
            recommendations.append(f"Review IAM configurations ({len(iam_issues)} issues)")
        
        access_issues = [issue for issue in security_issues if 'access' in issue['check_name'].lower()]
        if access_issues:
            recommendations.append(f"Review access controls ({len(access_issues)} issues)")
        
        encryption_issues = [issue for issue in security_issues if 'encryption' in issue['check_name'].lower()]
        if encryption_issues:
            recommendations.append(f"Review encryption settings ({len(encryption_issues)} issues)")
        
        recommendations.append("Prioritize security issues based on severity and impact")
    else:
        recommendations.append("No security issues found - maintain current security posture")
        recommendations.append("Continue regular security monitoring")
    
    return {
        "security_issues": security_issues,
        "total_security_checks": len(security_checks),
        "issues_found": len(security_issues),
        "recommendations": recommendations
    }
