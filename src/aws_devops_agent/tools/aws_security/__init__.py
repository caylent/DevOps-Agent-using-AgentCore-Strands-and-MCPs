"""
AWS Security Analysis Tools
Real security analysis using AWS native APIs (Security Hub, Config, Inspector, Trusted Advisor)
"""

from .security_hub_analysis import *
from .config_compliance import *
from .inspector_analysis import *
from .trusted_advisor import *
from .comprehensive_analysis import *

__all__ = [
    # Security Hub Analysis
    "analyze_security_hub_findings",
    "get_security_insights",
    "analyze_security_posture",
    
    # Config Compliance
    "analyze_config_compliance",
    "get_compliance_details",
    "check_resource_compliance",
    
    # Inspector Analysis
    "analyze_inspector_findings",
    "get_vulnerability_assessment",
    "check_security_vulnerabilities",
    
    # Trusted Advisor
    "get_trusted_advisor_checks",
    "analyze_trusted_advisor_recommendations",
    "get_security_recommendations",
    
    # Combined Analysis
    "perform_comprehensive_security_analysis",
    "generate_security_report"
]
