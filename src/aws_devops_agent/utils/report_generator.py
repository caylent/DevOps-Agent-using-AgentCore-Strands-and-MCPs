"""
Report Generation Utility
Handles saving reports to files in the reports folder
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd


class ReportGenerator:
    """Utility class for generating and saving reports to files"""
    
    def __init__(self, reports_dir: str = "reports"):
        """Initialize report generator with reports directory"""
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different report types
        self.subdirs = {
            "cost": self.reports_dir / "cost-analysis",
            "security": self.reports_dir / "security-compliance", 
            "iac": self.reports_dir / "infrastructure-as-code",
            "cdk": self.reports_dir / "cdk-analysis",
            "compliance": self.reports_dir / "compliance-reports",
            "multi-account": self.reports_dir / "multi-account",
            "general": self.reports_dir / "general"
        }
        
        # Create all subdirectories
        for subdir in self.subdirs.values():
            subdir.mkdir(exist_ok=True)
    
    def save_json_report(self, data: Dict[str, Any], filename: str, report_type: str = "general") -> Dict[str, Any]:
        """Save report data as JSON file"""
        try:
            # Get appropriate subdirectory
            subdir = self.subdirs.get(report_type, self.subdirs["general"])
            
            # Generate filename with timestamp if not provided
            if not filename.endswith('.json'):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{filename}_{timestamp}.json"
            
            file_path = subdir / filename
            
            # Add metadata to the data
            data_with_metadata = {
                "report_metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "report_type": report_type,
                    "file_path": str(file_path),
                    "format": "json"
                },
                "report_data": data
            }
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_with_metadata, f, indent=2, ensure_ascii=False)
            
            return {
                "status": "success",
                "file_path": str(file_path),
                "filename": filename,
                "report_type": report_type,
                "message": f"Report saved successfully to {file_path}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to save JSON report: {str(e)}"
            }
    
    def save_markdown_report(self, data: Dict[str, Any], filename: str, report_type: str = "general") -> Dict[str, Any]:
        """Save report data as Markdown file"""
        try:
            # Get appropriate subdirectory
            subdir = self.subdirs.get(report_type, self.subdirs["general"])
            
            # Generate filename with timestamp if not provided
            if not filename.endswith('.md'):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{filename}_{timestamp}.md"
            
            file_path = subdir / filename
            
            # Convert data to markdown
            markdown_content = self._convert_to_markdown(data, report_type)
            
            # Add metadata header
            metadata_header = f"""---
title: {filename.replace('.md', '').replace('_', ' ').title()}
generated_at: {datetime.now().isoformat()}
report_type: {report_type}
file_path: {file_path}
format: markdown
---

"""
            
            full_content = metadata_header + markdown_content
            
            # Save to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            return {
                "status": "success",
                "file_path": str(file_path),
                "filename": filename,
                "report_type": report_type,
                "message": f"Markdown report saved successfully to {file_path}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to save Markdown report: {str(e)}"
            }
    
    def save_csv_report(self, data: List[Dict[str, Any]], filename: str, report_type: str = "general") -> Dict[str, Any]:
        """Save report data as CSV file"""
        try:
            # Get appropriate subdirectory
            subdir = self.subdirs.get(report_type, self.subdirs["general"])
            
            # Generate filename with timestamp if not provided
            if not filename.endswith('.csv'):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{filename}_{timestamp}.csv"
            
            file_path = subdir / filename
            
            # Convert to DataFrame and save
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False, encoding='utf-8')
            
            return {
                "status": "success",
                "file_path": str(file_path),
                "filename": filename,
                "report_type": report_type,
                "message": f"CSV report saved successfully to {file_path}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to save CSV report: {str(e)}"
            }
    
    def save_excel_report(self, data: Dict[str, Any], filename: str, report_type: str = "general") -> Dict[str, Any]:
        """Save report data as Excel file with multiple sheets"""
        try:
            # Get appropriate subdirectory
            subdir = self.subdirs.get(report_type, self.subdirs["general"])
            
            # Generate filename with timestamp if not provided
            if not filename.endswith('.xlsx'):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{filename}_{timestamp}.xlsx"
            
            file_path = subdir / filename
            
            # Create Excel writer
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Save different sections as different sheets
                for sheet_name, sheet_data in data.items():
                    if isinstance(sheet_data, list):
                        df = pd.DataFrame(sheet_data)
                    elif isinstance(sheet_data, dict):
                        df = pd.DataFrame([sheet_data])
                    else:
                        df = pd.DataFrame([{"data": str(sheet_data)}])
                    
                    df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel sheet names max 31 chars
            
            return {
                "status": "success",
                "file_path": str(file_path),
                "filename": filename,
                "report_type": report_type,
                "message": f"Excel report saved successfully to {file_path}"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to save Excel report: {str(e)}"
            }
    
    def _convert_to_markdown(self, data: Dict[str, Any], report_type: str) -> str:
        """Convert data dictionary to markdown format"""
        markdown = []
        
        # Get icons and emojis for report type
        type_icons = self._get_report_type_icons(report_type)
        
        # Add title with icon
        title = report_type.replace('_', ' ').title() + " Report"
        markdown.append(f"# {type_icons['main']} {title}")
        markdown.append("")
        
        # Add header with metadata
        markdown.append(f"**{type_icons['calendar']} Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        markdown.append(f"**{type_icons['type']} Type:** {report_type.replace('_', ' ').title()}")
        markdown.append(f"**{type_icons['status']} Status:** Generated by AWS DevOps Agent")
        markdown.append("")
        
        # Add executive summary if available
        if "executive_summary" in data:
            markdown.append(f"## {type_icons['summary']} Executive Summary")
            markdown.append("")
            exec_summary = data["executive_summary"]
            if isinstance(exec_summary, dict):
                for key, value in exec_summary.items():
                    icon = self._get_metric_icon(key)
                    markdown.append(f"- **{icon} {key.replace('_', ' ').title()}:** {value}")
            else:
                markdown.append(str(exec_summary))
            markdown.append("")
        
        # Process different sections
        for key, value in data.items():
            if key == "status" or key == "executive_summary":
                continue
                
            # Get section icon
            section_icon = self._get_section_icon(key)
            section_title = key.replace('_', ' ').title()
            markdown.append(f"## {section_icon} {section_title}")
            markdown.append("")
            
            if isinstance(value, dict):
                # Handle dictionary sections
                for sub_key, sub_value in value.items():
                    sub_icon = self._get_metric_icon(sub_key)
                    sub_title = sub_key.replace('_', ' ').title()
                    markdown.append(f"### {sub_icon} {sub_title}")
                    markdown.append("")
                    
                    if isinstance(sub_value, list):
                        for i, item in enumerate(sub_value, 1):
                            if isinstance(item, dict):
                                markdown.append(f"#### {i}. {self._get_metric_icon('item')} Item {i}")
                                for item_key, item_value in item.items():
                                    item_icon = self._get_metric_icon(item_key)
                                    markdown.append(f"- **{item_icon} {item_key.replace('_', ' ').title()}:** {item_value}")
                            else:
                                markdown.append(f"- {self._get_metric_icon('item')} {item}")
                    elif isinstance(sub_value, str):
                        markdown.append(sub_value)
                    else:
                        markdown.append(str(sub_value))
                    markdown.append("")
                    
            elif isinstance(value, list):
                # Handle list sections
                for i, item in enumerate(value, 1):
                    if isinstance(item, dict):
                        markdown.append(f"#### {i}. {self._get_metric_icon('item')} Item {i}")
                        for item_key, item_value in item.items():
                            item_icon = self._get_metric_icon(item_key)
                            markdown.append(f"- **{item_icon} {item_key.replace('_', ' ').title()}:** {item_value}")
                    else:
                        markdown.append(f"- {self._get_metric_icon('item')} {item}")
                markdown.append("")
            else:
                # Handle simple values
                markdown.append(str(value))
                markdown.append("")
        
        return "\n".join(markdown)
    
    def _get_report_type_icons(self, report_type: str) -> Dict[str, str]:
        """Get icons for different report types"""
        icon_sets = {
            "cost": {
                "main": "💰",
                "calendar": "📅",
                "type": "🏷️",
                "status": "✅",
                "summary": "📊",
                "analysis": "🔍",
                "recommendations": "💡",
                "findings": "🔎",
                "next_steps": "🚀"
            },
            "security": {
                "main": "🔒",
                "calendar": "📅",
                "type": "🏷️",
                "status": "✅",
                "summary": "📊",
                "analysis": "🔍",
                "recommendations": "💡",
                "findings": "🔎",
                "next_steps": "🚀"
            },
            "iac": {
                "main": "🏗️",
                "calendar": "📅",
                "type": "🏷️",
                "status": "✅",
                "summary": "📊",
                "analysis": "🔍",
                "recommendations": "💡",
                "findings": "🔎",
                "next_steps": "🚀"
            },
            "cdk": {
                "main": "⚡",
                "calendar": "📅",
                "type": "🏷️",
                "status": "✅",
                "summary": "📊",
                "analysis": "🔍",
                "recommendations": "💡",
                "findings": "🔎",
                "next_steps": "🚀"
            },
            "compliance": {
                "main": "📋",
                "calendar": "📅",
                "type": "🏷️",
                "status": "✅",
                "summary": "📊",
                "analysis": "🔍",
                "recommendations": "💡",
                "findings": "🔎",
                "next_steps": "🚀"
            },
            "multi-account": {
                "main": "🌐",
                "calendar": "📅",
                "type": "🏷️",
                "status": "✅",
                "summary": "📊",
                "analysis": "🔍",
                "recommendations": "💡",
                "findings": "🔎",
                "next_steps": "🚀"
            },
            "general": {
                "main": "📄",
                "calendar": "📅",
                "type": "🏷️",
                "status": "✅",
                "summary": "📊",
                "analysis": "🔍",
                "recommendations": "💡",
                "findings": "🔎",
                "next_steps": "🚀"
            }
        }
        
        return icon_sets.get(report_type, icon_sets["general"])
    
    def _get_metric_icon(self, metric_name: str) -> str:
        """Get appropriate icon for metric names"""
        metric_icons = {
            "cost": "💰",
            "savings": "💵",
            "total": "📊",
            "monthly": "📅",
            "potential": "🎯",
            "optimization": "⚡",
            "opportunities": "🔍",
            "recommendations": "💡",
            "findings": "🔎",
            "issues": "⚠️",
            "critical": "🚨",
            "high": "🔴",
            "medium": "🟡",
            "low": "🟢",
            "score": "📈",
            "compliance": "✅",
            "security": "🔒",
            "resources": "🏗️",
            "instances": "💻",
            "storage": "💾",
            "network": "🌐",
            "database": "🗄️",
            "performance": "⚡",
            "availability": "🔄",
            "reliability": "🛡️",
            "scalability": "📈",
            "efficiency": "🎯",
            "utilization": "📊",
            "capacity": "📦",
            "throughput": "🚀",
            "latency": "⏱️",
            "errors": "❌",
            "success": "✅",
            "failure": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "status": "📊",
            "health": "💚",
            "unhealthy": "❤️",
            "degraded": "🟡",
            "unknown": "❓"
        }
        
        metric_lower = metric_name.lower()
        for key, icon in metric_icons.items():
            if key in metric_lower:
                return icon
        
        return "📊"  # Default icon
    
    def _get_section_icon(self, section_name: str) -> str:
        """Get appropriate icon for section names"""
        section_icons = {
            "analysis": "🔍",
            "findings": "🔎",
            "recommendations": "💡",
            "next_steps": "🚀",
            "summary": "📊",
            "details": "📋",
            "breakdown": "📊",
            "trends": "📈",
            "forecast": "🔮",
            "optimization": "⚡",
            "security": "🔒",
            "compliance": "📋",
            "cost": "💰",
            "performance": "⚡",
            "architecture": "🏗️",
            "implementation": "🛠️",
            "roadmap": "🗺️",
            "plan": "📋",
            "strategy": "🎯",
            "tactics": "⚔️",
            "metrics": "📊",
            "kpis": "📈",
            "goals": "🎯",
            "objectives": "🎯",
            "results": "📊",
            "outcomes": "🎯",
            "impact": "💥",
            "benefits": "✨",
            "risks": "⚠️",
            "challenges": "🚧",
            "opportunities": "🔍",
            "improvements": "⬆️",
            "enhancements": "✨",
            "upgrades": "⬆️",
            "migrations": "🔄",
            "deployments": "🚀",
            "releases": "🎉",
            "versions": "🏷️",
            "updates": "🔄",
            "patches": "🔧",
            "fixes": "🔧",
            "bugs": "🐛",
            "features": "✨",
            "capabilities": "⚡",
            "functionality": "🛠️",
            "services": "🔧",
            "tools": "🛠️",
            "technologies": "⚙️",
            "frameworks": "🏗️",
            "platforms": "🏢",
            "environments": "🌍",
            "configurations": "⚙️",
            "settings": "⚙️",
            "parameters": "📝",
            "variables": "📝",
            "constants": "📌",
            "definitions": "📖",
            "glossary": "📚",
            "references": "📖",
            "links": "🔗",
            "resources": "📚",
            "documentation": "📖",
            "guides": "📖",
            "tutorials": "🎓",
            "examples": "💡",
            "samples": "🧪",
            "templates": "📋",
            "patterns": "🔧",
            "best_practices": "⭐",
            "standards": "📏",
            "guidelines": "📋",
            "policies": "📜",
            "procedures": "📋",
            "processes": "🔄",
            "workflows": "🔄",
            "pipelines": "🔧",
            "automation": "🤖",
            "integration": "🔗",
            "connectivity": "🌐",
            "communication": "💬",
            "collaboration": "🤝",
            "coordination": "🎯",
            "management": "👥",
            "governance": "👑",
            "oversight": "👁️",
            "monitoring": "👁️",
            "tracking": "📍",
            "logging": "📝",
            "auditing": "🔍",
            "reporting": "📊",
            "analytics": "📈",
            "insights": "💡",
            "intelligence": "🧠",
            "data": "📊",
            "information": "ℹ️",
            "knowledge": "🧠",
            "wisdom": "🧙",
            "expertise": "🎓",
            "experience": "⭐",
            "skills": "⚡",
            "abilities": "💪",
            "capabilities": "⚡",
            "competencies": "🎯",
            "proficiencies": "⭐",
            "qualifications": "🏆",
            "certifications": "🏅",
            "credentials": "🎫",
            "accreditations": "🏆",
            "validations": "✅",
            "verifications": "✅",
            "confirmations": "✅",
            "approvals": "✅",
            "authorizations": "🔐",
            "permissions": "🔑",
            "access": "🚪",
            "privileges": "👑",
            "rights": "⚖️",
            "entitlements": "🎫",
            "benefits": "✨",
            "advantages": "⬆️",
            "strengths": "💪",
            "weaknesses": "⚠️",
            "limitations": "🚧",
            "constraints": "🔒",
            "restrictions": "🚫",
            "barriers": "🚧",
            "obstacles": "🚧",
            "challenges": "🚧",
            "problems": "❌",
            "issues": "⚠️",
            "concerns": "😟",
            "risks": "⚠️",
            "threats": "⚠️",
            "vulnerabilities": "🔓",
            "exposures": "👁️",
            "gaps": "🕳️",
            "deficiencies": "❌",
            "shortcomings": "⚠️",
            "failures": "❌",
            "errors": "❌",
            "mistakes": "❌",
            "bugs": "🐛",
            "defects": "❌",
            "flaws": "❌",
            "imperfections": "⚠️",
            "inconsistencies": "⚠️",
            "discrepancies": "⚠️",
            "conflicts": "⚔️",
            "contradictions": "⚠️",
            "ambiguities": "❓",
            "uncertainties": "❓",
            "doubts": "❓",
            "questions": "❓",
            "inquiries": "❓",
            "requests": "🙏",
            "demands": "📢",
            "requirements": "📋",
            "specifications": "📝",
            "criteria": "📏",
            "standards": "📏",
            "benchmarks": "📊",
            "baselines": "📏",
            "thresholds": "📏",
            "limits": "🚧",
            "boundaries": "🚧",
            "scope": "🎯",
            "coverage": "📊",
            "reach": "🌐",
            "extent": "📏",
            "range": "📊",
            "span": "📏",
            "duration": "⏱️",
            "timeline": "📅",
            "schedule": "📅",
            "calendar": "📅",
            "agenda": "📋",
            "plan": "📋",
            "strategy": "🎯",
            "approach": "🛤️",
            "method": "🔧",
            "technique": "🔧",
            "procedure": "📋",
            "process": "🔄",
            "workflow": "🔄",
            "pipeline": "🔧",
            "pipeline": "🔧",
            "pipeline": "🔧"
        }
        
        section_lower = section_name.lower()
        for key, icon in section_icons.items():
            if key in section_lower:
                return icon
        
        return "📋"  # Default icon
    
    def list_reports(self, report_type: str = None) -> Dict[str, Any]:
        """List all available reports"""
        try:
            reports = []
            
            if report_type:
                # List reports for specific type
                subdir = self.subdirs.get(report_type, self.subdirs["general"])
                if subdir.exists():
                    for file_path in subdir.glob("*"):
                        if file_path.is_file():
                            reports.append({
                                "filename": file_path.name,
                                "file_path": str(file_path),
                                "report_type": report_type,
                                "size_bytes": file_path.stat().st_size,
                                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                            })
            else:
                # List all reports
                for report_type, subdir in self.subdirs.items():
                    if subdir.exists():
                        for file_path in subdir.glob("*"):
                            if file_path.is_file():
                                reports.append({
                                    "filename": file_path.name,
                                    "file_path": str(file_path),
                                    "report_type": report_type,
                                    "size_bytes": file_path.stat().st_size,
                                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                                })
            
            return {
                "status": "success",
                "reports": reports,
                "total_reports": len(reports),
                "reports_dir": str(self.reports_dir)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to list reports: {str(e)}"
            }
    
    def get_report_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a specific report file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return {
                    "status": "error",
                    "error": f"Report file not found: {file_path}"
                }
            
            stat = path.stat()
            return {
                "status": "success",
                "filename": path.name,
                "file_path": str(path),
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to get report info: {str(e)}"
            }


# Global report generator instance
_report_generator = None

def get_report_generator() -> ReportGenerator:
    """Get the global report generator instance"""
    global _report_generator
    if _report_generator is None:
        _report_generator = ReportGenerator()
    return _report_generator
