#!/usr/bin/env python3
"""
Demo: AWS Security Analysis with Real APIs
Focused demonstrations of specific security capabilities
"""

import sys
import asyncio
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aws_devops_agent.tools.aws_security import (
    analyze_security_hub_findings,
    analyze_config_compliance,
    analyze_inspector_findings,
    get_security_recommendations,
    perform_comprehensive_security_analysis
)


async def demo_security_hub_focused():
    """Demo Security Hub with specific focus"""
    print("🔍 Security Hub Analysis Demo")
    print("=" * 40)
    print("Focus: Critical and High severity findings from last 7 days")
    
    try:
        result = analyze_security_hub_findings(
            severity_filter=['CRITICAL', 'HIGH'],
            time_range_days=7
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Total Findings: {result.get('total_findings', 0)}")
            print(f"Severity Breakdown: {analysis.get('severity_breakdown', {})}")
            print(f"Compliance Status: {analysis.get('compliance_status', 'Unknown')}")
            
            # Show top threats
            top_threats = analysis.get('top_threats', [])
            if top_threats:
                print("\n🚨 Top Security Threats:")
                for i, threat in enumerate(top_threats[:3], 1):
                    print(f"  {i}. {threat.get('threat')} ({threat.get('count')} occurrences)")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
            
    except Exception as e:
        print(f"Exception: {e}")


async def demo_config_compliance_focused():
    """Demo Config compliance with specific focus"""
    print("\n📋 Config Compliance Demo")
    print("=" * 40)
    print("Focus: Non-compliant resources and compliance score")
    
    try:
        result = analyze_config_compliance(
            compliance_types=['NON_COMPLIANT']
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Compliance Score: {analysis.get('compliance_score', 0)}/100")
            print(f"Non-compliant Resources: {len(analysis.get('non_compliant_resources', []))}")
            
            # Show non-compliant resources
            non_compliant = analysis.get('non_compliant_resources', [])
            if non_compliant:
                print("\n❌ Non-Compliant Resources:")
                for i, resource in enumerate(non_compliant[:3], 1):
                    print(f"  {i}. {resource.get('resource_id')} ({resource.get('resource_type')})")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
            
    except Exception as e:
        print(f"Exception: {e}")


async def demo_inspector_focused():
    """Demo Inspector with specific focus"""
    print("\n🔬 Inspector Vulnerability Demo")
    print("=" * 40)
    print("Focus: Critical vulnerabilities and affected resources")
    
    try:
        result = analyze_inspector_findings(
            severity_filter=['CRITICAL', 'HIGH']
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Total Findings: {result.get('total_findings', 0)}")
            print(f"Risk Assessment: {analysis.get('risk_assessment', 'Unknown')}")
            
            # Show affected resources
            affected_resources = analysis.get('affected_resources', {})
            if affected_resources:
                print(f"\n🎯 Affected Resources: {len(affected_resources)}")
                for i, (resource_id, data) in enumerate(list(affected_resources.items())[:3], 1):
                    print(f"  {i}. {resource_id} ({data.get('type')}) - {data.get('vulnerability_count')} vulnerabilities")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
            
    except Exception as e:
        print(f"Exception: {e}")


async def demo_trusted_advisor_focused():
    """Demo Trusted Advisor with specific focus"""
    print("\n💡 Trusted Advisor Security Demo")
    print("=" * 40)
    print("Focus: Security-specific recommendations and issues")
    
    try:
        result = get_security_recommendations()
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Security Checks: {result.get('total_security_checks', 0)}")
            print(f"Issues Found: {analysis.get('issues_found', 0)}")
            
            # Show security issues
            security_issues = analysis.get('security_issues', [])
            if security_issues:
                print("\n⚠️ Security Issues:")
                for i, issue in enumerate(security_issues[:3], 1):
                    print(f"  {i}. {issue.get('check_name')} - {issue.get('status')}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
            
    except Exception as e:
        print(f"Exception: {e}")


async def demo_comprehensive_focused():
    """Demo comprehensive analysis with specific focus"""
    print("\n🛡️ Comprehensive Security Analysis Demo")
    print("=" * 40)
    print("Focus: Overall security score and top 3 actionable recommendations")
    
    try:
        result = perform_comprehensive_security_analysis(
            include_findings=True,
            include_compliance=True,
            include_vulnerabilities=True,
            include_recommendations=True
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        
        if result.get('status') == 'success':
            summary = result.get('comprehensive_summary', {})
            print(f"Overall Security Score: {summary.get('overall_security_score', 0)}/100")
            print(f"Risk Level: {summary.get('risk_level', 'Unknown')}")
            print(f"Total Issues: {summary.get('total_issues', 0)}")
            
            # Show actionable recommendations
            recommendations = result.get('actionable_recommendations', [])
            if recommendations:
                print("\n🎯 Top 3 Actionable Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"  {i}. [{rec.get('priority', 'Unknown')}] {rec.get('action', 'Unknown')}")
                    print(f"     Source: {rec.get('source', 'Unknown')}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
            
    except Exception as e:
        print(f"Exception: {e}")


async def demo_terraform_security_focused():
    """Demo Terraform security with specific focus"""
    print("\n🏗️ Terraform Security Analysis Demo")
    print("=" * 40)
    print("Focus: Real AWS security analysis for infrastructure code")
    
    try:
        # Simulate a Terraform project analysis
        from aws_devops_agent.tools.aws_terraform import analyze_terraform_project
        
        # This would normally analyze a real Terraform project
        print("Note: This demo shows the integration capability")
        print("In production, this would analyze actual Terraform files")
        print("and use real AWS security APIs for analysis")
        
        print("\n✅ Terraform security analysis now uses:")
        print("  - Real Security Hub findings")
        print("  - Real Config compliance data")
        print("  - Real Inspector vulnerability data")
        print("  - Real Trusted Advisor recommendations")
        
    except Exception as e:
        print(f"Exception: {e}")


async def main():
    """Run focused security demos"""
    print("🚀 AWS Security Analysis - Focused Demos")
    print("=" * 50)
    print("Each demo focuses on specific capabilities with clear scope:")
    print("1. Security Hub: Critical/High findings from last 7 days")
    print("2. Config: Non-compliant resources and compliance score")
    print("3. Inspector: Critical vulnerabilities and affected resources")
    print("4. Trusted Advisor: Security-specific recommendations")
    print("5. Comprehensive: Overall score and top 3 recommendations")
    print("6. Terraform: Real AWS security integration")
    
    await demo_security_hub_focused()
    await demo_config_compliance_focused()
    await demo_inspector_focused()
    await demo_trusted_advisor_focused()
    await demo_comprehensive_focused()
    await demo_terraform_security_focused()
    
    print("\n🎉 Focused Demos Completed!")
    print("\nKey Benefits Demonstrated:")
    print("✅ Targeted analysis with specific scope")
    print("✅ Real AWS security data (when available)")
    print("✅ Clear, actionable insights")
    print("✅ Graceful error handling")
    print("✅ Production-ready security analysis")


if __name__ == "__main__":
    asyncio.run(main())
