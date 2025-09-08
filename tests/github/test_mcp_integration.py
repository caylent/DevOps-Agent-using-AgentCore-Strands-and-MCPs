#!/usr/bin/env python3
"""
GitHub MCP Integration Test Script
Test GitHub MCP wrapper functions with real repository

Usage:
    python3 tests/github/test_mcp_integration.py [repo] [token]
    
    repo:  GitHub repository in 'owner/repo' format (default: dpetrocelli/211125459593-iac-polyglot-infrastructure)
    token: GitHub Personal Access Token (required)

Examples:
    python3 tests/github/test_mcp_integration.py dpetrocelli/my-repo ghp_xxxxx
    GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxx python3 tests/github/test_mcp_integration.py dpetrocelli/my-repo
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

def test_github_mcp_integration(repo, token):
    """Test GitHub MCP integration with specified repo and token"""
    
    # Set token in environment
    os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'] = token
    
    print("=" * 50)
    print("🐙 GitHub MCP Integration Test")
    print("=" * 50)
    print(f"📁 Repository: {repo}")
    print(f"🔑 Token: {'*' * (len(token) - 8) + token[-8:]}")
    print()
    
    try:
        # Import GitHub MCP functions
        from aws_devops_agent.tools.github.integration import (
            check_repository_connectivity,
            list_repository_branches,
            get_repository_info,
            create_branch_simple
        )
        
        print("✅ GitHub MCP functions imported successfully")
        print()
        
        # Test 1: Repository connectivity
        print("🔍 Test 1: Repository Connectivity")
        print("-" * 30)
        
        result = check_repository_connectivity(repo)
        
        if result.get('status') == 'success':
            print(f"✅ Repository accessible: {result.get('accessible')}")
            print(f"✅ Authenticated user: {result.get('authenticated_user')}")
            print(f"✅ Repository exists: {result.get('repository_exists')}")
        else:
            print(f"❌ Connectivity failed: {result.get('error')}")
            return False
        
        print()
        
        # Test 2: List branches
        print("🌿 Test 2: List Repository Branches") 
        print("-" * 30)
        
        branches_result = list_repository_branches(repo)
        
        if branches_result.get('status') == 'success':
            branch_count = branches_result.get('total_branches', 0)
            branch_names = branches_result.get('branch_names', [])
            
            print(f"✅ Total branches: {branch_count}")
            print(f"✅ Branch names: {branch_names}")
            
            # Show first few branches with details
            branches = branches_result.get('branches', [])[:3]
            if branches:
                print("✅ Branch details (first 3):")
                for branch in branches:
                    name = branch.get('name', 'unknown')
                    protected = branch.get('protected', False)
                    sha = branch.get('commit_sha', 'unknown')[:7]
                    print(f"   - {name} (protected: {protected}, sha: {sha})")
        else:
            print(f"❌ Branch listing failed: {branches_result.get('error')}")
            return False
            
        print()
        
        # Test 3: Repository info
        print("📊 Test 3: Repository Info")
        print("-" * 30)
        
        info_result = get_repository_info(repo)
        
        if info_result.get('status') == 'success':
            print(f"✅ Owner: {info_result.get('owner')}")
            print(f"✅ Repo: {info_result.get('repo')}")
            print(f"✅ Accessible: {info_result.get('accessible')}")
            print(f"✅ Branch count: {info_result.get('branch_count')}")
            print(f"✅ Repository URL: {info_result.get('repository_url')}")
        else:
            print(f"❌ Repository info failed: {info_result.get('error')}")
            return False
            
        print()
        
        # Test 4: Function availability (no actual branch creation)
        print("🔧 Test 4: Branch Creation Function")
        print("-" * 30)
        print("✅ create_branch_simple function available")
        print("💡 Note: Not creating actual branch in test")
        
        print()
        print("=" * 50)
        print("🎉 All GitHub MCP tests passed!")
        print("=" * 50)
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the project root and venv is activated")
        return False
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to handle command line arguments"""
    
    # Default values
    default_repo = "dpetrocelli/211125459593-iac-polyglot-infrastructure"
    token = None
    repo = default_repo
    
    # Parse command line arguments
    if len(sys.argv) >= 2:
        repo = sys.argv[1]
    
    if len(sys.argv) >= 3:
        token = sys.argv[2]
    else:
        # Try to get token from environment
        token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    
    # Validate inputs
    if not token:
        print("❌ Error: GitHub Personal Access Token required")
        print()
        print("Usage:")
        print(f"  {sys.argv[0]} [repo] [token]")
        print(f"  GITHUB_PERSONAL_ACCESS_TOKEN=token {sys.argv[0]} [repo]")
        print()
        print("Examples:")
        print(f"  {sys.argv[0]} dpetrocelli/my-repo ghp_xxxxx")
        print(f"  GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxxxx {sys.argv[0]} dpetrocelli/my-repo")
        sys.exit(1)
    
    if '/' not in repo:
        print(f"❌ Error: Repository must be in 'owner/repo' format, got: {repo}")
        sys.exit(1)
    
    # Run the test
    success = test_github_mcp_integration(repo, token)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()