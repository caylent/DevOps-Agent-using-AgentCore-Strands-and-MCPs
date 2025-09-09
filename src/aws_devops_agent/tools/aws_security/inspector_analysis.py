"""
Amazon Inspector Analysis Tools
Real vulnerability analysis using Amazon Inspector APIs
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
def analyze_inspector_findings(
    severity_filter: List[str] = None,
    finding_types: List[str] = None,
    resource_tags: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Analyze vulnerability findings from Amazon Inspector
    
    Args:
        severity_filter: List of severity levels to filter (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL)
        finding_types: List of finding types to filter (e.g., ['VULNERABILITY', 'PACKAGE_VULNERABILITY'])
        resource_tags: Dictionary of resource tags to filter by
    
    Returns:
        Dict containing vulnerability analysis
    """
    try:
        inspector = boto3.client('inspector2')
        
        # Build filters
        filters = {}
        
        if severity_filter:
            filters['severity'] = [{'comparison': 'EQUALS', 'value': sev} for sev in severity_filter]
        
        if finding_types:
            filters['type'] = [{'comparison': 'EQUALS', 'value': ft} for ft in finding_types]
        
        if resource_tags:
            tag_filters = []
            for key, value in resource_tags.items():
                tag_filters.append({
                    'comparison': 'EQUALS',
                    'key': key,
                    'value': value
                })
            filters['resourceTags'] = tag_filters
        
        # Get findings
        response = inspector.list_findings(
            filterCriteria=filters,
            maxResults=100
        )
        
        findings = response.get('findings', [])
        
        # Get detailed findings
        if findings:
            finding_arns = [finding['findingArn'] for finding in findings]
            detailed_response = inspector.batch_get_findings(
                findingArns=finding_arns
            )
            detailed_findings = detailed_response.get('findings', [])
        else:
            detailed_findings = []
        
        # Analyze findings
        analysis = _analyze_inspector_findings(detailed_findings)
        
        return {
            "status": "success",
            "data_source": "Amazon Inspector (Real-time)",
            "total_findings": len(findings),
            "analysis": analysis,
            "raw_findings": detailed_findings[:10],  # Include first 10 findings for reference
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Inspector analysis failed: {str(e)}",
            "suggestion": "Ensure Amazon Inspector is enabled and you have proper IAM permissions"
        }


@tool
@rate_limit(calls_per_second=2)
def get_vulnerability_assessment(
    resource_arn: str = None,
    assessment_run_arn: str = None
) -> Dict[str, Any]:
    """
    Get vulnerability assessment results
    
    Args:
        resource_arn: Specific resource ARN to assess
        assessment_run_arn: Specific assessment run ARN
    
    Returns:
        Dict containing vulnerability assessment
    """
    try:
        inspector = boto3.client('inspector2')
        
        # Build filters
        filters = {}
        
        if resource_arn:
            filters['resourceId'] = [{'comparison': 'EQUALS', 'value': resource_arn}]
        
        # Get findings
        response = inspector.list_findings(
            filterCriteria=filters,
            maxResults=100
        )
        
        findings = response.get('findings', [])
        
        # Get detailed findings
        if findings:
            finding_arns = [finding['findingArn'] for finding in findings]
            detailed_response = inspector.batch_get_findings(
                findingArns=finding_arns
            )
            detailed_findings = detailed_response.get('findings', [])
        else:
            detailed_findings = []
        
        # Analyze vulnerability assessment
        analysis = _analyze_vulnerability_assessment(detailed_findings, resource_arn)
        
        return {
            "status": "success",
            "data_source": "Amazon Inspector (Real-time)",
            "resource_arn": resource_arn or "all",
            "total_findings": len(findings),
            "analysis": analysis,
            "findings": detailed_findings,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Vulnerability assessment failed: {str(e)}",
            "suggestion": "Ensure Amazon Inspector is enabled and the resource is supported"
        }


@tool
@rate_limit(calls_per_second=2)
def check_security_vulnerabilities(
    package_name: str = None,
    cve_id: str = None,
    severity_threshold: str = "MEDIUM"
) -> Dict[str, Any]:
    """
    Check for specific security vulnerabilities
    
    Args:
        package_name: Specific package name to check
        cve_id: Specific CVE ID to check
        severity_threshold: Minimum severity level to include
    
    Returns:
        Dict containing vulnerability check results
    """
    try:
        inspector = boto3.client('inspector2')
        
        # Build filters
        filters = {}
        
        if package_name:
            filters['packageName'] = [{'comparison': 'EQUALS', 'value': package_name}]
        
        if cve_id:
            filters['cveId'] = [{'comparison': 'EQUALS', 'value': cve_id}]
        
        # Add severity filter
        severity_levels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL']
        threshold_index = severity_levels.index(severity_threshold) if severity_threshold in severity_levels else 2
        filters['severity'] = [{'comparison': 'EQUALS', 'value': sev} for sev in severity_levels[:threshold_index + 1]]
        
        # Get findings
        response = inspector.list_findings(
            filterCriteria=filters,
            maxResults=100
        )
        
        findings = response.get('findings', [])
        
        # Get detailed findings
        if findings:
            finding_arns = [finding['findingArn'] for finding in findings]
            detailed_response = inspector.batch_get_findings(
                findingArns=finding_arns
            )
            detailed_findings = detailed_response.get('findings', [])
        else:
            detailed_findings = []
        
        # Analyze vulnerabilities
        analysis = _analyze_security_vulnerabilities(detailed_findings, package_name, cve_id)
        
        return {
            "status": "success",
            "data_source": "Amazon Inspector (Real-time)",
            "package_name": package_name or "all",
            "cve_id": cve_id or "all",
            "severity_threshold": severity_threshold,
            "total_findings": len(findings),
            "analysis": analysis,
            "findings": detailed_findings,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Security vulnerability check failed: {str(e)}",
            "suggestion": "Ensure Amazon Inspector is enabled and you have proper IAM permissions"
        }


def _analyze_inspector_findings(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze Inspector findings and extract key metrics"""
    if not findings:
        return {
            "severity_breakdown": {},
            "vulnerability_types": {},
            "affected_resources": {},
            "risk_assessment": "No vulnerabilities found"
        }
    
    # Severity breakdown
    severity_counts = {}
    vulnerability_types = {}
    affected_resources = {}
    
    for finding in findings:
        # Severity analysis
        severity = finding.get('severity', 'UNKNOWN')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Vulnerability type analysis
        vuln_type = finding.get('type', 'UNKNOWN')
        vulnerability_types[vuln_type] = vulnerability_types.get(vuln_type, 0) + 1
        
        # Affected resources analysis
        resources = finding.get('resources', [])
        for resource in resources:
            resource_id = resource.get('id', 'Unknown')
            resource_type = resource.get('type', 'Unknown')
            if resource_id not in affected_resources:
                affected_resources[resource_id] = {
                    "type": resource_type,
                    "vulnerability_count": 0,
                    "severities": set()
                }
            affected_resources[resource_id]["vulnerability_count"] += 1
            affected_resources[resource_id]["severities"].add(severity)
    
    # Convert sets to lists for JSON serialization
    for resource_id in affected_resources:
        affected_resources[resource_id]["severities"] = list(affected_resources[resource_id]["severities"])
    
    # Risk assessment
    critical_count = severity_counts.get('CRITICAL', 0)
    high_count = severity_counts.get('HIGH', 0)
    
    if critical_count > 0:
        risk_assessment = f"Critical risk - {critical_count} critical vulnerabilities found"
    elif high_count > 5:
        risk_assessment = f"High risk - {high_count} high severity vulnerabilities found"
    elif high_count > 0:
        risk_assessment = f"Medium risk - {high_count} high severity vulnerabilities found"
    else:
        risk_assessment = "Low risk - No critical or high severity vulnerabilities"
    
    return {
        "severity_breakdown": severity_counts,
        "vulnerability_types": vulnerability_types,
        "affected_resources": affected_resources,
        "risk_assessment": risk_assessment,
        "total_findings": len(findings)
    }


def _analyze_vulnerability_assessment(findings: List[Dict[str, Any]], resource_arn: str = None) -> Dict[str, Any]:
    """Analyze vulnerability assessment for specific resources"""
    if not findings:
        return {
            "resource_arn": resource_arn or "all",
            "vulnerability_count": 0,
            "risk_level": "Low",
            "recommendations": ["No vulnerabilities found"]
        }
    
    # Analyze by resource
    resource_analysis = {}
    total_vulnerabilities = 0
    
    for finding in findings:
        resources = finding.get('resources', [])
        for resource in resources:
            resource_id = resource.get('id', 'Unknown')
            if resource_id not in resource_analysis:
                resource_analysis[resource_id] = {
                    "vulnerability_count": 0,
                    "severities": [],
                    "vulnerability_types": []
                }
            
            resource_analysis[resource_id]["vulnerability_count"] += 1
            resource_analysis[resource_id]["severities"].append(finding.get('severity', 'UNKNOWN'))
            resource_analysis[resource_id]["vulnerability_types"].append(finding.get('type', 'UNKNOWN'))
            total_vulnerabilities += 1
    
    # Calculate risk level
    max_severity = 'INFORMATIONAL'
    for resource_data in resource_analysis.values():
        for severity in resource_data["severities"]:
            if severity == 'CRITICAL':
                max_severity = 'CRITICAL'
                break
            elif severity == 'HIGH' and max_severity != 'CRITICAL':
                max_severity = 'HIGH'
            elif severity == 'MEDIUM' and max_severity not in ['CRITICAL', 'HIGH']:
                max_severity = 'MEDIUM'
            elif severity == 'LOW' and max_severity not in ['CRITICAL', 'HIGH', 'MEDIUM']:
                max_severity = 'LOW'
    
    # Generate recommendations
    recommendations = []
    if max_severity == 'CRITICAL':
        recommendations.append("Immediately patch critical vulnerabilities")
    elif max_severity == 'HIGH':
        recommendations.append("Prioritize patching high severity vulnerabilities")
    elif max_severity == 'MEDIUM':
        recommendations.append("Plan patching for medium severity vulnerabilities")
    else:
        recommendations.append("Monitor low severity vulnerabilities")
    
    recommendations.append(f"Total vulnerabilities found: {total_vulnerabilities}")
    
    return {
        "resource_arn": resource_arn or "all",
        "vulnerability_count": total_vulnerabilities,
        "risk_level": max_severity,
        "resource_analysis": resource_analysis,
        "recommendations": recommendations
    }


def _analyze_security_vulnerabilities(findings: List[Dict[str, Any]], package_name: str = None, cve_id: str = None) -> Dict[str, Any]:
    """Analyze specific security vulnerabilities"""
    if not findings:
        return {
            "package_name": package_name or "all",
            "cve_id": cve_id or "all",
            "vulnerability_count": 0,
            "affected_packages": {},
            "recommendations": ["No vulnerabilities found"]
        }
    
    # Analyze by package
    package_analysis = {}
    cve_analysis = {}
    
    for finding in findings:
        # Package analysis
        package_info = finding.get('packageVulnerabilityDetails', {})
        if package_info:
            package_name_found = package_info.get('packageName', 'Unknown')
            if package_name_found not in package_analysis:
                package_analysis[package_name_found] = {
                    "vulnerability_count": 0,
                    "severities": [],
                    "cves": set()
                }
            
            package_analysis[package_name_found]["vulnerability_count"] += 1
            package_analysis[package_name_found]["severities"].append(finding.get('severity', 'UNKNOWN'))
            
            # CVE analysis
            cves = package_info.get('vulnerabilityIds', [])
            for cve in cves:
                cve_id_found = cve.get('id', 'Unknown')
                package_analysis[package_name_found]["cves"].add(cve_id_found)
                
                if cve_id_found not in cve_analysis:
                    cve_analysis[cve_id_found] = {
                        "severity": finding.get('severity', 'UNKNOWN'),
                        "affected_packages": set(),
                        "description": finding.get('description', 'No description available')
                    }
                cve_analysis[cve_id_found]["affected_packages"].add(package_name_found)
    
    # Convert sets to lists for JSON serialization
    for package_data in package_analysis.values():
        package_data["cves"] = list(package_data["cves"])
    
    for cve_data in cve_analysis.values():
        cve_data["affected_packages"] = list(cve_data["affected_packages"])
    
    # Generate recommendations
    recommendations = []
    total_vulnerabilities = len(findings)
    
    if total_vulnerabilities > 0:
        recommendations.append(f"Found {total_vulnerabilities} vulnerabilities")
        
        if package_name:
            recommendations.append(f"Specific package '{package_name}' has vulnerabilities that need patching")
        
        if cve_id:
            recommendations.append(f"Specific CVE '{cve_id}' affects multiple packages")
        
        recommendations.append("Review and apply security patches for affected packages")
        recommendations.append("Consider updating to latest package versions")
    else:
        recommendations.append("No vulnerabilities found for the specified criteria")
    
    return {
        "package_name": package_name or "all",
        "cve_id": cve_id or "all",
        "vulnerability_count": total_vulnerabilities,
        "affected_packages": package_analysis,
        "cve_analysis": cve_analysis,
        "recommendations": recommendations
    }
