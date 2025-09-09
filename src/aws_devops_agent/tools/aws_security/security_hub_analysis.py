"""
AWS Security Hub Analysis Tools
Real security analysis using AWS Security Hub APIs
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


def safe_aws_api_call(api_function, *args, **kwargs):
    """Safely call AWS API with proper error handling"""
    try:
        result = api_function(*args, **kwargs)
        return {"status": "success", "data": result}
    except Exception as e:
        error_code = getattr(e, 'response', {}).get('Error', {}).get('Code', 'Unknown')
        if error_code in ['AccessDenied', 'UnauthorizedOperation']:
            return {"status": "error", "error": "Insufficient permissions for Security Hub access"}
        else:
            return {"status": "error", "error": f"Security Hub API call failed: {str(e)}"}


@tool
@rate_limit(calls_per_second=2)
def analyze_security_hub_findings(
    severity_filter: List[str] = None,
    resource_types: List[str] = None,
    time_range_days: int = 30
) -> Dict[str, Any]:
    """
    Analyze security findings from AWS Security Hub
    
    Args:
        severity_filter: List of severity levels to filter (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
        resource_types: List of resource types to filter (e.g., ['AwsEc2Instance', 'AwsS3Bucket'])
        time_range_days: Number of days to look back for findings
    
    Returns:
        Dict containing security findings analysis
    """
    try:
        # Initialize Security Hub client
        security_hub = boto3.client('securityhub')
        
        # Calculate time range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=time_range_days)
        
        # Build filters
        filters = {
            'RecordState': [{'Value': 'ACTIVE', 'Comparison': 'EQUALS'}],
            'CreatedAt': [
                {
                    'Start': start_time.isoformat(),
                    'End': end_time.isoformat()
                }
            ]
        }
        
        if severity_filter:
            filters['SeverityLabel'] = [{'Value': sev, 'Comparison': 'EQUALS'} for sev in severity_filter]
        
        if resource_types:
            filters['ResourceType'] = [{'Value': rt, 'Comparison': 'EQUALS'} for rt in resource_types]
        
        # Get findings
        response = security_hub.get_findings(
            Filters=filters,
            MaxResults=100
        )
        
        findings = response.get('Findings', [])
        
        # Analyze findings
        analysis = _analyze_security_findings(findings)
        
        return {
            "status": "success",
            "data_source": "AWS Security Hub (Real-time)",
            "time_range": f"{time_range_days} days",
            "total_findings": len(findings),
            "analysis": analysis,
            "raw_findings": findings[:10],  # Include first 10 findings for reference
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Security Hub analysis failed: {str(e)}",
            "suggestion": "Ensure Security Hub is enabled and you have proper IAM permissions"
        }


@tool
@rate_limit(calls_per_second=2)
def get_security_insights(
    insight_arn: str = None,
    insight_types: List[str] = None
) -> Dict[str, Any]:
    """
    Get security insights from AWS Security Hub
    
    Args:
        insight_arn: Specific insight ARN to analyze
        insight_types: List of insight types to retrieve
    
    Returns:
        Dict containing security insights
    """
    try:
        security_hub = boto3.client('securityhub')
        
        if insight_arn:
            # Get specific insight
            response = security_hub.get_insights(
                InsightArns=[insight_arn]
            )
        else:
            # Get all insights
            response = security_hub.get_insights()
        
        insights = response.get('Insights', [])
        
        # Filter by type if specified
        if insight_types:
            insights = [insight for insight in insights if insight.get('Name', '').split(' - ')[0] in insight_types]
        
        # Analyze insights
        analysis = _analyze_security_insights(insights)
        
        return {
            "status": "success",
            "data_source": "AWS Security Hub Insights (Real-time)",
            "total_insights": len(insights),
            "analysis": analysis,
            "insights": insights,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Security insights retrieval failed: {str(e)}",
            "suggestion": "Ensure Security Hub is enabled and you have proper IAM permissions"
        }


@tool
@rate_limit(calls_per_second=2)
def analyze_security_posture(
    account_id: str = None,
    region: str = None
) -> Dict[str, Any]:
    """
    Analyze overall security posture using Security Hub data
    
    Args:
        account_id: Specific account ID to analyze (if None, uses current account)
        region: Specific region to analyze (if None, uses current region)
    
    Returns:
        Dict containing security posture analysis
    """
    try:
        security_hub = boto3.client('securityhub')
        
        # Get all active findings
        response = security_hub.get_findings(
            Filters={
                'RecordState': [{'Value': 'ACTIVE', 'Comparison': 'EQUALS'}]
            },
            MaxResults=1000
        )
        
        findings = response.get('Findings', [])
        
        # Filter by account and region if specified
        if account_id:
            findings = [f for f in findings if f.get('AwsAccountId') == account_id]
        
        if region:
            findings = [f for f in findings if f.get('Region') == region]
        
        # Analyze security posture
        posture_analysis = _analyze_security_posture(findings)
        
        return {
            "status": "success",
            "data_source": "AWS Security Hub (Real-time)",
            "account_id": account_id or "current",
            "region": region or "current",
            "total_findings": len(findings),
            "posture_analysis": posture_analysis,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Security posture analysis failed: {str(e)}",
            "suggestion": "Ensure Security Hub is enabled and you have proper IAM permissions"
        }


def _analyze_security_findings(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze security findings and extract key metrics"""
    if not findings:
        return {
            "severity_breakdown": {},
            "top_threats": [],
            "resource_analysis": {},
            "compliance_status": "No findings available"
        }
    
    # Severity breakdown
    severity_counts = {}
    for finding in findings:
        severity = finding.get('Severity', {}).get('Label', 'UNKNOWN')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    # Top threats by count
    threat_counts = {}
    for finding in findings:
        threat = finding.get('Title', 'Unknown Threat')
        threat_counts[threat] = threat_counts.get(threat, 0) + 1
    
    top_threats = sorted(threat_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Resource analysis
    resource_counts = {}
    for finding in findings:
        resources = finding.get('Resources', [])
        for resource in resources:
            resource_type = resource.get('Type', 'Unknown')
            resource_counts[resource_type] = resource_counts.get(resource_type, 0) + 1
    
    # Compliance status
    critical_high_count = severity_counts.get('CRITICAL', 0) + severity_counts.get('HIGH', 0)
    if critical_high_count == 0:
        compliance_status = "Good - No critical or high severity findings"
    elif critical_high_count < 5:
        compliance_status = "Moderate - Some critical/high severity findings"
    else:
        compliance_status = "Poor - Multiple critical/high severity findings"
    
    return {
        "severity_breakdown": severity_counts,
        "top_threats": [{"threat": threat, "count": count} for threat, count in top_threats],
        "resource_analysis": resource_counts,
        "compliance_status": compliance_status,
        "total_findings": len(findings)
    }


def _analyze_security_insights(insights: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze security insights"""
    if not insights:
        return {
            "insight_categories": {},
            "top_insights": [],
            "summary": "No insights available"
        }
    
    # Categorize insights
    categories = {}
    for insight in insights:
        name = insight.get('Name', 'Unknown')
        category = name.split(' - ')[0] if ' - ' in name else 'Other'
        categories[category] = categories.get(category, 0) + 1
    
    # Top insights by result count
    top_insights = sorted(insights, key=lambda x: x.get('ResultCount', 0), reverse=True)[:5]
    
    return {
        "insight_categories": categories,
        "top_insights": [
            {
                "name": insight.get('Name', 'Unknown'),
                "result_count": insight.get('ResultCount', 0),
                "arn": insight.get('InsightArn', '')
            }
            for insight in top_insights
        ],
        "total_insights": len(insights)
    }


def _analyze_security_posture(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze overall security posture"""
    if not findings:
        return {
            "overall_score": 100,
            "risk_level": "Low",
            "recommendations": ["No security findings detected"],
            "compliance_status": "Compliant"
        }
    
    # Calculate security score
    total_findings = len(findings)
    critical_count = sum(1 for f in findings if f.get('Severity', {}).get('Label') == 'CRITICAL')
    high_count = sum(1 for f in findings if f.get('Severity', {}).get('Label') == 'HIGH')
    medium_count = sum(1 for f in findings if f.get('Severity', {}).get('Label') == 'MEDIUM')
    low_count = sum(1 for f in findings if f.get('Severity', {}).get('Label') == 'LOW')
    
    # Calculate score (100 - weighted penalties)
    score = 100 - (critical_count * 20) - (high_count * 10) - (medium_count * 5) - (low_count * 1)
    score = max(0, min(100, score))
    
    # Determine risk level
    if score >= 80:
        risk_level = "Low"
    elif score >= 60:
        risk_level = "Medium"
    elif score >= 40:
        risk_level = "High"
    else:
        risk_level = "Critical"
    
    # Generate recommendations
    recommendations = []
    if critical_count > 0:
        recommendations.append(f"Address {critical_count} critical security findings immediately")
    if high_count > 0:
        recommendations.append(f"Review and remediate {high_count} high severity findings")
    if medium_count > 0:
        recommendations.append(f"Plan remediation for {medium_count} medium severity findings")
    if low_count > 0:
        recommendations.append(f"Monitor {low_count} low severity findings")
    
    if not recommendations:
        recommendations.append("Maintain current security posture")
    
    # Compliance status
    if critical_count > 0 or high_count > 5:
        compliance_status = "Non-compliant"
    elif high_count > 0 or medium_count > 10:
        compliance_status = "Partially compliant"
    else:
        compliance_status = "Compliant"
    
    return {
        "overall_score": score,
        "risk_level": risk_level,
        "severity_breakdown": {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count
        },
        "recommendations": recommendations,
        "compliance_status": compliance_status,
        "total_findings": total_findings
    }
