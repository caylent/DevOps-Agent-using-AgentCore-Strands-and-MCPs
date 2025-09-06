"""
Document Generation Tools
Generate and save various types of reports and documents
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from strands import tool

from ...utils.report_generator import get_report_generator


@tool
def generate_document(
    content: str,
    title: str,
    document_type: str = "general",
    format: str = "markdown",
    filename: str = None
) -> Dict[str, Any]:
    """
    Generate and save a document to the reports folder
    
    Args:
        content: Document content (can be text, JSON data, or structured data)
        title: Document title
        document_type: Type of document (general, cost, security, iac, cdk, compliance, multi-account)
        format: Output format (markdown, json, csv, excel)
        filename: Custom filename (auto-generated if None)
    
    Returns:
        Dict containing document generation results and file path
    """
    try:
        # Get report generator
        report_gen = get_report_generator()
        
        # Generate filename if not provided
        if not filename:
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_').lower()
            filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prepare data structure
        if isinstance(content, str):
            # If content is a string, wrap it in a structure
            data = {
                "title": title,
                "content": content,
                "generated_at": datetime.now().isoformat(),
                "document_type": document_type
            }
        else:
            # If content is already structured, use it directly
            data = content
        
        # Save based on format
        if format.lower() == "markdown":
            result = report_gen.save_markdown_report(data, filename, document_type)
        elif format.lower() == "json":
            result = report_gen.save_json_report(data, filename, document_type)
        elif format.lower() == "csv" and isinstance(content, list):
            result = report_gen.save_csv_report(content, filename, document_type)
        elif format.lower() == "excel":
            result = report_gen.save_excel_report(data, filename, document_type)
        else:
            return {
                "status": "error",
                "error": f"Unsupported format: {format}. Supported formats: markdown, json, csv, excel"
            }
        
        if result["status"] == "success":
            result["document_info"] = {
                "title": title,
                "document_type": document_type,
                "format": format,
                "generated_at": datetime.now().isoformat()
            }
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Document generation failed: {str(e)}"
        }


@tool
def generate_cost_analysis_document(
    cost_data: Dict[str, Any],
    title: str = "Cost Analysis Report",
    filename: str = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive cost analysis document
    
    Args:
        cost_data: Cost analysis data from cost tools
        title: Document title
        filename: Custom filename (auto-generated if None)
    
    Returns:
        Dict containing document generation results
    """
    try:
        # Prepare comprehensive cost analysis document
        document_content = {
            "executive_summary": {
                "total_monthly_cost": f"${cost_data.get('total_monthly_cost', 0):,.2f}",
                "potential_savings": f"${cost_data.get('potential_savings', 0):,.2f}",
                "savings_percentage": f"{(cost_data.get('potential_savings', 0) / max(cost_data.get('total_monthly_cost', 1), 1)) * 100:.1f}%",
                "optimization_opportunities": len(cost_data.get("optimization_opportunities", [])),
                "recommendations_count": len(cost_data.get("recommendations", [])),
                "analysis_period": "Last 30 days",
                "report_confidence": "High (Real AWS data via MCP servers)"
            },
            "cost_breakdown": {
                "by_service": cost_data.get("cost_breakdown", {}).get("by_service", {}),
                "by_region": cost_data.get("cost_breakdown", {}).get("by_region", {}),
                "by_account": cost_data.get("cost_breakdown", {}).get("by_account", {}),
                "monthly_trend": cost_data.get("cost_breakdown", {}).get("monthly_trend", [])
            },
            "optimization_opportunities": cost_data.get("optimization_opportunities", []),
            "recommendations": {
                "immediate_actions": [r for r in cost_data.get("recommendations", []) if r.get("priority") == "high"],
                "medium_term": [r for r in cost_data.get("recommendations", []) if r.get("priority") == "medium"],
                "long_term": [r for r in cost_data.get("recommendations", []) if r.get("priority") == "low"]
            },
            "resource_analysis": {
                "underutilized_resources": cost_data.get("resource_analysis", {}).get("underutilized", []),
                "overprovisioned_resources": cost_data.get("resource_analysis", {}).get("overprovisioned", []),
                "unused_resources": cost_data.get("resource_analysis", {}).get("unused", []),
                "rightsizing_opportunities": cost_data.get("resource_analysis", {}).get("rightsizing", [])
            },
            "trend_analysis": {
                "cost_trends": cost_data.get("trend_analysis", {}).get("cost_trends", []),
                "usage_patterns": cost_data.get("trend_analysis", {}).get("usage_patterns", []),
                "seasonal_variations": cost_data.get("trend_analysis", {}).get("seasonal", []),
                "forecast": cost_data.get("trend_analysis", {}).get("forecast", {})
            },
            "implementation_roadmap": {
                "phase_1_immediate": ["Review and implement high-priority recommendations", "Set up cost monitoring alerts"],
                "phase_2_short_term": ["Implement rightsizing recommendations", "Set up automated scaling policies"],
                "phase_3_long_term": ["Implement reserved instances", "Optimize data transfer costs"]
            },
            "next_steps": cost_data.get("next_steps", [
                "Review this report with your team",
                "Implement immediate cost optimization recommendations",
                "Set up regular cost monitoring and reporting",
                "Schedule follow-up analysis in 30 days"
            ])
        }
        
        return generate_document(
            content=document_content,
            title=title,
            document_type="cost",
            format="markdown",
            filename=filename
        )
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Cost analysis document generation failed: {str(e)}"
        }


@tool
def generate_security_compliance_document(
    security_data: Dict[str, Any],
    title: str = "Security Compliance Report",
    filename: str = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive security compliance document
    
    Args:
        security_data: Security analysis data from security tools
        title: Document title
        filename: Custom filename (auto-generated if None)
    
    Returns:
        Dict containing document generation results
    """
    try:
        # Prepare comprehensive security compliance document
        findings = security_data.get("findings", [])
        critical_issues = [f for f in findings if f.get("severity") == "critical"]
        high_issues = [f for f in findings if f.get("severity") == "high"]
        medium_issues = [f for f in findings if f.get("severity") == "medium"]
        low_issues = [f for f in findings if f.get("severity") == "low"]
        
        document_content = {
            "executive_summary": {
                "compliance_score": f"{security_data.get('compliance_score', 0)}%",
                "compliance_level": "High" if security_data.get("compliance_score", 0) >= 80 else "Medium" if security_data.get("compliance_score", 0) >= 60 else "Low",
                "total_findings": security_data.get("total_findings", 0),
                "critical_issues": len(critical_issues),
                "high_issues": len(high_issues),
                "medium_issues": len(medium_issues),
                "low_issues": len(low_issues),
                "assessment_date": datetime.now().strftime('%Y-%m-%d'),
                "report_confidence": "High (Real AWS security data via MCP servers)"
            },
            "compliance_status": {
                "overall_status": security_data.get("compliance_status", {}).get("overall", "Unknown"),
                "framework_compliance": security_data.get("compliance_status", {}).get("frameworks", {}),
                "control_coverage": security_data.get("compliance_status", {}).get("controls", {}),
                "last_assessment": security_data.get("compliance_status", {}).get("last_assessment", "Not available")
            },
            "security_findings": {
                "critical_findings": critical_issues,
                "high_priority_findings": high_issues,
                "medium_priority_findings": medium_issues,
                "low_priority_findings": low_issues,
                "summary_by_category": {
                    "access_control": len([f for f in findings if "access" in f.get("category", "").lower()]),
                    "encryption": len([f for f in findings if "encryption" in f.get("category", "").lower()]),
                    "network_security": len([f for f in findings if "network" in f.get("category", "").lower()]),
                    "data_protection": len([f for f in findings if "data" in f.get("category", "").lower()]),
                    "monitoring": len([f for f in findings if "monitoring" in f.get("category", "").lower()])
                }
            },
            "recommendations": {
                "immediate_actions": [r for r in security_data.get("recommendations", []) if r.get("priority") == "critical"],
                "high_priority": [r for r in security_data.get("recommendations", []) if r.get("priority") == "high"],
                "medium_priority": [r for r in security_data.get("recommendations", []) if r.get("priority") == "medium"],
                "low_priority": [r for r in security_data.get("recommendations", []) if r.get("priority") == "low"]
            },
            "remediation_plan": {
                "immediate_remediation": security_data.get("remediation_plan", {}).get("immediate", []),
                "short_term_remediation": security_data.get("remediation_plan", {}).get("short_term", []),
                "long_term_remediation": security_data.get("remediation_plan", {}).get("long_term", []),
                "estimated_effort": security_data.get("remediation_plan", {}).get("effort_estimate", "To be determined"),
                "required_resources": security_data.get("remediation_plan", {}).get("resources", [])
            },
            "security_metrics": {
                "vulnerability_score": security_data.get("vulnerability_score", 0),
                "threat_level": security_data.get("threat_level", "Unknown"),
                "risk_score": security_data.get("risk_score", 0),
                "security_posture": security_data.get("security_posture", "Unknown")
            },
            "implementation_roadmap": {
                "phase_1_critical": ["Address all critical security findings", "Implement immediate access controls"],
                "phase_2_high_priority": ["Resolve high-priority security issues", "Enhance monitoring and logging"],
                "phase_3_ongoing": ["Implement continuous security monitoring", "Regular security assessments"]
            },
            "next_steps": security_data.get("next_steps", [
                "Review critical security findings immediately",
                "Implement immediate remediation actions",
                "Schedule security team review meeting",
                "Set up continuous security monitoring",
                "Plan regular security assessments"
            ])
        }
        
        return generate_document(
            content=document_content,
            title=title,
            document_type="security",
            format="markdown",
            filename=filename
        )
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Security compliance document generation failed: {str(e)}"
        }


@tool
def generate_infrastructure_document(
    iac_data: Dict[str, Any],
    title: str = "Infrastructure Analysis Report",
    filename: str = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive infrastructure analysis document
    
    Args:
        iac_data: Infrastructure analysis data from IaC tools
        title: Document title
        filename: Custom filename (auto-generated if None)
    
    Returns:
        Dict containing document generation results
    """
    try:
        # Prepare structured infrastructure document
        document_content = {
            "executive_summary": {
                "total_resources": iac_data.get("total_resources", 0),
                "compliance_score": iac_data.get("compliance_score", 0),
                "best_practices_violations": len(iac_data.get("best_practices_violations", [])),
                "security_issues": len(iac_data.get("security_issues", []))
            },
            "infrastructure_analysis": iac_data.get("analysis", {}),
            "best_practices": iac_data.get("best_practices_analysis", {}),
            "security_findings": iac_data.get("security_issues", []),
            "recommendations": iac_data.get("recommendations", []),
            "improvement_plan": iac_data.get("improvement_recommendations", [])
        }
        
        return generate_document(
            content=document_content,
            title=title,
            document_type="iac",
            format="markdown",
            filename=filename
        )
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Infrastructure document generation failed: {str(e)}"
        }


@tool
def generate_cdk_analysis_document(
    cdk_data: Dict[str, Any],
    title: str = "CDK Analysis Report",
    filename: str = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive CDK analysis document
    
    Args:
        cdk_data: CDK analysis data from CDK tools
        title: Document title
        filename: Custom filename (auto-generated if None)
    
    Returns:
        Dict containing document generation results
    """
    try:
        # Prepare structured CDK analysis document
        document_content = {
            "executive_summary": cdk_data.get("executive_summary", {}),
            "project_analysis": cdk_data.get("project_info", {}),
            "cost_optimization": cdk_data.get("cost_optimization", {}),
            "security_recommendations": cdk_data.get("security_recommendations", {}),
            "architecture_improvements": cdk_data.get("architecture_improvements", {}),
            "implementation_roadmap": cdk_data.get("implementation_roadmap", []),
            "findings": cdk_data.get("findings", []),
            "recommendations": cdk_data.get("recommendations", [])
        }
        
        return generate_document(
            content=document_content,
            title=title,
            document_type="cdk",
            format="markdown",
            filename=filename
        )
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"CDK analysis document generation failed: {str(e)}"
        }


@tool
def list_generated_documents(
    document_type: str = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    List all generated documents in the reports folder
    
    Args:
        document_type: Filter by document type (optional)
        limit: Maximum number of documents to return
    
    Returns:
        Dict containing list of generated documents
    """
    try:
        report_gen = get_report_generator()
        result = report_gen.list_reports(document_type)
        
        if result["status"] == "success":
            # Sort by modification time (newest first)
            reports = sorted(result["reports"], key=lambda x: x["modified"], reverse=True)
            
            # Apply limit
            if limit > 0:
                reports = reports[:limit]
            
            result["reports"] = reports
            result["showing"] = len(reports)
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to list documents: {str(e)}"
        }


@tool
def get_document_info(file_path: str) -> Dict[str, Any]:
    """
    Get information about a specific document
    
    Args:
        file_path: Path to the document file
    
    Returns:
        Dict containing document information
    """
    try:
        report_gen = get_report_generator()
        return report_gen.get_report_info(file_path)
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to get document info: {str(e)}"
        }
