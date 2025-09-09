"""
Comprehensive Security Analysis Tools
Combines Security Hub, Config, Inspector, and Trusted Advisor for complete security analysis
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from strands import tool

from .security_hub_analysis import analyze_security_hub_findings, get_security_insights, analyze_security_posture
from .config_compliance import analyze_config_compliance, get_compliance_details, check_resource_compliance
from .inspector_analysis import analyze_inspector_findings, get_vulnerability_assessment, check_security_vulnerabilities
from .trusted_advisor import get_trusted_advisor_checks, analyze_trusted_advisor_recommendations, get_security_recommendations


@tool
def perform_comprehensive_security_analysis(
    account_id: str = None,
    region: str = None,
    include_findings: bool = True,
    include_compliance: bool = True,
    include_vulnerabilities: bool = True,
    include_recommendations: bool = True
) -> Dict[str, Any]:
    """
    Perform comprehensive security analysis using all available AWS security services
    
    Args:
        account_id: Specific account ID to analyze (if None, uses current account)
        region: Specific region to analyze (if None, uses current region)
        include_findings: Include Security Hub findings analysis
        include_compliance: Include Config compliance analysis
        include_vulnerabilities: Include Inspector vulnerability analysis
        include_recommendations: Include Trusted Advisor recommendations
    
    Returns:
        Dict containing comprehensive security analysis
    """
    try:
        analysis_results = {
            "status": "success",
            "data_source": "AWS Security Services (Real-time)",
            "account_id": account_id or "current",
            "region": region or "current",
            "analysis_timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # 1. Security Hub Analysis
        if include_findings:
            print("🔍 Analyzing Security Hub findings...")
            security_hub_result = analyze_security_hub_findings(
                severity_filter=['CRITICAL', 'HIGH', 'MEDIUM'],
                time_range_days=30
            )
            analysis_results["components"]["security_hub"] = security_hub_result
        
        # 2. Config Compliance Analysis
        if include_compliance:
            print("📋 Analyzing Config compliance...")
            config_result = analyze_config_compliance(
                compliance_types=['COMPLIANT', 'NON_COMPLIANT']
            )
            analysis_results["components"]["config_compliance"] = config_result
        
        # 3. Inspector Vulnerability Analysis
        if include_vulnerabilities:
            print("🔬 Analyzing Inspector vulnerabilities...")
            inspector_result = analyze_inspector_findings(
                severity_filter=['CRITICAL', 'HIGH', 'MEDIUM']
            )
            analysis_results["components"]["inspector_vulnerabilities"] = inspector_result
        
        # 4. Trusted Advisor Recommendations
        if include_recommendations:
            print("💡 Analyzing Trusted Advisor recommendations...")
            trusted_advisor_result = get_security_recommendations()
            analysis_results["components"]["trusted_advisor"] = trusted_advisor_result
        
        # 5. Generate comprehensive summary
        comprehensive_summary = _generate_comprehensive_summary(analysis_results["components"])
        analysis_results["comprehensive_summary"] = comprehensive_summary
        
        # 6. Generate actionable recommendations
        actionable_recommendations = _generate_actionable_recommendations(analysis_results["components"])
        analysis_results["actionable_recommendations"] = actionable_recommendations
        
        return analysis_results
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Comprehensive security analysis failed: {str(e)}",
            "suggestion": "Ensure all AWS security services are enabled and you have proper IAM permissions"
        }


@tool
def generate_security_report(
    analysis_results: Dict[str, Any],
    report_format: str = "comprehensive",
    include_details: bool = True
) -> Dict[str, Any]:
    """
    Generate a comprehensive security report from analysis results
    
    Args:
        analysis_results: Results from comprehensive security analysis
        report_format: Report format (comprehensive, executive, technical)
        include_details: Include detailed findings in the report
    
    Returns:
        Dict containing formatted security report
    """
    try:
        if analysis_results.get("status") != "success":
            return {
                "status": "error",
                "error": "Invalid analysis results provided",
                "suggestion": "Run comprehensive security analysis first"
            }
        
        components = analysis_results.get("components", {})
        comprehensive_summary = analysis_results.get("comprehensive_summary", {})
        actionable_recommendations = analysis_results.get("actionable_recommendations", [])
        
        # Generate report based on format
        if report_format == "executive":
            report = _generate_executive_report(comprehensive_summary, actionable_recommendations)
        elif report_format == "technical":
            report = _generate_technical_report(components, include_details)
        else:  # comprehensive
            report = _generate_comprehensive_report(components, comprehensive_summary, actionable_recommendations, include_details)
        
        return {
            "status": "success",
            "report_format": report_format,
            "report": report,
            "generated_at": datetime.now().isoformat(),
            "data_source": "AWS Security Services (Real-time)"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Security report generation failed: {str(e)}",
            "suggestion": "Check analysis results format and try again"
        }


def _generate_comprehensive_summary(components: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive summary from all analysis components"""
    summary = {
        "overall_security_score": 0,
        "risk_level": "Unknown",
        "total_issues": 0,
        "critical_issues": 0,
        "high_issues": 0,
        "medium_issues": 0,
        "compliance_status": "Unknown",
        "vulnerability_status": "Unknown",
        "recommendation_status": "Unknown"
    }
    
    # Analyze Security Hub findings
    if "security_hub" in components:
        security_hub = components["security_hub"]
        if security_hub.get("status") == "success":
            analysis = security_hub.get("analysis", {})
            severity_breakdown = analysis.get("severity_breakdown", {})
            
            summary["critical_issues"] += severity_breakdown.get("CRITICAL", 0)
            summary["high_issues"] += severity_breakdown.get("HIGH", 0)
            summary["medium_issues"] += severity_breakdown.get("MEDIUM", 0)
            summary["total_issues"] += analysis.get("total_findings", 0)
    
    # Analyze Config compliance
    if "config_compliance" in components:
        config = components["config_compliance"]
        if config.get("status") == "success":
            analysis = config.get("analysis", {})
            compliance_score = analysis.get("compliance_score", 100)
            
            if compliance_score >= 90:
                summary["compliance_status"] = "Compliant"
            elif compliance_score >= 70:
                summary["compliance_status"] = "Partially Compliant"
            else:
                summary["compliance_status"] = "Non-Compliant"
    
    # Analyze Inspector vulnerabilities
    if "inspector_vulnerabilities" in components:
        inspector = components["inspector_vulnerabilities"]
        if inspector.get("status") == "success":
            analysis = inspector.get("analysis", {})
            severity_breakdown = analysis.get("severity_breakdown", {})
            
            summary["critical_issues"] += severity_breakdown.get("CRITICAL", 0)
            summary["high_issues"] += severity_breakdown.get("HIGH", 0)
            summary["medium_issues"] += severity_breakdown.get("MEDIUM", 0)
            summary["total_issues"] += analysis.get("total_findings", 0)
            
            risk_assessment = analysis.get("risk_assessment", "Unknown")
            if "Critical risk" in risk_assessment:
                summary["vulnerability_status"] = "Critical"
            elif "High risk" in risk_assessment:
                summary["vulnerability_status"] = "High"
            elif "Medium risk" in risk_assessment:
                summary["vulnerability_status"] = "Medium"
            else:
                summary["vulnerability_status"] = "Low"
    
    # Analyze Trusted Advisor recommendations
    if "trusted_advisor" in components:
        trusted_advisor = components["trusted_advisor"]
        if trusted_advisor.get("status") == "success":
            analysis = trusted_advisor.get("analysis", {})
            issues_found = analysis.get("issues_found", 0)
            
            if issues_found == 0:
                summary["recommendation_status"] = "Good"
            elif issues_found < 5:
                summary["recommendation_status"] = "Moderate"
            else:
                summary["recommendation_status"] = "Needs Attention"
    
    # Calculate overall security score
    total_issues = summary["total_issues"]
    critical_issues = summary["critical_issues"]
    high_issues = summary["high_issues"]
    
    if total_issues == 0:
        summary["overall_security_score"] = 100
        summary["risk_level"] = "Low"
    else:
        # Calculate score based on issues
        score = 100 - (critical_issues * 20) - (high_issues * 10) - (summary["medium_issues"] * 5)
        summary["overall_security_score"] = max(0, min(100, score))
        
        if summary["overall_security_score"] >= 80:
            summary["risk_level"] = "Low"
        elif summary["overall_security_score"] >= 60:
            summary["risk_level"] = "Medium"
        elif summary["overall_security_score"] >= 40:
            summary["risk_level"] = "High"
        else:
            summary["risk_level"] = "Critical"
    
    return summary


def _generate_actionable_recommendations(components: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate actionable recommendations from all analysis components"""
    recommendations = []
    
    # Security Hub recommendations
    if "security_hub" in components:
        security_hub = components["security_hub"]
        if security_hub.get("status") == "success":
            analysis = security_hub.get("analysis", {})
            top_threats = analysis.get("top_threats", [])
            
            for threat in top_threats[:3]:  # Top 3 threats
                recommendations.append({
                    "priority": "High",
                    "category": "Security",
                    "action": f"Address {threat['threat']} ({threat['count']} occurrences)",
                    "source": "Security Hub"
                })
    
    # Config compliance recommendations
    if "config_compliance" in components:
        config = components["config_compliance"]
        if config.get("status") == "success":
            analysis = config.get("analysis", {})
            non_compliant_resources = analysis.get("non_compliant_resources", [])
            
            if non_compliant_resources:
                recommendations.append({
                    "priority": "High",
                    "category": "Compliance",
                    "action": f"Fix {len(non_compliant_resources)} non-compliant resources",
                    "source": "Config"
                })
    
    # Inspector vulnerability recommendations
    if "inspector_vulnerabilities" in components:
        inspector = components["inspector_vulnerabilities"]
        if inspector.get("status") == "success":
            analysis = inspector.get("analysis", {})
            risk_assessment = analysis.get("risk_assessment", "")
            
            if "Critical risk" in risk_assessment:
                recommendations.append({
                    "priority": "Critical",
                    "category": "Vulnerabilities",
                    "action": "Immediately patch critical vulnerabilities",
                    "source": "Inspector"
                })
            elif "High risk" in risk_assessment:
                recommendations.append({
                    "priority": "High",
                    "category": "Vulnerabilities",
                    "action": "Prioritize patching high severity vulnerabilities",
                    "source": "Inspector"
                })
    
    # Trusted Advisor recommendations
    if "trusted_advisor" in components:
        trusted_advisor = components["trusted_advisor"]
        if trusted_advisor.get("status") == "success":
            analysis = trusted_advisor.get("analysis", {})
            security_issues = analysis.get("security_issues", [])
            
            for issue in security_issues[:3]:  # Top 3 issues
                recommendations.append({
                    "priority": "Medium",
                    "category": "Best Practices",
                    "action": f"Review {issue['check_name']} - {issue['status']}",
                    "source": "Trusted Advisor"
                })
    
    # Sort by priority
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))
    
    return recommendations


def _generate_executive_report(summary: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate executive summary report"""
    return {
        "title": "AWS Security Executive Summary",
        "overall_security_score": summary.get("overall_security_score", 0),
        "risk_level": summary.get("risk_level", "Unknown"),
        "key_metrics": {
            "total_issues": summary.get("total_issues", 0),
            "critical_issues": summary.get("critical_issues", 0),
            "high_issues": summary.get("high_issues", 0),
            "compliance_status": summary.get("compliance_status", "Unknown")
        },
        "top_recommendations": recommendations[:5],
        "next_steps": [
            "Review critical and high priority recommendations",
            "Implement security fixes based on findings",
            "Schedule regular security reviews",
            "Monitor security posture continuously"
        ]
    }


def _generate_technical_report(components: Dict[str, Any], include_details: bool) -> Dict[str, Any]:
    """Generate technical detailed report"""
    report = {
        "title": "AWS Security Technical Report",
        "components": {}
    }
    
    for component_name, component_data in components.items():
        if component_data.get("status") == "success":
            report["components"][component_name] = {
                "status": "success",
                "data_source": component_data.get("data_source", "Unknown"),
                "summary": component_data.get("analysis", {}),
                "last_updated": component_data.get("last_updated", "Unknown")
            }
            
            if include_details:
                report["components"][component_name]["details"] = component_data
        else:
            report["components"][component_name] = {
                "status": "error",
                "error": component_data.get("error", "Unknown error")
            }
    
    return report


def _generate_comprehensive_report(
    components: Dict[str, Any], 
    summary: Dict[str, Any], 
    recommendations: List[Dict[str, Any]], 
    include_details: bool
) -> Dict[str, Any]:
    """Generate comprehensive report combining all elements"""
    return {
        "title": "AWS Security Comprehensive Report",
        "executive_summary": _generate_executive_report(summary, recommendations),
        "technical_details": _generate_technical_report(components, include_details),
        "action_plan": {
            "immediate_actions": [r for r in recommendations if r["priority"] in ["Critical", "High"]],
            "planned_actions": [r for r in recommendations if r["priority"] in ["Medium", "Low"]],
            "monitoring_recommendations": [
                "Set up CloudWatch alarms for security events",
                "Enable AWS Security Hub continuous monitoring",
                "Schedule regular compliance reviews",
                "Implement automated security scanning"
            ]
        }
    }
