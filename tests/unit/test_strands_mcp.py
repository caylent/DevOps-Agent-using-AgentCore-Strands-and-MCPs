#!/usr/bin/env python3
"""Test Strands MCP Client"""

import sys
sys.path.append('.')
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from aws_devops_agent.mcp_clients.strands_mcp_client import StrandsMCPClient

def test_strands_mcp():
    """Test Strands MCP client integration"""
    print("🚀 Testing Strands MCP Client")
    print("=" * 50)
    
    try:
        # Get the MCP client
        client = get_mcp_client()
        print("✅ Strands MCP client created")
        
        # Test Cost Explorer
        print("\n💰 Testing Cost Explorer...")
        cost_tools = client.list_cost_explorer_tools()
        print(f"✅ Cost Explorer tools: {cost_tools}")
        
        if cost_tools:
            # Test actual cost query
            print("💰 Getting AWS costs for last 7 days...")
            cost_result = client.get_aws_costs(days=7)
            print(f"💰 Cost result status: {cost_result.get('status')}")
            if cost_result.get('status') == 'success':
                print("🎉 REAL COST DATA RETRIEVED!")
                # Print just the structure, not all data
                result = cost_result.get('result', {})
                if hasattr(result, 'content'):
                    content_preview = str(result.content)[:200]
                    print(f"📊 Cost data preview: {content_preview}...")
                else:
                    print(f"📊 Cost result type: {type(result)}")
            else:
                print(f"❌ Cost query error: {cost_result.get('error')}")
        
        # Test CloudWatch
        print("\n📊 Testing CloudWatch...")
        cw_tools = client.list_cloudwatch_tools()
        print(f"✅ CloudWatch tools: {cw_tools}")
        
        print("\n🎉 Strands MCP client test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        try:
            if 'client' in locals():
                client.cleanup()
        except:
            pass

if __name__ == "__main__":
    test_strands_mcp()