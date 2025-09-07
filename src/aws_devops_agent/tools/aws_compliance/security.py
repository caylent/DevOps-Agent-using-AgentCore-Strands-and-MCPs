"""
AWS Compliance and Security Validation Tools
Security policies, compliance standards, and vulnerability scanning
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from strands import tool


@tool
def validate_security_policies(resource_type: str, configuration: Dict[str, Any], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Validate AWS resource configurations against security policies
    
    Args:
        resource_type: Type of AWS resource (EC2, RDS, S3, etc.)
        configuration: Resource configuration to validate
        region: AWS region
    
    Returns:
        Dict containing security policy validation results
    """
    try:
        validation_results = {
            "status": "success",
            "resource_type": resource_type,
            "region": region,
            "validation_timestamp": datetime.now().isoformat(),
            "data_source": "Security Policy Validation (Static Analysis - Mock Data)",
            "security_findings": [],
            "compliance_status": "unknown",
            "severity_summary": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "recommendations": []
        }
        
        # Validate based on resource type
        if resource_type.upper() == "EC2":
            findings = _validate_ec2_security_policies(configuration)
            validation_results["security_findings"].extend(findings)
        elif resource_type.upper() == "S3":
            findings = _validate_s3_security_policies(configuration)
            validation_results["security_findings"].extend(findings)
        elif resource_type.upper() == "RDS":
            findings = _validate_rds_security_policies(configuration)
            validation_results["security_findings"].extend(findings)
        elif resource_type.upper() == "LAMBDA":
            findings = _validate_lambda_security_policies(configuration)
            validation_results["security_findings"].extend(findings)
        else:
            findings = _validate_generic_security_policies(configuration)
            validation_results["security_findings"].extend(findings)
        
        # Calculate severity summary
        for finding in validation_results["security_findings"]:
            severity = finding.get("severity", "low")
            validation_results["severity_summary"][severity] += 1
        
        # Determine overall compliance status
        critical_count = validation_results["severity_summary"]["critical"]
        high_count = validation_results["severity_summary"]["high"]
        
        if critical_count > 0:
            validation_results["compliance_status"] = "non_compliant"
        elif high_count > 0:
            validation_results["compliance_status"] = "partially_compliant"
        else:
            validation_results["compliance_status"] = "compliant"
        
        # Generate recommendations
        validation_results["recommendations"] = _generate_security_recommendations(
            validation_results["security_findings"]
        )
        
        return validation_results
        
    except Exception as e:
        return {"status": "error", "error": f"Security policy validation failed: {str(e)}"}


@tool
def check_compliance_standards(standard: str, resource_configurations: List[Dict[str, Any]], region: str = "us-east-1") -> Dict[str, Any]:
    """
    Check compliance against industry standards (SOC2, HIPAA, PCI-DSS, etc.)
    
    Args:
        standard: Compliance standard (SOC2, HIPAA, PCI-DSS, ISO27001, etc.)
        resource_configurations: List of resource configurations to check
        region: AWS region
    
    Returns:
        Dict containing compliance check results
    """
    try:
        compliance_results = {
            "status": "success",
            "compliance_standard": standard.upper(),
            "region": region,
            "assessment_timestamp": datetime.now().isoformat(),
            "data_source": "Compliance Standards Check (Mock Data - Real AWS Config/Trusted Advisor integration needed)",
            "total_resources_checked": len(resource_configurations),
            "compliance_checks": [],
            "overall_compliance_score": 0,
            "compliant_controls": 0,
            "non_compliant_controls": 0,
            "remediation_actions": []
        }
        
        # Get compliance checks for the specific standard
        if standard.upper() == "SOC2":
            checks = _get_soc2_compliance_checks()
        elif standard.upper() == "HIPAA":
            checks = _get_hipaa_compliance_checks()
        elif standard.upper() == "PCI-DSS":
            checks = _get_pci_dss_compliance_checks()
        elif standard.upper() == "ISO27001":
            checks = _get_iso27001_compliance_checks()
        else:
            return {"status": "error", "error": f"Unsupported compliance standard: {standard}"}
        
        # Run compliance checks
        for check in checks:
            check_result = _run_compliance_check(check, resource_configurations)
            compliance_results["compliance_checks"].append(check_result)
            
            if check_result["status"] == "compliant":
                compliance_results["compliant_controls"] += 1
            else:
                compliance_results["non_compliant_controls"] += 1
                compliance_results["remediation_actions"].extend(check_result.get("remediation_actions", []))
        
        # Calculate overall compliance score
        total_checks = len(checks)
        if total_checks > 0:
            compliance_results["overall_compliance_score"] = round(
                (compliance_results["compliant_controls"] / total_checks) * 100, 1
            )
        
        return compliance_results
        
    except Exception as e:
        return {"status": "error", "error": f"Compliance standards check failed: {str(e)}"}


@tool
def generate_compliance_report(standard: str, assessment_results: Dict[str, Any], format: str = "json") -> Dict[str, Any]:
    """
    Generate comprehensive compliance report
    
    Args:
        standard: Compliance standard
        assessment_results: Results from compliance assessment
        format: Report format (json, pdf, excel)
    
    Returns:
        Dict containing the compliance report
    """
    try:
        report = {
            "status": "success",
            "report_metadata": {
                "standard": standard.upper(),
                "report_generated": datetime.now().isoformat(),
                "report_format": format,
                "assessment_period": "Current state",
                "report_version": "1.0"
            },
            "data_source": "Compliance Report Generation (Mock Data - Real AWS integration needed)",
            "executive_summary": {},
            "detailed_findings": {},
            "remediation_plan": {},
            "appendices": {}
        }
        
        # Generate executive summary
        if "overall_compliance_score" in assessment_results:
            score = assessment_results["overall_compliance_score"]
            report["executive_summary"] = {
                "compliance_score": f"{score}%",
                "compliance_level": _get_compliance_level(score),
                "total_controls_assessed": assessment_results.get("compliant_controls", 0) + assessment_results.get("non_compliant_controls", 0),
                "compliant_controls": assessment_results.get("compliant_controls", 0),
                "non_compliant_controls": assessment_results.get("non_compliant_controls", 0),
                "key_findings": _generate_key_findings(assessment_results),
                "recommended_actions": assessment_results.get("remediation_actions", [])[:5]  # Top 5 actions
            }
        
        # Generate detailed findings
        report["detailed_findings"] = {
            "compliance_checks": assessment_results.get("compliance_checks", []),
            "risk_assessment": _assess_compliance_risks(assessment_results),
            "gap_analysis": _perform_gap_analysis(assessment_results)
        }
        
        # Generate remediation plan
        report["remediation_plan"] = _generate_remediation_plan(assessment_results)
        
        # Generate appendices
        report["appendices"] = {
            "compliance_framework_reference": _get_framework_reference(standard),
            "technical_configurations": _extract_technical_configurations(assessment_results),
            "definitions_and_acronyms": _get_definitions_and_acronyms(standard)
        }
        
        return report
        
    except Exception as e:
        return {"status": "error", "error": f"Compliance report generation failed: {str(e)}"}


@tool
def scan_security_vulnerabilities(resource_type: str, scan_scope: str = "configuration", region: str = "us-east-1") -> Dict[str, Any]:
    """
    Scan for security vulnerabilities in AWS resources
    
    Args:
        resource_type: Type of AWS resource to scan
        scan_scope: Scope of scan (configuration, network, data, all)
        region: AWS region
    
    Returns:
        Dict containing vulnerability scan results
    """
    try:
        scan_results = {
            "status": "success",
            "resource_type": resource_type,
            "scan_scope": scan_scope,
            "region": region,
            "scan_timestamp": datetime.now().isoformat(),
            "data_source": "Security Vulnerability Scan (Mock Data - Real AWS Inspector/Security Hub integration needed)",
            "vulnerabilities": [],
            "vulnerability_summary": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
            "remediation_priority": [],
            "compliance_impact": []
        }
        
        # Perform vulnerability scans based on resource type and scope
        if scan_scope == "configuration" or scan_scope == "all":
            config_vulns = _scan_configuration_vulnerabilities(resource_type)
            scan_results["vulnerabilities"].extend(config_vulns)
        
        if scan_scope == "network" or scan_scope == "all":
            network_vulns = _scan_network_vulnerabilities(resource_type)
            scan_results["vulnerabilities"].extend(network_vulns)
        
        if scan_scope == "data" or scan_scope == "all":
            data_vulns = _scan_data_vulnerabilities(resource_type)
            scan_results["vulnerabilities"].extend(data_vulns)
        
        # Calculate vulnerability summary
        for vuln in scan_results["vulnerabilities"]:
            severity = vuln.get("severity", "info")
            scan_results["vulnerability_summary"][severity] += 1
        
        # Prioritize remediation
        scan_results["remediation_priority"] = _prioritize_remediation(scan_results["vulnerabilities"])
        
        # Assess compliance impact
        scan_results["compliance_impact"] = _assess_compliance_impact(scan_results["vulnerabilities"])
        
        return scan_results
        
    except Exception as e:
        return {"status": "error", "error": f"Security vulnerability scan failed: {str(e)}"}


# Helper functions for security policy validation
def _validate_ec2_security_policies(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate EC2 security policies"""
    findings = []
    
    # Check for public instances
    if config.get("associate_public_ip_address"):
        findings.append({
            "policy": "EC2-PUBLIC-ACCESS",
            "severity": "high",
            "finding": "EC2 instance has public IP address",
            "recommendation": "Use private instances with NAT Gateway or ALB",
            "cis_control": "CIS 4.1"
        })
    
    # Check security groups
    security_groups = config.get("security_groups", [])
    for sg in security_groups:
        if "0.0.0.0/0" in str(sg):
            findings.append({
                "policy": "EC2-SG-OPEN-TO-WORLD",
                "severity": "critical",
                "finding": "Security group allows access from 0.0.0.0/0",
                "recommendation": "Restrict source IP ranges to minimum required",
                "cis_control": "CIS 4.2"
            })
    
    return findings


def _validate_s3_security_policies(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate S3 security policies"""
    findings = []
    
    # Check public access
    if config.get("public_read_access") or config.get("public_write_access"):
        findings.append({
            "policy": "S3-PUBLIC-ACCESS",
            "severity": "critical",
            "finding": "S3 bucket allows public access",
            "recommendation": "Disable public access and use bucket policies",
            "cis_control": "CIS 2.1.1"
        })
    
    # Check encryption
    if not config.get("server_side_encryption"):
        findings.append({
            "policy": "S3-ENCRYPTION-DISABLED",
            "severity": "high",
            "finding": "S3 bucket encryption not enabled",
            "recommendation": "Enable AES-256 or KMS encryption",
            "cis_control": "CIS 2.1.2"
        })
    
    return findings


def _validate_rds_security_policies(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate RDS security policies"""
    findings = []
    
    # Check encryption
    if not config.get("encrypted"):
        findings.append({
            "policy": "RDS-ENCRYPTION-DISABLED",
            "severity": "high",
            "finding": "RDS instance encryption not enabled",
            "recommendation": "Enable encryption at rest",
            "cis_control": "CIS 2.3.1"
        })
    
    # Check public accessibility
    if config.get("publicly_accessible"):
        findings.append({
            "policy": "RDS-PUBLIC-ACCESS",
            "severity": "critical",
            "finding": "RDS instance is publicly accessible",
            "recommendation": "Disable public access and use private subnets",
            "cis_control": "CIS 2.3.2"
        })
    
    return findings


def _validate_lambda_security_policies(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate Lambda security policies"""
    findings = []
    
    # Check environment variables encryption
    if config.get("environment_variables") and not config.get("kms_key_arn"):
        findings.append({
            "policy": "LAMBDA-ENV-ENCRYPTION",
            "severity": "medium",
            "finding": "Lambda environment variables not encrypted with KMS",
            "recommendation": "Use KMS key to encrypt environment variables",
            "cis_control": "CIS 3.1"
        })
    
    return findings


def _validate_generic_security_policies(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Validate generic security policies"""
    findings = []
    
    # Check for missing tags
    if not config.get("tags"):
        findings.append({
            "policy": "RESOURCE-TAGGING",
            "severity": "low",
            "finding": "Resource missing required tags",
            "recommendation": "Add tags for compliance and cost management",
            "cis_control": "General"
        })
    
    return findings


# Helper functions for compliance standards
def _get_soc2_compliance_checks() -> List[Dict[str, Any]]:
    """Get SOC2 compliance checks"""
    return [
        {
            "control": "CC6.1",
            "description": "Network Security - Logical and physical access controls",
            "check_type": "security_groups",
            "requirements": ["no_open_security_groups", "principle_of_least_privilege"]
        },
        {
            "control": "CC6.7",
            "description": "Data Transmission - Data transmitted over networks is protected",
            "check_type": "encryption_in_transit",
            "requirements": ["https_only", "ssl_tls_encryption"]
        }
    ]


def _get_hipaa_compliance_checks() -> List[Dict[str, Any]]:
    """Get HIPAA compliance checks"""
    return [
        {
            "control": "164.312(a)(1)",
            "description": "Assigned security responsibility",
            "check_type": "access_controls",
            "requirements": ["iam_policies", "role_based_access"]
        },
        {
            "control": "164.312(e)(1)",
            "description": "Automatic logoff",
            "check_type": "session_management",
            "requirements": ["session_timeout", "automatic_logoff"]
        }
    ]


def _get_pci_dss_compliance_checks() -> List[Dict[str, Any]]:
    """Get PCI-DSS compliance checks"""
    return [
        {
            "control": "PCI-DSS 1.1.1",
            "description": "Firewall configuration standards",
            "check_type": "network_security",
            "requirements": ["firewall_rules", "network_segmentation"]
        }
    ]


def _get_iso27001_compliance_checks() -> List[Dict[str, Any]]:
    """Get ISO 27001 compliance checks"""
    return [
        {
            "control": "A.13.1.1",
            "description": "Network controls",
            "check_type": "network_security",
            "requirements": ["network_segregation", "access_controls"]
        }
    ]


def _run_compliance_check(check: Dict[str, Any], configurations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run individual compliance check"""
    # Simulate compliance check execution
    return {
        "control": check["control"],
        "description": check["description"],
        "status": "compliant" if len(configurations) > 0 else "non_compliant",
        "findings": [],
        "remediation_actions": ["Review and update configuration"] if len(configurations) == 0 else []
    }


def _generate_security_recommendations(findings: List[Dict[str, Any]]) -> List[str]:
    """Generate security recommendations based on findings"""
    recommendations = []
    
    critical_findings = [f for f in findings if f.get("severity") == "critical"]
    if critical_findings:
        recommendations.append("Address all critical security findings immediately")
    
    recommendations.extend([
        "Implement regular security assessments",
        "Enable CloudTrail for audit logging",
        "Use AWS Config for compliance monitoring",
        "Implement least privilege access principles"
    ])
    
    return recommendations[:10]  # Return top 10 recommendations


def _get_compliance_level(score: float) -> str:
    """Determine compliance level based on score"""
    if score >= 95:
        return "Excellent"
    elif score >= 85:
        return "Good"
    elif score >= 70:
        return "Satisfactory"
    elif score >= 50:
        return "Needs Improvement"
    else:
        return "Poor"


def _generate_key_findings(assessment_results: Dict[str, Any]) -> List[str]:
    """Generate key findings from assessment results"""
    findings = []
    
    non_compliant = assessment_results.get("non_compliant_controls", 0)
    if non_compliant > 0:
        findings.append(f"{non_compliant} non-compliant controls identified")
    
    findings.extend([
        "Regular security assessments recommended",
        "Implementation of automated compliance monitoring suggested"
    ])
    
    return findings[:5]


def _assess_compliance_risks(assessment_results: Dict[str, Any]) -> Dict[str, Any]:
    """Assess risks based on compliance results"""
    return {
        "overall_risk_level": "Medium",
        "key_risk_areas": ["Network Security", "Data Protection"],
        "risk_mitigation_priority": ["Critical findings first", "High findings second"]
    }


def _perform_gap_analysis(assessment_results: Dict[str, Any]) -> Dict[str, Any]:
    """Perform gap analysis"""
    return {
        "identified_gaps": ["Security policy documentation", "Automated monitoring"],
        "gap_priority": ["High", "Medium"],
        "recommended_timeline": "3-6 months for full compliance"
    }


def _generate_remediation_plan(assessment_results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate remediation plan"""
    return {
        "immediate_actions": assessment_results.get("remediation_actions", [])[:3],
        "short_term_actions": ["Implement automated monitoring", "Update security policies"],
        "long_term_actions": ["Regular compliance assessments", "Security awareness training"],
        "estimated_timeline": "3-6 months",
        "required_resources": ["Security team", "Cloud architects", "Compliance officer"]
    }


def _get_framework_reference(standard: str) -> Dict[str, Any]:
    """Get compliance framework reference"""
    return {
        "framework_name": standard,
        "version": "Latest",
        "reference_url": f"https://example.com/{standard.lower()}-framework",
        "key_principles": ["Confidentiality", "Integrity", "Availability"]
    }


def _extract_technical_configurations(assessment_results: Dict[str, Any]) -> Dict[str, Any]:
    """Extract technical configurations from assessment"""
    return {
        "assessed_resources": assessment_results.get("total_resources_checked", 0),
        "configuration_details": "Available upon request",
        "technical_standards": "AWS best practices applied"
    }


def _get_definitions_and_acronyms(standard: str) -> Dict[str, str]:
    """Get definitions and acronyms for the standard"""
    return {
        "AWS": "Amazon Web Services",
        "IAM": "Identity and Access Management",
        "VPC": "Virtual Private Cloud",
        "KMS": "Key Management Service"
    }


def _scan_configuration_vulnerabilities(resource_type: str) -> List[Dict[str, Any]]:
    """Scan for configuration vulnerabilities"""
    vulnerabilities = []
    
    if resource_type.upper() == "EC2":
        vulnerabilities.append({
            "vulnerability_id": "CONFIG-001",
            "severity": "high",
            "title": "Default security group allows all traffic",
            "description": "Default security group has overly permissive rules",
            "remediation": "Remove or restrict default security group rules"
        })
    
    return vulnerabilities


def _scan_network_vulnerabilities(resource_type: str) -> List[Dict[str, Any]]:
    """Scan for network vulnerabilities"""
    return [
        {
            "vulnerability_id": "NET-001",
            "severity": "medium",
            "title": "Network segmentation insufficient",
            "description": "Resources not properly segmented by network",
            "remediation": "Implement proper VPC and subnet design"
        }
    ]


def _scan_data_vulnerabilities(resource_type: str) -> List[Dict[str, Any]]:
    """Scan for data vulnerabilities"""
    return [
        {
            "vulnerability_id": "DATA-001",
            "severity": "critical",
            "title": "Data encryption at rest not enabled",
            "description": "Sensitive data stored without encryption",
            "remediation": "Enable encryption at rest using AWS KMS"
        }
    ]


def _prioritize_remediation(vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Prioritize remediation actions"""
    # Sort by severity: critical, high, medium, low, info
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    
    sorted_vulns = sorted(vulnerabilities, key=lambda x: severity_order.get(x.get("severity", "info"), 4))
    
    return [
        {
            "priority": i + 1,
            "vulnerability_id": vuln["vulnerability_id"],
            "title": vuln["title"],
            "severity": vuln["severity"],
            "remediation": vuln["remediation"]
        }
        for i, vuln in enumerate(sorted_vulns[:10])  # Top 10 priorities
    ]


def _assess_compliance_impact(vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Assess compliance impact of vulnerabilities"""
    impact_assessment = []
    
    for vuln in vulnerabilities:
        if vuln.get("severity") in ["critical", "high"]:
            impact_assessment.append({
                "vulnerability_id": vuln["vulnerability_id"],
                "compliance_frameworks_affected": ["SOC2", "HIPAA", "PCI-DSS"],
                "impact_level": "High",
                "required_action": "Immediate remediation required"
            })
    
    return impact_assessment