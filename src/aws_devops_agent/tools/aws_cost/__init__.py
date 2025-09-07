"""
AWS Cost Management Tools - Real AWS Data Access via MCP Client
Access to actual AWS Cost Explorer data using MCP servers

This module provides comprehensive cost analysis capabilities including:
- Real-time cost data retrieval via AWS Cost Explorer MCP Server  
- Usage-based optimization recommendations from actual utilization data
- Multi-account cost analysis and reporting
- Integration with AWS Cost Anomaly Detection
"""

from .explorer import (
    get_actual_aws_costs,
    get_cost_by_service,
    get_cost_trends,
    get_rightsizing_recommendations,
    get_reserved_instance_recommendations,
    analyze_cost_anomalies
)

from .optimization import (
    analyze_usage_based_optimization,
    get_underutilized_resources,
    calculate_wasted_spend,
    generate_cost_optimization_report
)

from .resources import (
    scan_live_aws_resources,
    analyze_unused_resources,
    get_resource_utilization_metrics,
    discover_cross_account_resources,
    analyze_resource_costs,
    get_unused_resources,
    calculate_resource_utilization
)

from .multi_account import (
    get_organization_costs,
    analyze_account_costs,
    generate_multi_account_report
)

__all__ = [
    'get_actual_aws_costs',
    'get_cost_by_service', 
    'get_cost_trends',
    'get_rightsizing_recommendations',
    'get_reserved_instance_recommendations',
    'analyze_cost_anomalies',
    'analyze_usage_based_optimization',
    'get_underutilized_resources',
    'calculate_wasted_spend',
    'generate_cost_optimization_report',
    'scan_live_aws_resources',
    'analyze_unused_resources',
    'get_resource_utilization_metrics',
    'discover_cross_account_resources',
    'analyze_resource_costs',
    'get_unused_resources',
    'calculate_resource_utilization',
    'get_organization_costs',
    'analyze_account_costs',
    'generate_multi_account_report'
]
