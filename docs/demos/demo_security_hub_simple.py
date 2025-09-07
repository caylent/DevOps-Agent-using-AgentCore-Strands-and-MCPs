#!/usr/bin/env python3
"""
Demo: Security Hub Analysis - Simple Focus
Demonstrates Security Hub analysis with a single, focused example
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aws_devops_agent.tools.aws_security import analyze_security_hub_findings


def demo_security_hub_simple():
    """Simple, focused Security Hub demo"""
    print("🔍 Security Hub Analysis - Simple Demo")
    print("=" * 50)
    print("Purpose: Show how to get critical security findings from AWS Security Hub")
    print("Scope: Critical and High severity findings from last 30 days")
    print()
    
    try:
        # Call the Security Hub analysis function
        result = analyze_security_hub_findings(
            severity_filter=['CRITICAL', 'HIGH'],
            time_range_days=30
        )
        
        # Display results
        print(f"📊 Analysis Results:")
        print(f"   Status: {result.get('status')}")
        print(f"   Data Source: {result.get('data_source')}")
        print(f"   Time Range: {result.get('time_range')}")
        print(f"   Total Findings: {result.get('total_findings', 0)}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"\n🎯 Security Analysis:")
            print(f"   Severity Breakdown: {analysis.get('severity_breakdown', {})}")
            print(f"   Compliance Status: {analysis.get('compliance_status', 'Unknown')}")
            
            # Show top threats if available
            top_threats = analysis.get('top_threats', [])
            if top_threats:
                print(f"\n🚨 Top Security Threats:")
                for i, threat in enumerate(top_threats[:3], 1):
                    print(f"   {i}. {threat.get('threat')} ({threat.get('count')} occurrences)")
            else:
                print(f"\n✅ No critical or high severity threats found")
                
        else:
            print(f"\n❌ Analysis Failed:")
            print(f"   Error: {result.get('error')}")
            print(f"   Suggestion: {result.get('suggestion')}")
            
    except Exception as e:
        print(f"\n💥 Exception occurred: {e}")
    
    print(f"\n🎉 Demo completed!")
    print(f"This shows how to use Security Hub for focused security analysis.")


if __name__ == "__main__":
    demo_security_hub_simple()
