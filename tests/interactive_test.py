#!/usr/bin/env python3
"""
Interactive Testing for AWS DevOps Agent
Test both Strands and Bedrock Agent Core integration
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "config"))
sys.path.append(str(project_root / "tools" / "aws-devops"))

from config.app_config import get_config
from tools.aws_cost_tools import get_real_aws_pricing, analyze_cost_optimization_opportunities
from tools.aws_iac_tools import analyze_terraform_configuration, scan_infrastructure_drift
from tools.aws_compliance_tools import validate_security_policies, check_compliance_standards
from tools.aws_multi_account_tools import list_cross_account_resources
from tools.github_integration_tools import create_optimization_pull_request


class InteractiveAWSDevOpsTest:
    """Interactive testing environment for AWS DevOps Agent"""
    
    def __init__(self):
        print("🚀 AWS DevOps Agent - Interactive Testing Environment")
        print("=" * 60)
        self.config = get_config()
        print(f"📋 Model: {self.config.model.model_id}")
        print(f"🌍 Region: {self.config.aws_region}")
        print("=" * 60)
    
    def show_menu(self):
        """Display interactive menu"""
        print("\n🎯 Available Test Categories:")
        print("1. 💰 Cost Optimization Tools")
        print("2. 🏗️  Infrastructure as Code (IaC) Analysis")
        print("3. 🔒 Compliance & Security Validation")
        print("4. 🌐 Multi-Account Management")
        print("5. 📱 GitHub Integration & PR Automation")
        print("6. 🧪 Run All Tests")
        print("0. ❌ Exit")
        return input("\n👤 Select option (0-6): ").strip()
    
    def test_cost_optimization(self):
        """Test cost optimization tools"""
        print("\n💰 Testing Cost Optimization Tools")
        print("-" * 40)
        
        print("🔍 1. Testing Real AWS Pricing...")
        pricing_result = get_real_aws_pricing("EC2", "t3.medium", "us-east-1")
        self._print_result("AWS Pricing", pricing_result)
        
        print("\n🔍 2. Testing Cost Optimization Analysis...")
        config = {"instance_type": "t3.large", "region": "us-east-1"}
        optimization_result = analyze_cost_optimization_opportunities("EC2", config)
        self._print_result("Cost Optimization", optimization_result)
        
        print("\n💡 Cost Optimization Test Complete!")
    
    def test_iac_analysis(self):
        """Test IaC analysis tools"""
        print("\n🏗️ Testing Infrastructure as Code Analysis")
        print("-" * 45)
        
        print("🔍 1. Testing Infrastructure Drift Scanning...")
        drift_result = scan_infrastructure_drift("EC2", None, "us-east-1")
        self._print_result("Infrastructure Drift", drift_result)
        
        print("\n🔍 2. Testing Terraform Analysis (simulated)...")
        # Note: Would need actual Terraform files for real testing
        print("   📝 Would analyze Terraform configurations for:")
        print("   • Security best practices")
        print("   • Cost optimization opportunities")
        print("   • Compliance violations")
        print("   • Resource drift detection")
        
        print("\n💡 IaC Analysis Test Complete!")
    
    def test_compliance_security(self):
        """Test compliance and security tools"""
        print("\n🔒 Testing Compliance & Security Validation")
        print("-" * 45)
        
        print("🔍 1. Testing EC2 Security Policy Validation...")
        ec2_config = {
            "associate_public_ip_address": True,
            "security_groups": ["sg-12345 (0.0.0.0/0)"]
        }
        security_result = validate_security_policies("EC2", ec2_config)
        self._print_result("EC2 Security Validation", security_result)
        
        print("\n🔍 2. Testing SOC2 Compliance Check...")
        resource_configs = [
            {"type": "EC2", "config": ec2_config},
            {"type": "RDS", "config": {"encrypted": False, "publicly_accessible": True}}
        ]
        compliance_result = check_compliance_standards("SOC2", resource_configs)
        self._print_result("SOC2 Compliance", compliance_result)
        
        print("\n💡 Compliance & Security Test Complete!")
    
    def test_multi_account(self):
        """Test multi-account management"""
        print("\n🌐 Testing Multi-Account Management")
        print("-" * 40)
        
        print("🔍 1. Testing Cross-Account Resource Listing...")
        cross_account_result = list_cross_account_resources(
            "EC2", 
            ["123456789012", "123456789013"], 
            ["us-east-1", "us-west-2"]
        )
        self._print_result("Cross-Account Resources", cross_account_result)
        
        print("\n💡 Multi-Account Management Test Complete!")
    
    def test_github_integration(self):
        """Test GitHub integration tools"""
        print("\n📱 Testing GitHub Integration & PR Automation")
        print("-" * 50)
        
        print("🔍 1. Testing Optimization PR Creation...")
        changes = {
            "monthly_savings": 150.0,
            "annual_savings": 1800.0,
            "affected_resources": ["i-12345", "i-67890"],
            "specific_changes": [
                "Right-size t3.large to t3.medium instances",
                "Enable Reserved Instance recommendations"
            ]
        }
        
        pr_result = create_optimization_pull_request(
            "myorg/infrastructure",
            "cost",
            changes
        )
        self._print_result("GitHub PR Creation", pr_result)
        
        print("\n💡 GitHub Integration Test Complete!")
    
    def run_all_tests(self):
        """Run all test categories"""
        print("\n🧪 Running All Tests")
        print("=" * 30)
        
        self.test_cost_optimization()
        self.test_iac_analysis()
        self.test_compliance_security()
        self.test_multi_account()
        self.test_github_integration()
        
        print("\n🎉 All Tests Complete!")
        print("=" * 30)
    
    def _print_result(self, test_name: str, result: dict):
        """Print formatted test result"""
        status = result.get("status", "unknown")
        status_emoji = "✅" if status == "success" else "❌"
        
        print(f"   {status_emoji} {test_name}: {status.upper()}")
        
        if status == "success":
            # Print key information based on result type
            if "pricing_data" in result:
                pricing = result["pricing_data"]
                if "on_demand" in pricing:
                    print(f"      💰 On-Demand: ${pricing['on_demand'].get('monthly', 0):.2f}/month")
                if "savings_opportunities" in result:
                    opportunities = result["savings_opportunities"]
                    if opportunities:
                        print(f"      💡 Savings: ${opportunities[0].get('monthly_savings', 0):.2f}/month")
            
            elif "optimization_opportunities" in result:
                opportunities = result["optimization_opportunities"]
                total_savings = result.get("total_potential_monthly_savings", 0)
                print(f"      💡 Opportunities: {len(opportunities)}")
                print(f"      💰 Potential Savings: ${total_savings:.2f}/month")
            
            elif "security_findings" in result:
                findings = result["security_findings"]
                severity_summary = result.get("severity_summary", {})
                print(f"      🔒 Security Findings: {len(findings)}")
                print(f"      ⚠️  Critical: {severity_summary.get('critical', 0)}, High: {severity_summary.get('high', 0)}")
            
            elif "compliance_score" in result:
                score = result.get("overall_compliance_score", 0)
                print(f"      📊 Compliance Score: {score}%")
            
            elif "total_resources_found" in result:
                resources = result.get("total_resources_found", 0)
                accounts = result.get("accounts_scanned", 0)
                print(f"      🗂️  Resources Found: {resources} across {accounts} accounts")
            
            elif "pr_number" in result:
                pr_number = result.get("pr_number")
                pr_url = result.get("pr_url")
                print(f"      📝 PR #{pr_number}: {pr_url}")
                if "cost_analysis" in result:
                    savings = result["cost_analysis"].get("monthly_savings", 0)
                    print(f"      💰 Monthly Savings: ${savings:.2f}")
        
        else:
            error = result.get("error", "Unknown error")
            print(f"      ❌ Error: {error}")
    
    def run(self):
        """Main interactive loop"""
        print("\n💡 This tool tests AWS DevOps Agent capabilities")
        print("   Tests are safe and use mock data for demonstration")
        print("\n📝 Note: Real AWS operations require proper credentials")
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == "0":
                    print("\n👋 Exiting AWS DevOps Agent Testing")
                    break
                elif choice == "1":
                    self.test_cost_optimization()
                elif choice == "2":
                    self.test_iac_analysis()
                elif choice == "3":
                    self.test_compliance_security()
                elif choice == "4":
                    self.test_multi_account()
                elif choice == "5":
                    self.test_github_integration()
                elif choice == "6":
                    self.run_all_tests()
                else:
                    print("❌ Invalid option. Please select 0-6.")
                
                input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Exiting AWS DevOps Agent Testing")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("\n⏸️  Press Enter to continue...")


def main():
    """Main entry point"""
    try:
        tester = InteractiveAWSDevOpsTest()
        tester.run()
    except Exception as e:
        print(f"❌ Failed to start interactive testing: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())