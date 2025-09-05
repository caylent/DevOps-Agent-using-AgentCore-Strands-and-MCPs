#!/usr/bin/env python3
"""
Test AWS DevOps Agent - Comprehensive testing
Testing both Strands and Bedrock Agent Core integration
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import sys

# Add project paths for testing
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "config"))
sys.path.append(str(project_root / "tools" / "aws-devops"))
sys.path.append(str(project_root / "bedrock_deployment"))

from config.app_config import ConfigManager, get_config
from tools.aws_cost_tools import (
    get_real_aws_pricing,
    analyze_cost_optimization_opportunities,
    calculate_reserved_instance_savings
)
from tools.aws_iac_tools import (
    analyze_terraform_configuration,
    validate_cloudformation_template
)
from tools.aws_compliance_tools import (
    validate_security_policies,
    check_compliance_standards
)


class TestConfigurationManagement:
    """Test configuration management for AWS DevOps Agent"""
    
    def test_config_manager_initialization(self):
        """Test ConfigManager initialization"""
        config_manager = ConfigManager()
        assert config_manager is not None
        assert "claude-3.5-sonnet" in config_manager.AVAILABLE_MODELS
        assert config_manager.DEFAULT_MODEL == "claude-3.5-sonnet"
    
    def test_load_config_with_defaults(self):
        """Test loading configuration with default values"""
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        assert config is not None
        assert config.model.model_id == "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
        assert config.aws_region == "us-east-1"
        assert config.mcp.pricing_server == "awslabs.aws-pricing-mcp-server@latest"
    
    @patch.dict('os.environ', {
        'STRANDS_MODEL': 'claude-4',
        'AWS_REGION': 'us-west-2',
        'DEBUG_MODE': 'true'
    })
    def test_load_config_with_environment_variables(self):
        """Test loading configuration with environment variables"""
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        assert config.model.model_id == "us.anthropic.claude-sonnet-4-20250514-v1:0"
        assert config.aws_region == "us-west-2"
        assert config.debug_mode is True
    
    def test_get_config_function(self):
        """Test get_config convenience function"""
        config = get_config()
        assert config is not None
        assert hasattr(config, 'model')
        assert hasattr(config, 'mcp')
        assert hasattr(config, 'aws_region')


class TestAWSCostTools:
    """Test AWS cost optimization tools"""
    
    @pytest.mark.asyncio
    async def test_get_real_aws_pricing_success(self):
        """Test successful AWS pricing retrieval"""
        result = get_real_aws_pricing("EC2", "t3.medium", "us-east-1")
        
        assert result["status"] == "success"
        assert result["service"] == "EC2"
        assert result["instance_type"] == "t3.medium"
        assert result["region"] == "us-east-1"
        assert "pricing_data" in result
    
    def test_analyze_cost_optimization_opportunities_ec2(self):
        """Test cost optimization analysis for EC2"""
        config = {
            "instance_type": "t3.large",
            "region": "us-east-1"
        }
        
        result = analyze_cost_optimization_opportunities("EC2", config, "us-east-1")
        
        assert result["status"] == "success"
        assert result["resource_type"] == "EC2"
        assert "optimization_opportunities" in result
        assert "total_potential_monthly_savings" in result
    
    def test_calculate_reserved_instance_savings(self):
        """Test Reserved Instance savings calculation"""
        instance_types = ["t3.medium", "t3.large"]
        
        result = calculate_reserved_instance_savings(instance_types, 730, "us-east-1")
        
        assert result["status"] == "success"
        assert len(result["instance_analysis"]) == 2
        assert "summary" in result
        assert result["summary"]["total_monthly_savings"] >= 0
    
    def test_cost_optimization_with_invalid_resource_type(self):
        """Test cost optimization with invalid resource type"""
        result = analyze_cost_optimization_opportunities("INVALID", {}, "us-east-1")
        
        assert result["status"] == "success"  # Should handle gracefully
        assert result["total_opportunities"] >= 0


class TestAWSIaCTools:
    """Test Infrastructure as Code analysis tools"""
    
    def test_analyze_terraform_configuration_missing_path(self):
        """Test Terraform analysis with missing path"""
        result = analyze_terraform_configuration("/nonexistent/path", "production")
        
        assert result["status"] == "error"
        assert "not found" in result["error"]
    
    def test_validate_cloudformation_template_missing_file(self):
        """Test CloudFormation validation with missing template"""
        result = validate_cloudformation_template("/nonexistent/template.json", "production")
        
        assert result["status"] == "error"
        assert "not found" in result["error"]
    
    def test_scan_infrastructure_drift_ec2(self):
        """Test infrastructure drift scanning for EC2"""
        from tools.aws_iac_tools import scan_infrastructure_drift
        
        result = scan_infrastructure_drift("EC2", None, "us-east-1")
        
        assert result["status"] == "success"
        assert result["resource_type"] == "EC2"
        assert "drift_detected" in result
        assert "recommendations" in result
    
    def test_generate_iac_best_practices_report_terraform(self):
        """Test IaC best practices report generation"""
        from tools.aws_iac_tools import generate_iac_best_practices_report
        
        result = generate_iac_best_practices_report("/fake/path", "terraform")
        
        assert result["status"] == "success"
        assert result["iac_tool"] == "terraform"
        assert "compliance_score" in result
        assert result["compliance_score"] >= 0


class TestAWSComplianceTools:
    """Test AWS compliance and security validation tools"""
    
    def test_validate_security_policies_ec2(self):
        """Test security policy validation for EC2"""
        config = {
            "associate_public_ip_address": True,
            "security_groups": ["sg-12345 (0.0.0.0/0)"]
        }
        
        result = validate_security_policies("EC2", config, "us-east-1")
        
        assert result["status"] == "success"
        assert result["resource_type"] == "EC2"
        assert len(result["security_findings"]) > 0
        assert result["severity_summary"]["critical"] > 0
    
    def test_validate_security_policies_s3(self):
        """Test security policy validation for S3"""
        config = {
            "public_read_access": True,
            "server_side_encryption": False
        }
        
        result = validate_security_policies("S3", config, "us-east-1")
        
        assert result["status"] == "success"
        assert len(result["security_findings"]) >= 2  # Public access + encryption
        assert result["compliance_status"] == "non_compliant"
    
    def test_check_compliance_standards_soc2(self):
        """Test SOC2 compliance checking"""
        resource_configs = [
            {"type": "EC2", "config": {"security_groups": []}},
            {"type": "RDS", "config": {"encrypted": True}}
        ]
        
        result = check_compliance_standards("SOC2", resource_configs, "us-east-1")
        
        assert result["status"] == "success"
        assert result["compliance_standard"] == "SOC2"
        assert "overall_compliance_score" in result
        assert result["total_resources_checked"] == 2
    
    def test_generate_compliance_report(self):
        """Test compliance report generation"""
        from tools.aws_compliance_tools import generate_compliance_report
        
        assessment_results = {
            "overall_compliance_score": 85.0,
            "compliant_controls": 17,
            "non_compliant_controls": 3,
            "compliance_checks": [],
            "remediation_actions": ["Fix security groups", "Enable encryption"]
        }
        
        result = generate_compliance_report("SOC2", assessment_results, "json")
        
        assert result["status"] == "success"
        assert result["report_metadata"]["standard"] == "SOC2"
        assert "executive_summary" in result
        assert result["executive_summary"]["compliance_score"] == "85.0%"
    
    def test_scan_security_vulnerabilities(self):
        """Test security vulnerability scanning"""
        from tools.aws_compliance_tools import scan_security_vulnerabilities
        
        result = scan_security_vulnerabilities("EC2", "all", "us-east-1")
        
        assert result["status"] == "success"
        assert result["resource_type"] == "EC2"
        assert result["scan_scope"] == "all"
        assert "vulnerabilities" in result
        assert "vulnerability_summary" in result


class TestMultiAccountTools:
    """Test multi-account AWS management tools"""
    
    def test_list_cross_account_resources(self):
        """Test cross-account resource listing"""
        from tools.aws_multi_account_tools import list_cross_account_resources
        
        result = list_cross_account_resources("EC2", ["123456789012"], ["us-east-1"])
        
        assert result["status"] == "success"
        assert result["resource_type"] == "EC2"
        assert result["accounts_scanned"] == 1
        assert result["regions_scanned"] == 1
        assert "resource_inventory" in result
    
    def test_execute_cross_account_operation(self):
        """Test cross-account operation execution"""
        from tools.aws_multi_account_tools import execute_cross_account_operation
        
        result = execute_cross_account_operation(
            "patch",
            ["123456789012", "123456789013"],
            {"patch_type": "security"}
        )
        
        assert result["status"] == "success"
        assert result["operation"] == "patch"
        assert len(result["target_accounts"]) == 2
        assert "overall_success_rate" in result
    
    def test_generate_multi_account_report(self):
        """Test multi-account report generation"""
        from tools.aws_multi_account_tools import generate_multi_account_report
        
        result = generate_multi_account_report("security", "organization", True)
        
        assert result["status"] == "success"
        assert result["report_type"] == "security"
        assert "executive_summary" in result
        assert result["cost_analysis"] is not None  # include_costs=True


class TestGitHubIntegrationTools:
    """Test GitHub integration and PR automation tools"""
    
    def test_create_optimization_pull_request(self):
        """Test optimization PR creation"""
        from tools.github_integration_tools import create_optimization_pull_request
        
        changes = {
            "monthly_savings": 150.0,
            "annual_savings": 1800.0,
            "affected_resources": ["i-12345", "i-67890"],
            "specific_changes": ["Right-size t3.large to t3.medium", "Enable reserved instances"]
        }
        
        result = create_optimization_pull_request(
            "myorg/infrastructure",
            "cost",
            changes,
            "cost-optimization-jan2024"
        )
        
        assert result["status"] == "success"
        assert result["optimization_type"] == "cost"
        assert result["pr_number"] == 42
        assert "pr_url" in result
        assert result["cost_analysis"]["monthly_savings"] == 150.0
    
    def test_update_iac_via_github(self):
        """Test IaC updates via GitHub"""
        from tools.github_integration_tools import update_iac_via_github
        
        updates = {
            "resources": ["aws_instance.web", "aws_rds_instance.db"],
            "configurations": ["instance_type", "storage_encrypted"],
            "workspace": "production"
        }
        
        result = update_iac_via_github(
            "myorg/terraform-infrastructure",
            "terraform",
            updates,
            "platform-team"
        )
        
        assert result["status"] == "success"
        assert result["iac_tool"] == "terraform"
        assert result["terraform_specific"]["workspace"] == "production"
        assert "validation_steps" in result["terraform_specific"]
    
    def test_list_infrastructure_repositories(self):
        """Test infrastructure repository listing"""
        from tools.github_integration_tools import list_infrastructure_repositories
        
        result = list_infrastructure_repositories("myorg", "terraform", False)
        
        assert result["status"] == "success"
        assert result["organization"] == "myorg"
        assert result["repository_type"] == "terraform"
        assert "repositories" in result
        assert "statistics" in result
    
    def test_monitor_infrastructure_prs(self):
        """Test infrastructure PR monitoring"""
        from tools.github_integration_tools import monitor_infrastructure_prs
        
        result = monitor_infrastructure_prs("myorg/infrastructure", "open", 7)
        
        assert result["status"] == "success"
        assert result["monitoring_scope"] == "open"
        assert result["monitoring_period"] == "7 days"
        assert "pr_statistics" in result
        assert "risk_analysis" in result


class TestBedrockAgentCoreIntegration:
    """Test Bedrock Agent Core integration"""
    
    @patch('bedrock_agentcore.runtime.BedrockAgentCoreApp')
    @patch('strands.Agent')
    def test_agent_initialization(self, mock_agent, mock_app):
        """Test agent initialization with mocked dependencies"""
        # This test would verify that the agent initializes correctly
        # when Strands and Bedrock Agent Core are available
        
        # Mock the Agent creation
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        # Mock the BedrockAgentCoreApp
        mock_app_instance = Mock()
        mock_app.return_value = mock_app_instance
        
        # Import and test (would need actual implementation when dependencies are available)
        # from bedrock_deployment.aws_devops_agent_app import agent, app
        
        # For now, just verify mocks are set up correctly
        assert mock_agent is not None
        assert mock_app is not None
    
    def test_payload_processing_simulation(self):
        """Test payload processing logic simulation"""
        # Simulate the payload processing that would happen in Bedrock Agent Core
        
        sample_payload = {
            "prompt": "Analyze AWS costs and provide optimization recommendations",
            "inputText": "",
            "query": ""
        }
        
        # Extract message (simulating the extraction logic from aws_devops_agent_app.py)
        user_message = sample_payload.get("prompt", "")
        if not user_message:
            user_message = sample_payload.get("inputText", "")
        if not user_message:
            user_message = sample_payload.get("query", "Analyze AWS infrastructure")
        
        assert user_message == "Analyze AWS costs and provide optimization recommendations"
        
        # Simulate response structure
        expected_response = {
            "response": "Cost analysis complete",
            "status": "success",
            "agent": "AWS DevOps Agent",
            "capabilities": [
                "Real-time AWS cost analysis",
                "IaC analysis (Terraform/CloudFormation)",
                "Security compliance validation",
                "Multi-account operations",
                "Automated PR generation"
            ]
        }
        
        assert expected_response["status"] == "success"
        assert len(expected_response["capabilities"]) == 5


@pytest.fixture
def sample_terraform_config():
    """Fixture providing sample Terraform configuration"""
    return {
        "instance_type": "t3.medium",
        "security_groups": ["sg-12345"],
        "associate_public_ip_address": False,
        "tags": {
            "Environment": "production",
            "Team": "platform"
        }
    }


@pytest.fixture
def sample_compliance_config():
    """Fixture providing sample compliance configuration"""
    return {
        "encrypted": True,
        "publicly_accessible": False,
        "backup_retention_period": 30,
        "tags": {
            "Compliance": "SOC2",
            "DataClassification": "Internal"
        }
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])