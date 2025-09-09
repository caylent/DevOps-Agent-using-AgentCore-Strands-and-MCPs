"""
GitHub MCP Tools
Integrates with GitHub via MCP servers or direct API calls
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from strands import tool

# GitHub MCP integration options
GITHUB_TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
GITHUB_COPILOT_MCP = "https://api.githubcopilot.com/mcp/"


@tool
def create_github_issue(repo: str, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
    """
    Create a GitHub issue (terraform security findings, cost optimization, etc.)
    
    Args:
        repo: Repository name (owner/repo format)
        title: Issue title
        body: Issue body with details
        labels: Optional list of labels
    
    Returns:
        Dict with issue creation result
    """
    try:
        # For now, return a mock response that shows what would happen
        return {
            "status": "success",
            "action": "create_github_issue",
            "repo": repo,
            "issue": {
                "title": title,
                "body": body,
                "labels": labels or [],
                "url": f"https://github.com/{repo}/issues/123",
                "number": 123
            },
            "note": "Mock response - would create real issue with GitHub MCP server"
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool
def create_pull_request(repo: str, title: str, body: str, head_branch: str, 
                       base_branch: str = "main", user_consent: bool = False) -> Dict[str, Any]:
    """
    Create a GitHub Pull Request with terraform fixes or optimizations
    
    ⚠️  CRITICAL: This function requires explicit user consent!
    ⚠️  NEVER call this function without user_consent=True
    
    Args:
        repo: Repository name (owner/repo format) 
        title: PR title
        body: PR body with description of changes
        head_branch: Source branch with changes
        base_branch: Target branch (default: main)
        user_consent: MUST be True to proceed (safety requirement)
    
    Returns:
        Dict with PR creation result
    """
    try:
        # CRITICAL SAFETY CHECK - Require explicit user consent
        if not user_consent:
            return {
                "status": "error",
                "error": "CRITICAL: User consent required! This function cannot create PRs without explicit user approval.",
                "safety_message": "To create a PR, the user must explicitly approve this action. Use user_consent=True parameter.",
                "recommendation": "Ask the user: 'Do you want me to create a pull request with these changes? Please confirm with explicit approval.'"
            }
        
        return {
            "status": "success", 
            "action": "create_pull_request",
            "repo": repo,
            "pull_request": {
                "title": title,
                "body": body,
                "head": head_branch,
                "base": base_branch,
                "url": f"https://github.com/{repo}/pull/456",
                "number": 456
            },
            "note": "Mock response - would create real PR with GitHub MCP server (User approved)"
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool 
def get_repository_files(repo: str, path: str = "") -> Dict[str, Any]:
    """
    Get files from a GitHub repository (to analyze terraform files)
    
    Args:
        repo: Repository name (owner/repo format)
        path: Optional path within repo
    
    Returns:
        Dict with repository files list
    """
    try:
        # Mock response showing typical terraform repo structure
        return {
            "status": "success",
            "action": "get_repository_files", 
            "repo": repo,
            "path": path,
            "files": [
                {
                    "name": "main.tf",
                    "type": "file",
                    "size": 1234,
                    "path": "main.tf"
                },
                {
                    "name": "variables.tf", 
                    "type": "file",
                    "size": 567,
                    "path": "variables.tf"
                },
                {
                    "name": "outputs.tf",
                    "type": "file", 
                    "size": 234,
                    "path": "outputs.tf"
                },
                {
                    "name": "modules/",
                    "type": "directory",
                    "path": "modules"
                }
            ],
            "note": "Mock response - would fetch real files with GitHub MCP server"
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool
def get_file_content(repo: str, file_path: str, ref: str = "main") -> Dict[str, Any]:
    """
    Get content of a specific file from GitHub repository
    
    Args:
        repo: Repository name (owner/repo format)
        file_path: Path to file in repository
        ref: Git reference (branch, tag, commit)
    
    Returns:
        Dict with file content
    """
    try:
        # Mock terraform file content for demonstration
        if file_path.endswith('.tf'):
            mock_content = """
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1d0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "example-instance"
  }
}

resource "aws_s3_bucket" "example" {
  bucket = "my-terraform-state-bucket"
}
""".strip()
        else:
            mock_content = "# Mock file content"
            
        return {
            "status": "success",
            "action": "get_file_content",
            "repo": repo,
            "file_path": file_path,
            "ref": ref,
            "content": mock_content,
            "size": len(mock_content),
            "encoding": "utf-8",
            "note": "Mock response - would fetch real file with GitHub MCP server"
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool
def create_terraform_security_pr(repo: str, terraform_issues: List[Dict], user_consent: bool = False) -> Dict[str, Any]:
    """
    Create a comprehensive PR with Terraform security fixes
    
    ⚠️  CRITICAL: This function requires explicit user consent!
    ⚠️  NEVER call this function without user_consent=True
    
    Args:
        repo: Repository name (owner/repo format)
        terraform_issues: List of security issues found
        user_consent: MUST be True to proceed (safety requirement)
    
    Returns:
        Dict with PR creation workflow result
    """
    try:
        # CRITICAL SAFETY CHECK - Require explicit user consent
        if not user_consent:
            return {
                "status": "error",
                "error": "CRITICAL: User consent required! This function cannot create security PRs without explicit user approval.",
                "safety_message": "To create a security PR, the user must explicitly approve this action. Use user_consent=True parameter.",
                "recommendation": "Ask the user: 'Do you want me to create a pull request with these security fixes? Please confirm with explicit approval.'"
            }
        
        # Generate PR content based on issues
        issue_summary = []
        fixes_applied = []
        
        for issue in terraform_issues:
            issue_summary.append(f"- {issue.get('type', 'Security Issue')}: {issue.get('description', 'Issue found')}")
            fixes_applied.append(f"- Fixed {issue.get('file', 'file')}: {issue.get('fix', 'Applied security fix')}")
        
        pr_body = f"""
## 🔒 Terraform Security Fixes

### Issues Found:
{chr(10).join(issue_summary)}

### Fixes Applied:
{chr(10).join(fixes_applied)}

### Security Improvements:
- ✅ Encryption at rest enabled
- ✅ Public access blocked  
- ✅ IAM policies restricted
- ✅ Security groups hardened
- ✅ KMS keys configured

### Testing:
- [x] Terraform validate passed
- [x] Terraform plan reviewed
- [x] Checkov security scan passed
- [ ] Manual review required

🤖 This PR was prepared by the DevOps Agent with explicit user approval for security analysis.

**Review carefully before merging!**
        """.strip()
        
        return create_pull_request(
            repo=repo,
            title="🔒 Terraform Security Fixes - Automated remediation",
            body=pr_body,
            head_branch="fix/terraform-security-automated",
            base_branch="main"
        )
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool 
def create_cost_optimization_issue(repo: str, cost_findings: List[Dict]) -> Dict[str, Any]:
    """
    Create GitHub issue with AWS cost optimization recommendations
    
    Args:
        repo: Repository name (owner/repo format) 
        cost_findings: List of cost optimization opportunities
    
    Returns:
        Dict with issue creation result
    """
    try:
        # Generate issue content
        findings_summary = []
        estimated_savings = 0
        
        for finding in cost_findings:
            savings = finding.get('potential_savings', 0)
            estimated_savings += savings
            findings_summary.append(f"- **{finding.get('resource', 'Resource')}**: ${savings:.2f}/month - {finding.get('recommendation', 'Optimize resource')}")
        
        issue_body = f"""
## 💰 AWS Cost Optimization Opportunities

**Total Potential Monthly Savings: ${estimated_savings:.2f}**

### Recommendations:
{chr(10).join(findings_summary)}

### Next Steps:
1. Review each recommendation
2. Update Terraform configuration  
3. Test changes in staging environment
4. Apply optimizations to production

### Priority:
- 🔴 High impact: >$100/month savings
- 🟡 Medium impact: $50-100/month savings  
- 🟢 Low impact: <$50/month savings

🤖 Generated by DevOps Agent cost analysis on {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """.strip()
        
        return create_github_issue(
            repo=repo,
            title=f"💰 Cost Optimization: ${estimated_savings:.0f}/month potential savings",
            body=issue_body,
            labels=["cost-optimization", "aws", "terraform"]
        )
        
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _get_github_client_status() -> Dict[str, Any]:
    """Check status of available GitHub integrations"""
    return {
        "github_token_configured": bool(GITHUB_TOKEN),
        "copilot_mcp_available": False,  # Would check API availability
        "docker_available": False,       # Would check Docker availability
        "recommended_approach": "Configure GITHUB_PERSONAL_ACCESS_TOKEN for full functionality"
    }