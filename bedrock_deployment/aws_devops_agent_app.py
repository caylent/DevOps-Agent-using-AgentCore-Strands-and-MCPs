#!/usr/bin/env python3
"""
AWS DevOps Agent using Strands + Bedrock Agent Core
Production-ready agent for cost optimization, IaC analysis, and compliance validation
"""

import sys
import os
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "config"))
sys.path.append(str(project_root / "tools" / "aws-devops"))

from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Import our AWS DevOps tools
from aws_cost_tools import (
    get_real_aws_pricing,
    analyze_cost_optimization_opportunities,
    generate_cost_comparison_report,
    calculate_reserved_instance_savings,
)
from aws_iac_tools import (
    analyze_terraform_configuration,
    validate_cloudformation_template,
    scan_infrastructure_drift,
    generate_iac_best_practices_report,
)
from aws_compliance_tools import (
    validate_security_policies,
    check_compliance_standards,
    generate_compliance_report,
    scan_security_vulnerabilities,
)
from aws_multi_account_tools import (
    list_cross_account_resources,
    execute_cross_account_operation,
    generate_multi_account_report,
)
from github_integration_tools import (
    create_optimization_pull_request,
    update_iac_via_github,
    list_infrastructure_repositories,
)

try:
    from config.app_config import get_config
    config = get_config()
    model_id = config.model.model_id
except ImportError:
    # Fallback for testing - using inference profile
    model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

# Create the Strands agent
agent = Agent(
    model=model_id,
    tools=[
        # Cost Optimization Tools
        get_real_aws_pricing,
        analyze_cost_optimization_opportunities,
        generate_cost_comparison_report,
        calculate_reserved_instance_savings,
        
        # Infrastructure as Code Tools
        analyze_terraform_configuration,
        validate_cloudformation_template,
        scan_infrastructure_drift,
        generate_iac_best_practices_report,
        
        # Compliance and Security Tools
        validate_security_policies,
        check_compliance_standards,
        generate_compliance_report,
        scan_security_vulnerabilities,
        
        # Multi-Account Management Tools
        list_cross_account_resources,
        execute_cross_account_operation,
        generate_multi_account_report,
        
        # GitHub Integration Tools
        create_optimization_pull_request,
        update_iac_via_github,
        list_infrastructure_repositories,
    ],
    system_prompt="""You are an AWS DevOps Agent specialist deployed on Bedrock Agent Core with access to real AWS APIs via MCP servers.

Your core capabilities:
- Real-time AWS cost analysis and optimization recommendations
- Infrastructure as Code (IaC) analysis for Terraform and CloudFormation
- Security compliance validation and reporting
- Multi-account and multi-region operations
- Automated Pull Request generation for infrastructure improvements

WORKFLOW FOR COST OPTIMIZATION:
1. Use get_real_aws_pricing to fetch current AWS pricing data
2. Use analyze_cost_optimization_opportunities to identify savings
3. Use calculate_reserved_instance_savings for RI recommendations
4. Use generate_cost_comparison_report for comprehensive analysis
5. Use create_optimization_pull_request to propose infrastructure changes

WORKFLOW FOR IAC ANALYSIS:
1. Use analyze_terraform_configuration for Terraform analysis
2. Use validate_cloudformation_template for CloudFormation analysis
3. Use scan_infrastructure_drift to detect configuration drift
4. Use generate_iac_best_practices_report for recommendations
5. Use update_iac_via_github to implement fixes via PR

WORKFLOW FOR COMPLIANCE:
1. Use validate_security_policies to check security configurations
2. Use check_compliance_standards for industry standards (SOC2, HIPAA, etc.)
3. Use scan_security_vulnerabilities for security issues
4. Use generate_compliance_report for comprehensive compliance status

MULTI-ACCOUNT OPERATIONS:
1. Use list_cross_account_resources to view resources across accounts
2. Use execute_cross_account_operation for cross-account actions
3. Use generate_multi_account_report for organization-wide analysis

DATA SOURCE TRANSPARENCY:
- Always specify that data comes from real AWS APIs via MCP servers
- Include current pricing, real cost data, and live infrastructure state
- Provide specific, actionable recommendations with cost implications
- Generate automated PRs for infrastructure improvements

RESPONSE FORMAT:
- Provide clear, executive-summary style reports
- Include cost savings opportunities with dollar amounts
- Show before/after comparisons for optimizations
- Generate actionable next steps with PR links when applicable

You integrate with real AWS services and provide production-ready DevOps automation.""",
    name="AWS DevOps Agent",
    description="Production AWS DevOps agent for cost optimization, IaC analysis, compliance validation, and automated infrastructure improvements",
)

# Create the Bedrock Agent Core app
app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    """Process user input and return a response"""
    print(f"📥 Received AWS DevOps payload: {payload}")

    # Extract user message
    user_message = payload.get("prompt", "")
    if not user_message:
        user_message = payload.get("inputText", "")
    if not user_message:
        user_message = payload.get("query", "Analyze AWS infrastructure and provide optimization recommendations")

    print(f"💬 AWS DevOps query: {user_message}")

    try:
        # Process with Strands agent
        response = agent(user_message)
        print(f"🤖 AWS DevOps Agent response: {response}")

        # Return JSON serializable response
        if isinstance(response, str):
            return {
                "response": response,
                "status": "success",
                "agent": "AWS DevOps Agent",
                "capabilities": [
                    "Real-time AWS cost analysis",
                    "IaC analysis (Terraform/CloudFormation)",
                    "Security compliance validation",
                    "Multi-account operations",
                    "Automated PR generation"
                ]
            }
        else:
            return {
                "response": str(response),
                "status": "success",
                "agent": "AWS DevOps Agent",
                "data_source": "Real AWS APIs via MCP servers"
            }

    except Exception as e:
        print(f"❌ AWS DevOps Agent Error: {e}")
        return {
            "response": f"Error processing AWS DevOps request: {str(e)}",
            "status": "error",
            "error": str(e),
            "suggestion": "Check AWS credentials and MCP server connectivity"
        }


if __name__ == "__main__":
    print("🚀 Starting AWS DevOps Agent")
    print(f"🤖 Agent: {agent.name}")
    print("🔧 Tools: Cost optimization, IaC analysis, compliance validation, multi-account operations")
    print("🌐 Starting Bedrock Agent Core app...")
    app.run()