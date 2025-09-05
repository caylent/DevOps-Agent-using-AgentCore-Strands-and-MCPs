#!/usr/bin/env python3
"""
Setup and Configuration Script for AWS MCP Servers
Installs and configures the official AWS MCP servers for the DevOps agent
"""

import subprocess
import sys
import os
from typing import List, Dict, Any


class MCPServerSetup:
    """Setup manager for AWS MCP servers"""
    
    def __init__(self):
        self.servers = [
            {
                "name": "AWS Cost Explorer MCP Server",
                "package": "awslabs.cost-explorer-mcp-server@latest",
                "description": "Real AWS cost analysis and reporting"
            },
            {
                "name": "AWS CloudWatch MCP Server", 
                "package": "awslabs.cloudwatch-mcp-server@latest",
                "description": "Metrics, alarms, and logs analysis"
            },
            {
                "name": "AWS Pricing MCP Server",
                "package": "awslabs.aws-pricing-mcp-server@latest", 
                "description": "Pre-deployment cost estimation"
            },
            {
                "name": "AWS Billing and Cost Management MCP Server",
                "package": "awslabs.billing-cost-management-mcp-server@latest",
                "description": "Comprehensive cost management and optimization"
            }
        ]
    
    def check_prerequisites(self) -> bool:
        """Check if required tools are installed"""
        print("🔍 Checking prerequisites...")
        
        # Check if uvx is available
        try:
            result = subprocess.run(["uvx", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ uvx is available: {result.stdout.strip()}")
            else:
                print("❌ uvx not found. Please install uv first: pip install uv")
                return False
        except FileNotFoundError:
            print("❌ uvx not found. Please install uv first: pip install uv")
            return False
        
        # Check AWS credentials
        aws_profile = os.getenv("AWS_PROFILE", "default")
        aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        
        print(f"✅ AWS Profile: {aws_profile}")
        print(f"✅ AWS Region: {aws_region}")
        
        # Test AWS credentials
        try:
            result = subprocess.run(["aws", "sts", "get-caller-identity"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ AWS credentials are configured")
            else:
                print("⚠️  Warning: AWS credentials test failed")
                print(f"   Error: {result.stderr}")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("⚠️  Warning: Could not test AWS credentials (aws CLI not found or timeout)")
        
        return True
    
    def install_mcp_servers(self) -> Dict[str, bool]:
        """Install all AWS MCP servers"""
        print("\n🚀 Installing AWS MCP Servers...")
        
        installation_results = {}
        
        for server in self.servers:
            print(f"\n📦 Installing {server['name']}...")
            print(f"   Package: {server['package']}")
            print(f"   Description: {server['description']}")
            
            try:
                # Install the MCP server using uvx
                result = subprocess.run(
                    ["uvx", "install", server['package']], 
                    capture_output=True, 
                    text=True, 
                    timeout=120  # 2 minutes timeout
                )
                
                if result.returncode == 0:
                    print(f"   ✅ Successfully installed {server['name']}")
                    installation_results[server['name']] = True
                else:
                    print(f"   ❌ Failed to install {server['name']}")
                    print(f"   Error: {result.stderr}")
                    installation_results[server['name']] = False
                    
            except subprocess.TimeoutExpired:
                print(f"   ⏰ Installation timeout for {server['name']}")
                installation_results[server['name']] = False
            except Exception as e:
                print(f"   ❌ Exception installing {server['name']}: {e}")
                installation_results[server['name']] = False
        
        return installation_results
    
    def test_mcp_servers(self) -> Dict[str, bool]:
        """Test connectivity to installed MCP servers"""
        print("\n🧪 Testing MCP Server Connectivity...")
        
        test_results = {}
        
        # Test Cost Explorer MCP Server
        print(f"\n🔬 Testing AWS Cost Explorer MCP Server...")
        try:
            result = subprocess.run(
                ["uvx", "awslabs.cost-explorer-mcp-server@latest", "--help"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("   ✅ Cost Explorer MCP Server responding")
                test_results["Cost Explorer"] = True
            else:
                print("   ❌ Cost Explorer MCP Server not responding")
                test_results["Cost Explorer"] = False
                
        except Exception as e:
            print(f"   ❌ Error testing Cost Explorer: {e}")
            test_results["Cost Explorer"] = False
        
        # Test CloudWatch MCP Server
        print(f"\n🔬 Testing AWS CloudWatch MCP Server...")
        try:
            result = subprocess.run(
                ["uvx", "awslabs.cloudwatch-mcp-server@latest", "--help"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("   ✅ CloudWatch MCP Server responding")
                test_results["CloudWatch"] = True
            else:
                print("   ❌ CloudWatch MCP Server not responding")
                test_results["CloudWatch"] = False
                
        except Exception as e:
            print(f"   ❌ Error testing CloudWatch: {e}")
            test_results["CloudWatch"] = False
        
        return test_results
    
    def generate_usage_guide(self) -> str:
        """Generate usage guide for the MCP servers"""
        guide = """
╔══════════════════════════════════════════════════════════════════╗
║                    AWS MCP SERVERS USAGE GUIDE                   ║
╚══════════════════════════════════════════════════════════════════╝

📋 INSTALLED MCP SERVERS:

1️⃣  AWS Cost Explorer MCP Server
   • Command: uvx awslabs.cost-explorer-mcp-server@latest
   • Features: Real cost analysis, forecasting, comparisons
   • Tools: get_cost_and_usage, get_cost_forecast, get_dimension_values

2️⃣  AWS CloudWatch MCP Server  
   • Command: uvx awslabs.cloudwatch-mcp-server@latest
   • Features: Metrics analysis, alarms, log insights
   • Tools: get_metric_data, get_active_alarms, execute_log_insights_query

3️⃣  AWS Pricing MCP Server
   • Command: uvx awslabs.aws-pricing-mcp-server@latest
   • Features: Pre-deployment cost estimation
   • Tools: get_pricing, get_services

4️⃣  AWS Billing and Cost Management MCP Server
   • Command: uvx awslabs.billing-cost-management-mcp-server@latest
   • Features: Comprehensive cost management
   • Tools: Cost optimization, budgets, anomaly detection

🔧 CONFIGURATION REQUIREMENTS:

• AWS Credentials: Ensure AWS CLI is configured with proper permissions
• IAM Permissions Required:
  - ce:GetCostAndUsage (Cost Explorer)
  - ce:GetForecast (Cost Explorer)
  - cloudwatch:GetMetricData (CloudWatch)
  - logs:StartQuery, logs:GetQueryResults (CloudWatch Logs)
  - pricing:GetProducts (Pricing API)

⚡ USAGE IN AWS DEVOPS AGENT:

The MCP servers are automatically integrated into the AWS DevOps Agent.
Run: python aws_devops_agent_v2.py --mode interactive

Example queries:
• "Show me AWS costs for the last 30 days"
• "Get CloudWatch alarms for EC2 instances"  
• "Forecast my AWS costs for next month"
• "Analyze errors in my application logs"

💡 TROUBLESHOOTING:

• Permission Errors: Check AWS IAM permissions
• Timeout Issues: Increase timeout values for large queries
• Installation Problems: Run 'uvx install package@latest' manually

📚 For more information: https://awslabs.github.io/mcp/
"""
        return guide
    
    def run_full_setup(self):
        """Run complete MCP servers setup"""
        print("🎯 AWS MCP Servers Setup Starting...")
        print("=" * 70)
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("\n❌ Prerequisites check failed. Please fix issues and retry.")
            sys.exit(1)
        
        # Install MCP servers
        installation_results = self.install_mcp_servers()
        
        # Test MCP servers
        test_results = self.test_mcp_servers()
        
        # Generate summary
        print("\n" + "=" * 70)
        print("📊 SETUP SUMMARY")
        print("=" * 70)
        
        successful_installs = sum(1 for result in installation_results.values() if result)
        successful_tests = sum(1 for result in test_results.values() if result)
        
        print(f"✅ Installed MCP Servers: {successful_installs}/{len(self.servers)}")
        print(f"✅ Tested MCP Servers: {successful_tests}/{len(test_results)}")
        
        if successful_installs > 0:
            print("\n🎉 Setup completed successfully!")
            print(self.generate_usage_guide())
        else:
            print("\n❌ Setup failed. Please check error messages above.")
            sys.exit(1)


def main():
    """Main entry point"""
    setup = MCPServerSetup()
    setup.run_full_setup()


if __name__ == "__main__":
    main()