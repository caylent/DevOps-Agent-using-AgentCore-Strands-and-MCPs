"""
GitHub Integration Tools
Automated PR generation and repository management for infrastructure improvements
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from strands import tool


@tool
def create_optimization_pull_request(
    repository: str, 
    optimization_type: str, 
    changes: Dict[str, Any], 
    branch_name: str = None,
    user_consent: bool = False
) -> Dict[str, Any]:
    """
    Create a pull request with AWS optimization recommendations
    
    ⚠️  CRITICAL: This function requires explicit user consent!
    ⚠️  NEVER call this function without user_consent=True
    
    Args:
        repository: GitHub repository (org/repo format)
        optimization_type: Type of optimization (cost, security, compliance, etc.)
        changes: Dictionary containing the changes to be made
        branch_name: Custom branch name (auto-generated if None)
        user_consent: MUST be True to proceed (safety requirement)
    
    Returns:
        Dict containing PR creation results and URL
    """
    try:
        # CRITICAL SAFETY CHECK - Require explicit user consent
        if not user_consent:
            return {
                "status": "error",
                "error": "CRITICAL: User consent required! This function cannot create PRs without explicit user approval.",
                "safety_message": "To create a PR, the user must explicitly approve this action. Use user_consent=True parameter.",
                "recommendation": "Ask the user: 'Do you want me to create a pull request with these optimization changes? Please confirm with explicit approval.'"
            }
        
        if not branch_name:
            branch_name = f"aws-optimization/{optimization_type.lower()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Prepare PR content
        pr_title = f"AWS {optimization_type.title()} Optimization - User Approved Changes"
        pr_body = _generate_optimization_pr_body(optimization_type, changes)
        
        # Simulate PR creation (in real implementation, this would use GitHub API)
        pr_result = {
            "status": "success",
            "repository": repository,
            "pr_number": 42,  # Simulated PR number
            "pr_url": f"https://github.com/{repository}/pull/42",
            "branch_name": branch_name,
            "title": pr_title,
            "optimization_type": optimization_type,
            "changes_summary": {
                "files_modified": len(changes.get("file_changes", [])),
                "configurations_updated": len(changes.get("config_updates", [])),
                "potential_savings": changes.get("estimated_savings", {})
            },
            "created_timestamp": datetime.now().isoformat(),
            "review_required": True,
            "automated_tests_status": "pending"
        }
        
        # Add specific details based on optimization type
        if optimization_type.lower() == "cost":
            pr_result["cost_analysis"] = {
                "monthly_savings": changes.get("monthly_savings", 0),
                "annual_savings": changes.get("annual_savings", 0),
                "affected_resources": changes.get("affected_resources", [])
            }
        elif optimization_type.lower() == "security":
            pr_result["security_improvements"] = {
                "vulnerabilities_addressed": len(changes.get("security_fixes", [])),
                "compliance_improvements": changes.get("compliance_improvements", []),
                "risk_reduction": changes.get("risk_reduction", "Medium")
            }
        elif optimization_type.lower() == "compliance":
            pr_result["compliance_updates"] = {
                "standards_addressed": changes.get("standards", []),
                "controls_implemented": len(changes.get("controls", [])),
                "compliance_score_improvement": changes.get("score_improvement", 0)
            }
        
        return pr_result
        
    except Exception as e:
        return {"status": "error", "error": f"Failed to create optimization PR: {str(e)}"}


@tool
def update_iac_via_github(
    repository: str,
    iac_tool: str,
    updates: Dict[str, Any],
    review_team: str = "platform-team",
    user_consent: bool = False
) -> Dict[str, Any]:
    """
    Update Infrastructure as Code via GitHub PR with proper reviews
    
    ⚠️  CRITICAL: This function requires explicit user consent!
    ⚠️  NEVER call this function without user_consent=True
    
    Args:
        repository: GitHub repository containing IaC
        iac_tool: IaC tool (terraform, cloudformation, etc.)
        updates: Updates to be made to IaC
        review_team: GitHub team for PR review
        user_consent: MUST be True to proceed (safety requirement)
    
    Returns:
        Dict containing IaC update PR results
    """
    try:
        # CRITICAL SAFETY CHECK - Require explicit user consent
        if not user_consent:
            return {
                "status": "error",
                "error": "CRITICAL: User consent required! This function cannot modify IaC without explicit user approval.",
                "safety_message": "To update IaC, the user must explicitly approve this action. Use user_consent=True parameter.",
                "recommendation": "Ask the user: 'Do you want me to create a pull request with these IaC changes? Please confirm with explicit approval.'"
            }
        
        branch_name = f"iac-updates/{iac_tool.lower()}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Prepare IaC-specific PR content
        pr_title = f"Infrastructure Update: {iac_tool.title()} Configuration Changes - User Approved"
        pr_body = _generate_iac_pr_body(iac_tool, updates)
        
        # Create PR with IaC-specific handling
        pr_result = {
            "status": "success",
            "repository": repository,
            "pr_number": 43,
            "pr_url": f"https://github.com/{repository}/pull/43",
            "branch_name": branch_name,
            "title": pr_title,
            "iac_tool": iac_tool,
            "updates_summary": {
                "resources_modified": len(updates.get("resources", [])),
                "configurations_changed": len(updates.get("configurations", [])),
                "safety_checks": updates.get("safety_checks", [])
            },
            "review_requirements": {
                "required_reviewers": [review_team],
                "auto_merge_enabled": False,
                "requires_plan_approval": iac_tool.lower() == "terraform"
            },
            "deployment_pipeline": {
                "plan_step": "terraform plan" if iac_tool.lower() == "terraform" else "validate template",
                "test_environments": ["staging", "pre-production"],
                "approval_gates": True
            },
            "created_timestamp": datetime.now().isoformat()
        }
        
        # Add tool-specific validations
        if iac_tool.lower() == "terraform":
            pr_result["terraform_specific"] = {
                "plan_command": "terraform plan -out=tfplan",
                "state_backend": "s3",
                "workspace": updates.get("workspace", "default"),
                "validation_steps": [
                    "terraform fmt -check",
                    "terraform validate", 
                    "tflint",
                    "checkov"
                ]
            }
        elif iac_tool.lower() == "cloudformation":
            pr_result["cloudformation_specific"] = {
                "template_validation": "aws cloudformation validate-template",
                "stack_policy": updates.get("stack_policy"),
                "change_set_required": True,
                "rollback_configuration": updates.get("rollback_config", {})
            }
        
        return pr_result
        
    except Exception as e:
        return {"status": "error", "error": f"Failed to update IaC via GitHub: {str(e)}"}


@tool
def list_infrastructure_repositories(
    organization: str,
    repository_type: str = "all",
    include_archived: bool = False
) -> Dict[str, Any]:
    """
    List GitHub repositories containing infrastructure code
    
    Args:
        organization: GitHub organization name
        repository_type: Type of repositories (terraform, cloudformation, ansible, all)
        include_archived: Whether to include archived repositories
    
    Returns:
        Dict containing list of infrastructure repositories
    """
    try:
        # Simulate repository discovery (real implementation would use GitHub API)
        repositories = _discover_infrastructure_repositories(organization, repository_type, include_archived)
        
        repository_summary = {
            "status": "success",
            "organization": organization,
            "repository_type": repository_type,
            "scan_timestamp": datetime.now().isoformat(),
            "total_repositories": len(repositories),
            "repositories": repositories,
            "statistics": {
                "terraform_repos": len([r for r in repositories if "terraform" in r.get("technologies", [])]),
                "cloudformation_repos": len([r for r in repositories if "cloudformation" in r.get("technologies", [])]),
                "ansible_repos": len([r for r in repositories if "ansible" in r.get("technologies", [])]),
                "active_repos": len([r for r in repositories if not r.get("archived", False)]),
                "archived_repos": len([r for r in repositories if r.get("archived", False)])
            },
            "recommendations": _generate_repository_recommendations(repositories)
        }
        
        return repository_summary
        
    except Exception as e:
        return {"status": "error", "error": f"Failed to list infrastructure repositories: {str(e)}"}


@tool
def monitor_infrastructure_prs(
    repository: str,
    monitoring_scope: str = "open",
    days_back: int = 30
) -> Dict[str, Any]:
    """
    Monitor infrastructure-related pull requests
    
    Args:
        repository: GitHub repository to monitor
        monitoring_scope: Scope of monitoring (open, merged, all)
        days_back: Number of days to look back
    
    Returns:
        Dict containing PR monitoring results
    """
    try:
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Simulate PR monitoring (real implementation would use GitHub API)
        prs = _get_infrastructure_prs(repository, monitoring_scope, cutoff_date)
        
        monitoring_results = {
            "status": "success",
            "repository": repository,
            "monitoring_scope": monitoring_scope,
            "monitoring_period": f"{days_back} days",
            "scan_timestamp": datetime.now().isoformat(),
            "total_prs": len(prs),
            "pull_requests": prs,
            "pr_statistics": {
                "open_prs": len([pr for pr in prs if pr.get("state") == "open"]),
                "merged_prs": len([pr for pr in prs if pr.get("state") == "merged"]),
                "closed_prs": len([pr for pr in prs if pr.get("state") == "closed"]),
                "average_review_time": "2.5 days",
                "automation_generated": len([pr for pr in prs if pr.get("automated", False)])
            },
            "risk_analysis": _analyze_pr_risks(prs),
            "recommendations": _generate_pr_monitoring_recommendations(prs)
        }
        
        return monitoring_results
        
    except Exception as e:
        return {"status": "error", "error": f"Failed to monitor infrastructure PRs: {str(e)}"}


@tool
def setup_infrastructure_automation(
    repository: str,
    automation_type: str,
    configuration: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Setup GitHub Actions or other automation for infrastructure management
    
    Args:
        repository: GitHub repository
        automation_type: Type of automation (ci_cd, security_scanning, cost_monitoring)
        configuration: Automation configuration
    
    Returns:
        Dict containing automation setup results
    """
    try:
        automation_result = {
            "status": "success",
            "repository": repository,
            "automation_type": automation_type,
            "setup_timestamp": datetime.now().isoformat(),
            "configuration": configuration,
            "workflow_files": [],
            "automation_features": [],
            "integration_points": []
        }
        
        if automation_type == "ci_cd":
            automation_result.update(_setup_ci_cd_automation(repository, configuration))
        elif automation_type == "security_scanning":
            automation_result.update(_setup_security_scanning_automation(repository, configuration))
        elif automation_type == "cost_monitoring":
            automation_result.update(_setup_cost_monitoring_automation(repository, configuration))
        else:
            return {"status": "error", "error": f"Unsupported automation type: {automation_type}"}
        
        return automation_result
        
    except Exception as e:
        return {"status": "error", "error": f"Failed to setup infrastructure automation: {str(e)}"}


# Helper functions
def _generate_optimization_pr_body(optimization_type: str, changes: Dict[str, Any]) -> str:
    """Generate PR body for optimization changes"""
    body = f"""# AWS {optimization_type.title()} Optimization

This pull request implements automated {optimization_type} optimizations based on analysis of your AWS infrastructure.

## Changes Summary

"""
    
    if optimization_type.lower() == "cost":
        body += f"""
### Cost Optimization
- **Estimated Monthly Savings**: ${changes.get('monthly_savings', 0):.2f}
- **Estimated Annual Savings**: ${changes.get('annual_savings', 0):.2f}
- **Resources Affected**: {len(changes.get('affected_resources', []))}

### Specific Changes
"""
        for change in changes.get("specific_changes", []):
            body += f"- {change}\n"
    
    elif optimization_type.lower() == "security":
        body += f"""
### Security Improvements
- **Vulnerabilities Addressed**: {len(changes.get('security_fixes', []))}
- **Risk Reduction**: {changes.get('risk_reduction', 'Medium')}

### Security Fixes
"""
        for fix in changes.get("security_fixes", []):
            body += f"- {fix}\n"
    
    body += """
## Review Checklist
- [ ] Changes have been tested in staging environment
- [ ] Security implications have been reviewed
- [ ] Cost impact has been analyzed
- [ ] Rollback plan is documented

## Deployment Notes
This change requires careful review and testing before production deployment.

---
*This pull request was prepared by AWS DevOps Agent with explicit user approval*
"""
    
    return body


def _generate_iac_pr_body(iac_tool: str, updates: Dict[str, Any]) -> str:
    """Generate PR body for IaC updates"""
    body = f"""# Infrastructure Update: {iac_tool.title()}

This pull request updates infrastructure configuration based on best practices analysis.

## Changes Overview

"""
    
    if iac_tool.lower() == "terraform":
        body += f"""
### Terraform Changes
- **Resources Modified**: {len(updates.get('resources', []))}
- **Configuration Updates**: {len(updates.get('configurations', []))}
- **Workspace**: {updates.get('workspace', 'default')}

### Plan Output
```
{updates.get('plan_output', 'Run terraform plan to see changes')}
```
"""
    elif iac_tool.lower() == "cloudformation":
        body += f"""
### CloudFormation Changes
- **Stack**: {updates.get('stack_name', 'TBD')}
- **Resources Modified**: {len(updates.get('resources', []))}
- **Change Set**: Will be created upon approval

### Template Validation
- [ ] Template syntax validated
- [ ] Template policies checked
- [ ] Parameter validation completed
"""
    
    body += """
## Deployment Plan
1. Review changes carefully
2. Run validation/plan commands
3. Test in staging environment
4. Apply to production with approval

## Safety Measures
- [ ] Rollback plan documented
- [ ] Change set reviewed (CloudFormation)
- [ ] Terraform plan analyzed
- [ ] State backup verified

---
*Infrastructure changes require careful review and testing*
"""
    
    return body


def _discover_infrastructure_repositories(organization: str, repo_type: str, include_archived: bool) -> List[Dict[str, Any]]:
    """Discover infrastructure repositories in organization"""
    # Simulate repository discovery
    base_repos = [
        {
            "name": "infrastructure-terraform",
            "full_name": f"{organization}/infrastructure-terraform",
            "description": "Main Terraform infrastructure repository",
            "technologies": ["terraform", "aws"],
            "archived": False,
            "private": True,
            "default_branch": "main",
            "last_activity": "2024-01-15T10:30:00Z"
        },
        {
            "name": "cloudformation-templates", 
            "full_name": f"{organization}/cloudformation-templates",
            "description": "CloudFormation templates for AWS resources",
            "technologies": ["cloudformation", "aws"],
            "archived": False,
            "private": True,
            "default_branch": "main",
            "last_activity": "2024-01-14T15:45:00Z"
        },
        {
            "name": "ansible-playbooks",
            "full_name": f"{organization}/ansible-playbooks", 
            "description": "Ansible configuration management",
            "technologies": ["ansible", "configuration"],
            "archived": True,
            "private": True,
            "default_branch": "main",
            "last_activity": "2023-12-01T09:00:00Z"
        }
    ]
    
    # Filter based on parameters
    filtered_repos = []
    for repo in base_repos:
        # Filter by archived status
        if not include_archived and repo.get("archived", False):
            continue
        
        # Filter by repository type
        if repo_type != "all":
            if repo_type.lower() not in repo.get("technologies", []):
                continue
        
        filtered_repos.append(repo)
    
    return filtered_repos


def _generate_repository_recommendations(repositories: List[Dict[str, Any]]) -> List[str]:
    """Generate recommendations based on repository analysis"""
    recommendations = []
    
    archived_repos = [r for r in repositories if r.get("archived", False)]
    if archived_repos:
        recommendations.append(f"Consider reviewing {len(archived_repos)} archived repositories for cleanup")
    
    terraform_repos = [r for r in repositories if "terraform" in r.get("technologies", [])]
    if len(terraform_repos) > 1:
        recommendations.append("Consider consolidating multiple Terraform repositories for better management")
    
    recommendations.extend([
        "Implement consistent repository naming conventions",
        "Add comprehensive README files to all infrastructure repositories",
        "Setup branch protection rules for infrastructure repositories",
        "Implement automated security scanning for all repositories"
    ])
    
    return recommendations


def _get_infrastructure_prs(repository: str, scope: str, cutoff_date: datetime) -> List[Dict[str, Any]]:
    """Get infrastructure PRs from repository"""
    # Simulate PR retrieval
    sample_prs = [
        {
            "number": 42,
            "title": "AWS Cost Optimization Updates",
            "state": "open",
            "created_at": "2024-01-14T10:00:00Z",
            "updated_at": "2024-01-15T14:30:00Z",
            "author": "aws-devops-agent",
            "automated": True,
            "labels": ["infrastructure", "cost-optimization"],
            "files_changed": 3,
            "risk_level": "low"
        },
        {
            "number": 41,
            "title": "Security Group Updates",
            "state": "merged",
            "created_at": "2024-01-12T15:00:00Z",
            "updated_at": "2024-01-13T09:30:00Z",
            "merged_at": "2024-01-13T09:30:00Z",
            "author": "platform-team",
            "automated": False,
            "labels": ["infrastructure", "security"],
            "files_changed": 2,
            "risk_level": "medium"
        }
    ]
    
    # Filter by scope
    if scope == "open":
        return [pr for pr in sample_prs if pr.get("state") == "open"]
    elif scope == "merged":
        return [pr for pr in sample_prs if pr.get("state") == "merged"]
    
    return sample_prs


def _analyze_pr_risks(prs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze risks in infrastructure PRs"""
    high_risk_prs = len([pr for pr in prs if pr.get("risk_level") == "high"])
    automated_prs = len([pr for pr in prs if pr.get("automated", False)])
    
    return {
        "overall_risk_level": "Medium",
        "high_risk_prs": high_risk_prs,
        "automated_prs": automated_prs,
        "risk_factors": [
            "Multiple infrastructure changes in single PR",
            "PRs without proper review requirements",
            "Large number of files changed in single PR"
        ],
        "mitigation_recommendations": [
            "Implement mandatory PR reviews for infrastructure changes",
            "Add automated testing for infrastructure changes",
            "Require approval from platform team for high-risk changes"
        ]
    }


def _generate_pr_monitoring_recommendations(prs: List[Dict[str, Any]]) -> List[str]:
    """Generate recommendations based on PR monitoring"""
    recommendations = []
    
    open_prs = [pr for pr in prs if pr.get("state") == "open"]
    if len(open_prs) > 5:
        recommendations.append("Consider reducing the number of open PRs for better focus")
    
    automated_prs = [pr for pr in prs if pr.get("automated", False)]
    if len(automated_prs) > 0:
        recommendations.append(f"Monitor {len(automated_prs)} automated PRs for proper review")
    
    recommendations.extend([
        "Implement PR templates for infrastructure changes",
        "Setup automated testing for all infrastructure PRs",
        "Add required status checks before merging"
    ])
    
    return recommendations


def _setup_ci_cd_automation(repository: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
    """Setup CI/CD automation"""
    return {
        "workflow_files": [
            ".github/workflows/terraform-ci.yml",
            ".github/workflows/terraform-cd.yml"
        ],
        "automation_features": [
            "Terraform plan on PR",
            "Terraform apply on merge to main",
            "Automated testing",
            "Security scanning"
        ],
        "integration_points": [
            "AWS credentials via OIDC",
            "Terraform Cloud/Enterprise",
            "Slack notifications"
        ]
    }


def _setup_security_scanning_automation(repository: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
    """Setup security scanning automation"""
    return {
        "workflow_files": [
            ".github/workflows/security-scan.yml",
            ".github/workflows/compliance-check.yml"
        ],
        "automation_features": [
            "Terraform security scanning with Checkov",
            "Secret scanning",
            "Dependency vulnerability scanning",
            "Infrastructure compliance checks"
        ],
        "integration_points": [
            "Security findings in PR comments",
            "SARIF uploads to GitHub Security tab",
            "Integration with security monitoring tools"
        ]
    }


def _setup_cost_monitoring_automation(repository: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
    """Setup cost monitoring automation"""
    return {
        "workflow_files": [
            ".github/workflows/cost-estimation.yml",
            ".github/workflows/cost-monitoring.yml"
        ],
        "automation_features": [
            "Terraform cost estimation on PR",
            "Cost impact analysis",
            "Resource optimization suggestions",
            "Monthly cost reports"
        ],
        "integration_points": [
            "AWS Cost Explorer API",
            "Cost optimization recommendations in PRs",
            "Cost alerts and notifications"
        ]
    }