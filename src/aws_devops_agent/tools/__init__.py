"""AWS DevOps Tools - Organized by domain"""

# Import all tools for easy access
from .aws_pricing import *
from .aws_cost import *
from .aws_iac import *
from .aws_cdk import *
from .aws_terraform import *
from .aws_compliance import *
from .github import *
from .reporting import *

__all__ = [
    # Pricing tools (AWS Pricing API)
    "get_real_aws_pricing",
    "calculate_reserved_instance_savings", 
    "get_service_pricing_overview",
    "generate_cost_comparison_report",
    "compare_instance_types",
    "compare_pricing_models",
    "compare_regions_pricing",
    "analyze_price_optimization_opportunities",
    "suggest_cost_effective_alternatives",
    "calculate_savings_potential",
    "optimize_terraform_plan_costs",
    
    # Cost tools (AWS Cost Explorer)
    "get_actual_aws_costs",
    "get_cost_by_service",
    "get_cost_trends",
    "get_rightsizing_recommendations", 
    "get_reserved_instance_recommendations",
    "analyze_cost_anomalies",
    "analyze_usage_based_optimization",
    "get_underutilized_resources",
    "calculate_wasted_spend",
    "generate_cost_optimization_report",
    "analyze_resource_costs",
    "get_unused_resources",
    "calculate_resource_utilization",
    "get_organization_costs",
    "analyze_account_costs",
    "generate_multi_account_report",
    
    # IaC tools
    "analyze_terraform_configuration",
    "validate_cloudformation_template",
    "scan_infrastructure_drift",
    "generate_iac_best_practices_report",
    
    # CDK tools
    "analyze_cdk_project",
    "synthesize_cdk_project",
    "analyze_cdk_synthesized_output",
    "generate_cdk_optimization_report",
    
    # Terraform tools
    "analyze_terraform_project",
    "validate_terraform_configuration",
    "plan_terraform_changes",
    "analyze_terraform_state",
    "generate_terraform_optimization_report",
    
    # Compliance tools
    "validate_security_policies",
    "check_compliance_standards",
    "generate_compliance_report",
    "scan_security_vulnerabilities",
    
    # GitHub tools
    "create_optimization_pull_request",
    "update_iac_via_github",
    "list_infrastructure_repositories",
    "monitor_infrastructure_prs",
    
    # Reporting tools
    "generate_document",
    "generate_cost_analysis_document",
    "generate_security_compliance_document", 
    "generate_infrastructure_document",
    "generate_cdk_analysis_document",
    "generate_terraform_analysis_document",
    "list_generated_documents",
    "get_document_info"
]
