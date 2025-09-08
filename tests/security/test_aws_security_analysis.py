#!/usr/bin/env python3
"""
Test AWS Security Analysis Tools
Tests the new real AWS security APIs implementation
"""

import sys
import os
import asyncio
import pytest
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Check for AWS credentials
def has_aws_credentials():
    """Check if AWS credentials are available"""
    return (
        os.getenv('AWS_ACCESS_KEY_ID') or 
        os.getenv('AWS_PROFILE') or 
        os.path.exists(os.path.expanduser('~/.aws/credentials'))
    )

from aws_devops_agent.tools.aws_security import (
    analyze_security_hub_findings,
    analyze_config_compliance,
    analyze_inspector_findings,
    get_security_recommendations,
    perform_comprehensive_security_analysis
)


@pytest.mark.asyncio
@pytest.mark.skipif(not has_aws_credentials(), reason="AWS credentials not available")
async def test_security_hub_analysis():
    """Test Security Hub analysis"""
    print("🔍 Testing Security Hub Analysis...")
    
    try:
        result = analyze_security_hub_findings(
            severity_filter=['CRITICAL', 'HIGH', 'MEDIUM'],
            time_range_days=30
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        print(f"Total Findings: {result.get('total_findings', 0)}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Severity Breakdown: {analysis.get('severity_breakdown', {})}")
            print(f"Compliance Status: {analysis.get('compliance_status', 'Unknown')}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"Exception: {e}")
        return False


@pytest.mark.asyncio
@pytest.mark.skipif(not has_aws_credentials(), reason="AWS credentials not available")
async def test_config_compliance():
    """Test Config compliance analysis"""
    print("\n📋 Testing Config Compliance Analysis...")
    
    try:
        result = analyze_config_compliance(
            compliance_types=['COMPLIANT', 'NON_COMPLIANT']
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        print(f"Total Evaluations: {result.get('total_evaluations', 0)}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Compliance Score: {analysis.get('compliance_score', 0)}")
            print(f"Non-compliant Resources: {len(analysis.get('non_compliant_resources', []))}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"Exception: {e}")
        return False


@pytest.mark.asyncio
@pytest.mark.skipif(not has_aws_credentials(), reason="AWS credentials not available")
async def test_inspector_analysis():
    """Test Inspector vulnerability analysis"""
    print("\n🔬 Testing Inspector Vulnerability Analysis...")
    
    try:
        result = analyze_inspector_findings(
            severity_filter=['CRITICAL', 'HIGH', 'MEDIUM']
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        print(f"Total Findings: {result.get('total_findings', 0)}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Severity Breakdown: {analysis.get('severity_breakdown', {})}")
            print(f"Risk Assessment: {analysis.get('risk_assessment', 'Unknown')}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"Exception: {e}")
        return False


@pytest.mark.asyncio
@pytest.mark.skipif(not has_aws_credentials(), reason="AWS credentials not available")
async def test_trusted_advisor():
    """Test Trusted Advisor recommendations"""
    print("\n💡 Testing Trusted Advisor Security Recommendations...")
    
    try:
        result = get_security_recommendations()
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        print(f"Total Security Checks: {result.get('total_security_checks', 0)}")
        
        if result.get('status') == 'success':
            analysis = result.get('analysis', {})
            print(f"Issues Found: {analysis.get('issues_found', 0)}")
            print(f"Security Issues: {len(analysis.get('security_issues', []))}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"Exception: {e}")
        return False


@pytest.mark.asyncio
@pytest.mark.skipif(not has_aws_credentials(), reason="AWS credentials not available")
async def test_comprehensive_analysis():
    """Test comprehensive security analysis"""
    print("\n🛡️ Testing Comprehensive Security Analysis...")
    
    try:
        result = perform_comprehensive_security_analysis(
            include_findings=True,
            include_compliance=True,
            include_vulnerabilities=True,
            include_recommendations=True
        )
        
        print(f"Status: {result.get('status')}")
        print(f"Data Source: {result.get('data_source')}")
        print(f"Components: {list(result.get('components', {}).keys())}")
        
        if result.get('status') == 'success':
            summary = result.get('comprehensive_summary', {})
            print(f"Overall Security Score: {summary.get('overall_security_score', 0)}")
            print(f"Risk Level: {summary.get('risk_level', 'Unknown')}")
            print(f"Total Issues: {summary.get('total_issues', 0)}")
            
            recommendations = result.get('actionable_recommendations', [])
            print(f"Actionable Recommendations: {len(recommendations)}")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"  {i}. [{rec.get('priority', 'Unknown')}] {rec.get('action', 'Unknown')}")
        else:
            print(f"Error: {result.get('error')}")
            print(f"Suggestion: {result.get('suggestion')}")
        
        return result.get('status') == 'success'
        
    except Exception as e:
        print(f"Exception: {e}")
        return False


async def main():
    """Run all security analysis tests"""
    print("🚀 Starting AWS Security Analysis Tests")
    print("=" * 50)
    
    tests = [
        ("Security Hub Analysis", test_security_hub_analysis),
        ("Config Compliance", test_config_compliance),
        ("Inspector Analysis", test_inspector_analysis),
        ("Trusted Advisor", test_trusted_advisor),
        ("Comprehensive Analysis", test_comprehensive_analysis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = await test_func()
            results.append((test_name, success))
            print(f"✅ {test_name}: {'PASSED' if success else 'FAILED'}")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All security analysis tests passed!")
    else:
        print("⚠️ Some tests failed - check AWS credentials and permissions")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
