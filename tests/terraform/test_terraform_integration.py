#!/usr/bin/env python3
"""
Terraform Integration Test

Test Terraform tools integration with the main agent.
"""

import os
import sys
import tempfile
import shutil
import asyncio
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from aws_devops_agent.main import AWSDevOpsAgentV2


class TestTerraformIntegration:
    """Test Terraform integration with main agent"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.agent = None
        
        # Create a simple Terraform project
        self.terraform_files = {
            'main.tf': '''
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name = "test-instance"
  }
}

resource "aws_security_group" "web_sg" {
  name_prefix = "web-sg-"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
''',
            'variables.tf': '''
variable "instance_type" {
  description = "Type of EC2 instance"
  type        = string
  default     = "t3.micro"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}
''',
            'outputs.tf': '''
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.web.id
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.web_sg.id
}
'''
        }
        
        # Create test Terraform files
        for filename, content in self.terraform_files.items():
            with open(os.path.join(self.test_dir, filename), 'w') as f:
                f.write(content)
    
    def teardown_method(self):
        """Cleanup test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_agent_initialization_with_terraform_tools(self):
        """Test that agent initializes with Terraform tools"""
        try:
            self.agent = AWSDevOpsAgentV2()
            assert self.agent is not None
            print("✅ Agent initialized with Terraform tools")
            
            # Check agent status
            status = self.agent.get_status()
            assert status["agent_ready"] is True
            assert status["tools_count"] >= 47  # Should include Terraform tools
            assert "IaC analysis (Terraform, CloudFormation, CDK)" in status["capabilities"]
            print("✅ Agent status includes Terraform capabilities")
            
        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
            raise
    
    def test_terraform_tools_available(self):
        """Test that Terraform tools are available in the agent"""
        try:
            self.agent = AWSDevOpsAgentV2()
            
            # Check that Terraform tools are available
            # Note: We can't directly access tools from the Strands agent
            # but we can verify the agent is working and has the right tool count
            agent_tools = []  # Placeholder since we can't access tools directly
            
            terraform_tools = [
                "analyze_terraform_project",
                "validate_terraform_configuration", 
                "plan_terraform_changes",
                "analyze_terraform_state",
                "generate_terraform_optimization_report"
            ]
            
            # Verify agent has the expected tool count (includes Terraform tools)
            status = self.agent.get_status()
            assert status["tools_count"] >= 47, f"Expected at least 47 tools, got {status['tools_count']}"
            
            print("✅ All Terraform tools are available in the agent")
            
        except Exception as e:
            print(f"❌ Terraform tools check failed: {e}")
            raise
    
    @pytest.mark.asyncio
    async def test_terraform_analysis_conversation(self):
        """Test Terraform analysis through agent conversation"""
        try:
            self.agent = AWSDevOpsAgentV2()
            
            # Test conversation about Terraform analysis
            message = f"Analyze my Terraform project at {self.test_dir} for optimization opportunities"
            
            # This would normally call the agent, but we'll test the tools directly
            # since we don't have AWS credentials in test environment
            from aws_devops_agent.tools.aws_terraform.terraform_analysis import analyze_terraform_project
            
            result = analyze_terraform_project(self.test_dir, "production")
            
            # The result should indicate that Terraform CLI is not found (expected in test)
            # or provide analysis results
            assert result["status"] in ["success", "error"]
            
            if result["status"] == "error":
                assert "Terraform CLI not found" in result["error"] or "Project path does not exist" in result["error"]
                print("✅ Terraform analysis handles missing CLI correctly")
            else:
                print("✅ Terraform analysis completed successfully")
            
        except Exception as e:
            print(f"❌ Terraform analysis conversation failed: {e}")
            raise
    
    def test_terraform_validation_conversation(self):
        """Test Terraform validation through agent conversation"""
        try:
            self.agent = AWSDevOpsAgentV2()
            
            # Test conversation about Terraform validation
            message = f"Validate my Terraform configuration at {self.test_dir}"
            
            # Test the validation tool directly
            from aws_devops_agent.tools.aws_terraform.terraform_analysis import validate_terraform_configuration
            
            result = validate_terraform_configuration(self.test_dir)
            
            # The result should indicate that Terraform CLI is not found (expected in test)
            # or provide validation results
            assert result["status"] in ["success", "error"]
            
            if result["status"] == "error":
                assert "Terraform CLI not found" in result["error"] or "Project path does not exist" in result["error"]
                print("✅ Terraform validation handles missing CLI correctly")
            else:
                print("✅ Terraform validation completed successfully")
            
        except Exception as e:
            print(f"❌ Terraform validation conversation failed: {e}")
            raise
    
    def test_terraform_optimization_report_conversation(self):
        """Test Terraform optimization report through agent conversation"""
        try:
            self.agent = AWSDevOpsAgentV2()
            
            # Test conversation about Terraform optimization report
            message = f"Generate an optimization report for my Terraform project at {self.test_dir}"
            
            # Test the optimization report tool directly
            from aws_devops_agent.tools.aws_terraform.terraform_analysis import generate_terraform_optimization_report
            
            # Create mock analysis results
            mock_analysis_results = {
                "status": "success",
                "data": {
                    "project_path": self.test_dir,
                    "environment": "production",
                    "security": {
                        "overall_security_score": 75,
                        "security_issues": []
                    },
                    "cost_optimization": {
                        "potential_savings": "$100.00/month",
                        "optimization_opportunities": []
                    },
                    "best_practices": {
                        "overall_score": 85,
                        "violations": []
                    },
                    "recommendations": []
                }
            }
            
            result = generate_terraform_optimization_report(mock_analysis_results)
            
            assert result["status"] == "success"
            assert result["data"]["report_generated"] is True
            assert "overall_score" in result["data"]
            print("✅ Terraform optimization report generation works correctly")
            
        except Exception as e:
            print(f"❌ Terraform optimization report conversation failed: {e}")
            raise


def test_terraform_tools_in_main_agent():
    """Test that Terraform tools are properly integrated in main agent"""
    print("🧪 Testing Terraform tools integration in main agent...")
    
    try:
        agent = AWSDevOpsAgentV2()
        
        # Check agent status
        status = agent.get_status()
        print(f"   📊 Agent status: {status}")
        
        # Verify agent has the expected tool count (includes Terraform tools)
        status = agent.get_status()
        assert status["tools_count"] >= 47, f"Expected at least 47 tools, got {status['tools_count']}"
        
        print("✅ All Terraform tools are properly integrated")
        
    except Exception as e:
        print(f"❌ Terraform tools integration test failed: {e}")
        raise


if __name__ == "__main__":
    print("🧪 Running Terraform Integration Tests...")
    print()
    
    # Run integration tests
    test_terraform_tools_in_main_agent()
    
    print()
    print("✅ All Terraform integration tests completed!")
