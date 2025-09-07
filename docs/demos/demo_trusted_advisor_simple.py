#!/usr/bin/env python3
"""
Demo: Trusted Advisor Security - Simple Focus
Demonstrates Trusted Advisor security analysis with a single, focused example
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aws_devops_agent.tools.aws_security import get_security_recommendations


def demo_trusted_advisor_simple():
    """Simple, focused Trusted Advisor demo"""
    print("💡 Trusted Advisor Security - Simple Demo")
    print("=" * 50)
    print("Purpose: Show how to get security recommendations from AWS Trusted Advisor")
    print("Scope: Security-specific checks and recommendations")
    print()
    
    try:
        # Call the Trusted Advisor security function
        result = get_security_recommendations()
        
        # Display results
        print(f"📊 Analysis Results:")
        print(f"   Status: {result.get('status')}")
        print(f"   Data Source: {result.get('data_source')}")
        print(f"   Security Checks: {result.get('total_security_checks', 0)}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"\n🎯 Security Analysis:")
            print(f"   Issues Found: {analysis.get('issues_found', 0)}")
            print(f"   Total Checks: {analysis.get('total_security_checks', 0)}")
            
            # Show security issues if available
            security_issues = analysis.get('security_issues', [])
            if security_issues:
                print(f"\n⚠️ Security Issues Found:")
                for i, issue in enumerate(security_issues[:5], 1):
                    print(f"   {i}. {issue.get('check_name', 'Unknown')}")
                    print(f"      Status: {issue.get('status', 'Unknown')}")
                    print(f"      Description: {issue.get('description', 'No description')[:80]}...")
                    print()
            else:
                print(f"\n✅ No security issues found")
                
            # Show recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                print(f"\n💡 Security Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec}")
                    
        else:
            print(f"\n❌ Analysis Failed:")
            print(f"   Error: {result.get('error')}")
            print(f"   Suggestion: {result.get('suggestion')}")
            
    except Exception as e:
        print(f"\n💥 Exception occurred: {e}")
    
    print(f"\n🎉 Demo completed!")
    print(f"This shows how to use Trusted Advisor for security recommendations.")


if __name__ == "__main__":
    demo_trusted_advisor_simple()
