#!/usr/bin/env python3
"""Test GitHub connectivity using the GitHub MCP tools"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from aws_devops_agent.tools.github.integration import check_repository_connectivity, get_repository_info
    
    # Get repository from command line argument or use default
    repo = sys.argv[1] if len(sys.argv) > 1 else 'octocat/Hello-World'
    
    print(f"Testing connectivity to {repo}...")
    
    # Test connectivity
    result = check_repository_connectivity(repo)
    print('Connectivity:', '✅ Success' if result.get('status') == 'success' else '❌ Failed:', result.get('error', 'Unknown error'))
    
    # Test repository info if connectivity succeeded
    if result.get('status') == 'success':
        print('Repository Info:', '✅ Success' if result.get('status') == 'success' else '❌ Failed')
        info = get_repository_info(repo)
        print('Branches:', info.get('branch_count', 0), 'found')
    else:
        print('Repository Info: ❌ Skipped (connectivity failed)')
        
except Exception as e:
    print(f"❌ Error testing GitHub connectivity: {e}")
    sys.exit(1)
