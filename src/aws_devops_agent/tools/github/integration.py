"""
GitHub Integration Tools - MCP Client Based
Simple wrapper functions that use GitHub MCP Server
"""

from typing import Dict, Any
from datetime import datetime
from strands import tool

# Import MCP client for GitHub MCP Server communication
try:
    from ...mcp_clients.mcp_client import mcp_client
except ImportError:
    mcp_client = None


@tool
def check_repository_connectivity(repository: str) -> Dict[str, Any]:
    """
    Check if we can access a GitHub repository using MCP server
    
    Args:
        repository: GitHub repository (owner/repo format)
    
    Returns:
        Dict containing connectivity status and repository info
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "MCP client not available",
                "recommendation": "Ensure GitHub MCP server is running and configured"
            }
        
        # Parse repository
        if '/' not in repository:
            return {"status": "error", "error": "Repository must be in 'owner/repo' format"}
        
        owner, repo = repository.split('/', 1)
        
        # Get GitHub MCP client and test connectivity
        github_client = mcp_client.get_github_client()
        if not github_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available",
                "recommendation": "Ensure GitHub MCP server is configured and running"
            }
        
        with github_client:
            # Test connectivity by getting basic repo info
            result = github_client.call_tool_sync(
                tool_use_id="test-repo-access",
                name="get_file_contents", 
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "path": "/"
                }
            )
            
            # Also get user info to verify authentication
            user_info = github_client.call_tool_sync(
                tool_use_id="test-auth",
                name="get_me", 
                arguments={}
            )
            
            # Parse MCP response format
            if result and result.get("status") == "success":
                # Extract user info
                user_login = "unknown"
                if user_info and user_info.get("status") == "success" and user_info.get("content"):
                    try:
                        import json
                        user_data = json.loads(user_info["content"][0]["text"])
                        user_login = user_data.get("login", "unknown")
                    except:
                        pass
                
                return {
                    "status": "success",
                    "repository": repository,
                    "accessible": True,
                    "authenticated_user": user_login,
                    "repository_exists": True,
                    "test_timestamp": datetime.now().isoformat(),
                    "mcp_server": "GitHub MCP Server"
                }
            else:
                return {
                    "status": "error",
                    "repository": repository,
                    "accessible": False,
                    "error": "Cannot access repository",
                    "recommendation": "Check repository name and permissions"
                }
            
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Failed to check repository connectivity: {str(e)}",
            "repository": repository
        }


@tool
def create_branch_simple(
    repository: str, 
    branch_name: str, 
    from_branch: str = "main"
) -> Dict[str, Any]:
    """
    Create a new branch in GitHub repository using MCP server
    
    Args:
        repository: GitHub repository (owner/repo format)
        branch_name: Name for the new branch
        from_branch: Source branch to create from (default: main)
    
    Returns:
        Dict containing branch creation results
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "MCP client not available"
            }
        
        # Parse repository
        if '/' not in repository:
            return {"status": "error", "error": "Repository must be in 'owner/repo' format"}
        
        owner, repo = repository.split('/', 1)
        
        # Get GitHub MCP client and create branch
        github_client = mcp_client.get_github_client()
        if not github_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available"
            }
        
        with github_client:
            result = github_client.call_tool_sync(
                tool_use_id="create-branch",
                name="create_branch", 
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "branch": branch_name,
                    "from_branch": from_branch
                }
            )
            
            if result and result.get("status") == "success":
                return {
                    "status": "success",
                    "repository": repository,
                    "branch_name": branch_name,
                    "from_branch": from_branch,
                    "branch_url": f"https://github.com/{repository}/tree/{branch_name}",
                    "created_timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "repository": repository,
                    "branch_name": branch_name,
                    "error": "Failed to create branch"
                }
            
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to create branch: {str(e)}",
            "repository": repository,
            "branch_name": branch_name
        }


@tool
def get_repository_info(repository: str) -> Dict[str, Any]:
    """
    Get basic repository information using MCP server
    
    Args:
        repository: GitHub repository (owner/repo format)
    
    Returns:
        Dict containing repository information
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "MCP client not available"
            }
        
        # Parse repository
        if '/' not in repository:
            return {"status": "error", "error": "Repository must be in 'owner/repo' format"}
        
        owner, repo = repository.split('/', 1)
        
        # Get GitHub MCP client
        github_client = mcp_client.get_github_client()
        if not github_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available"
            }
        
        with github_client:
            # Get repository root to check basic info
            repo_result = github_client.call_tool_sync(
                tool_use_id="get-repo-info",
                name="get_file_contents", 
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "path": "/"
                }
            )
            
            # Get branches list
            branches_result = github_client.call_tool_sync(
                tool_use_id="list-branches",
                name="list_branches", 
                arguments={
                    "owner": owner,
                    "repo": repo
                }
            )
            
            if repo_result and repo_result.get("status") == "success":
                branches = []
                if branches_result and branches_result.get("status") == "success" and branches_result.get("content"):
                    try:
                        import json
                        branches_data = json.loads(branches_result["content"][0]["text"])
                        branches = branches_data if isinstance(branches_data, list) else []
                    except:
                        branches = []
                
                return {
                    "status": "success",
                    "repository": repository,
                    "owner": owner,
                    "repo": repo,
                    "accessible": True,
                    "branches": [branch.get("name", "") for branch in branches] if branches else [],
                    "branch_count": len(branches),
                    "scan_timestamp": datetime.now().isoformat(),
                    "repository_url": f"https://github.com/{repository}"
                }
            else:
                return {
                    "status": "error",
                    "repository": repository,
                    "error": "Cannot access repository",
                    "accessible": False
                }
            
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to get repository info: {str(e)}",
            "repository": repository
        }


@tool
def list_repository_branches(repository: str, page: int = 1, per_page: int = 30) -> Dict[str, Any]:
    """
    List branches in a GitHub repository using MCP server
    
    Args:
        repository: GitHub repository (owner/repo format)  
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 30, max: 100)
    
    Returns:
        Dict containing list of branches
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "MCP client not available"
            }
        
        # Parse repository
        if '/' not in repository:
            return {"status": "error", "error": "Repository must be in 'owner/repo' format"}
        
        owner, repo = repository.split('/', 1)
        
        # Get GitHub MCP client
        github_client = mcp_client.get_github_client()
        if not github_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available"
            }
        
        with github_client:
            # List branches using MCP
            result = github_client.call_tool_sync(
                tool_use_id="list-repo-branches",
                name="list_branches", 
                arguments={
                    "owner": owner,
                    "repo": repo,
                    "page": page,
                    "perPage": min(per_page, 100)
                }
            )
            
            if result and result.get("status") == "success" and result.get("content"):
                try:
                    import json
                    branches = json.loads(result["content"][0]["text"])
                    if not isinstance(branches, list):
                        branches = []
                except:
                    branches = []
                
                return {
                    "status": "success",
                    "repository": repository,
                    "page": page,
                    "per_page": per_page,
                    "total_branches": len(branches),
                    "branches": [
                        {
                            "name": branch.get("name", "") if isinstance(branch, dict) else str(branch),
                            "protected": branch.get("protected", False) if isinstance(branch, dict) else False,
                            "commit_sha": branch.get("commit", {}).get("sha", "unknown") if isinstance(branch, dict) else "unknown"
                        }
                        for branch in branches
                    ],
                    "branch_names": [branch.get("name", "") if isinstance(branch, dict) else str(branch) for branch in branches],
                    "scan_timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "repository": repository,
                    "error": "Failed to list branches"
                }
            
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to list repository branches: {str(e)}",
            "repository": repository
        }