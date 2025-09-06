"""AWS Cost Optimization Tools"""

from .pricing import (
    get_real_aws_pricing,
    analyze_cost_optimization_opportunities,
    generate_cost_comparison_report,
    calculate_reserved_instance_savings
)
from .optimization import (
    get_actual_aws_costs,
    analyze_cost_trends_real,
    get_multi_account_cost_breakdown,
    get_rightsizing_recommendations,
    get_reserved_instance_recommendations,
    get_cost_forecast_mcp,
    compare_cost_periods_mcp
)
from .resources import (
    scan_live_aws_resources,
    analyze_unused_resources,
    get_resource_utilization_metrics,
    discover_cross_account_resources
)
from .multi_account import (
    list_cross_account_resources,
    execute_cross_account_operation,
    generate_multi_account_report,
    monitor_cross_account_compliance
)

__all__ = [
    # Pricing tools
    "get_real_aws_pricing",
    "analyze_cost_optimization_opportunities", 
    "generate_cost_comparison_report",
    "calculate_reserved_instance_savings",
    
    # Optimization tools
    "get_actual_aws_costs",
    "analyze_cost_trends_real",
    "get_multi_account_cost_breakdown",
    "get_rightsizing_recommendations",
    "get_reserved_instance_recommendations", 
    "get_cost_forecast_mcp",
    "compare_cost_periods_mcp",
    
    # Resource tools
    "scan_live_aws_resources",
    "analyze_unused_resources",
    "get_resource_utilization_metrics",
    "discover_cross_account_resources",
    
    # Multi-account tools
    "list_cross_account_resources",
    "execute_cross_account_operation",
    "generate_multi_account_report",
    "monitor_cross_account_compliance"
]
