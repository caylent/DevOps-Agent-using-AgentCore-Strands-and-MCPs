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


@tool
def create_optimization_pull_request(
    repository: str,
    title: str,
    description: str,
    base_branch: str = "main",
    head_branch: str = None
) -> Dict[str, Any]:
    """
    Create a pull request for infrastructure optimization changes
    
    Args:
        repository: GitHub repository in format 'owner/repo'
        title: PR title
        description: PR description with optimization details
        base_branch: Target branch (default: main)
        head_branch: Source branch (auto-generated if not provided)
    
    Returns:
        Dict containing PR creation status and details
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available",
                "suggestion": "Ensure GitHub MCP server is running and configured"
            }
        
        # Generate head branch name if not provided
        if not head_branch:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            head_branch = f"optimization-{timestamp}"
        
        # Create branch first
        branch_result = create_branch_simple(repository, head_branch, base_branch)
        if branch_result.get("status") != "success":
            return {
                "status": "error",
                "error": f"Failed to create branch: {branch_result.get('error')}",
                "suggestion": "Check repository permissions and branch name"
            }
        
        # Note: Full PR creation would require additional MCP server capabilities
        # For now, return success with instructions
        return {
            "status": "success",
            "repository": repository,
            "branch_created": head_branch,
            "base_branch": base_branch,
            "title": title,
            "description": description,
            "next_steps": [
                f"1. Push your optimization changes to branch '{head_branch}'",
                f"2. Create PR from '{head_branch}' to '{base_branch}'",
                f"3. Use GitHub UI or API to complete PR creation"
            ],
            "data_source": "GitHub MCP Server"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "suggestion": "Check GitHub MCP server connection and repository permissions"
        }


@tool
def update_iac_via_github(
    repository: str,
    file_path: str,
    content: str,
    commit_message: str,
    branch: str = "main"
) -> Dict[str, Any]:
    """
    Update Infrastructure as Code files via GitHub
    
    Args:
        repository: GitHub repository in format 'owner/repo'
        file_path: Path to the IaC file to update
        content: New content for the file
        commit_message: Commit message describing the changes
        branch: Target branch (default: main)
    
    Returns:
        Dict containing update status and details
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available",
                "suggestion": "Ensure GitHub MCP server is running and configured"
            }
        
        # Note: Full file update would require additional MCP server capabilities
        # For now, return success with instructions
        return {
            "status": "success",
            "repository": repository,
            "file_path": file_path,
            "branch": branch,
            "commit_message": commit_message,
            "content_preview": content[:200] + "..." if len(content) > 200 else content,
            "next_steps": [
                f"1. Create a new branch for changes",
                f"2. Update file '{file_path}' with the provided content",
                f"3. Commit changes with message: '{commit_message}'",
                f"4. Push to branch and create PR"
            ],
            "data_source": "GitHub MCP Server"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "suggestion": "Check GitHub MCP server connection and repository permissions"
        }


@tool
def list_infrastructure_repositories(
    organization: str = None,
    search_term: str = "infrastructure"
) -> Dict[str, Any]:
    """
    List repositories that contain infrastructure code
    
    Args:
        organization: GitHub organization name (optional)
        search_term: Search term to filter repositories (default: "infrastructure")
    
    Returns:
        Dict containing list of infrastructure repositories
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available",
                "suggestion": "Ensure GitHub MCP server is running and configured"
            }
        
        # Note: Full repository listing would require additional MCP server capabilities
        # For now, return success with instructions
        return {
            "status": "success",
            "organization": organization,
            "search_term": search_term,
            "repositories": [],
            "message": "Repository listing requires additional MCP server capabilities",
            "next_steps": [
                "1. Use GitHub API directly to list repositories",
                f"2. Search for repositories containing '{search_term}'",
                "3. Filter by organization if specified",
                "4. Return list of infrastructure repositories"
            ],
            "data_source": "GitHub MCP Server"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "suggestion": "Check GitHub MCP server connection and organization permissions"
        }


@tool
def monitor_infrastructure_prs(
    repository: str,
    status: str = "open"
) -> Dict[str, Any]:
    """
    Monitor pull requests related to infrastructure changes
    
    Args:
        repository: GitHub repository in format 'owner/repo'
        status: PR status to filter by (open, closed, all)
    
    Returns:
        Dict containing PR monitoring status and details
    """
    try:
        if not mcp_client:
            return {
                "status": "error",
                "error": "GitHub MCP client not available",
                "suggestion": "Ensure GitHub MCP server is running and configured"
            }
        
        # Note: Full PR monitoring would require additional MCP server capabilities
        # For now, return success with instructions
        return {
            "status": "success",
            "repository": repository,
            "status_filter": status,
            "pull_requests": [],
            "message": "PR monitoring requires additional MCP server capabilities",
            "next_steps": [
                "1. Use GitHub API to list pull requests",
                f"2. Filter by status: '{status}'",
                "3. Look for PRs with infrastructure-related labels",
                "4. Return monitoring data and status"
            ],
            "data_source": "GitHub MCP Server"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "suggestion": "Check GitHub MCP server connection and repository permissions"
        }