"""
Test CDK Analysis Tools
"""

import os
import tempfile
import json
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Import the CDK tools
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aws_devops_agent.tools.aws_cdk.cdk_analysis import (
    analyze_cdk_project,
    synthesize_cdk_project,
    analyze_cdk_synthesized_output,
    generate_cdk_optimization_report
)


class TestCDKAnalysis:
    """Test CDK analysis functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.cdk_project_path = os.path.join(self.temp_dir, "test-cdk-project")
        os.makedirs(self.cdk_project_path, exist_ok=True)
        
        # Create a mock CDK project
        self._create_mock_cdk_project()
    
    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_mock_cdk_project(self):
        """Create a mock CDK project for testing"""
        # Create cdk.json
        cdk_config = {
            "version": "2.0.0",
            "language": "typescript",
            "app": "npx ts-node --prefer-ts-exts bin/app.ts",
            "watch": {
                "include": ["**"],
                "exclude": ["README.md", "cdk*.json", "**/*.d.ts", "**/*.js", "tsconfig.json", "package*.json", "yarn.lock", "node_modules", "test"]
            },
            "context": {
                "@aws-cdk/aws-lambda:recognizeLayerVersion": True,
                "@aws-cdk/core:checkSecretUsage": True,
                "@aws-cdk/core:target-partitions": ["aws", "aws-cn"],
                "@aws-cdk-containers/ecs-service-extensions:enableDefaultLogDriver": True,
                "@aws-cdk/aws-ec2:uniqueImdsv2TemplateName": True,
                "@aws-cdk/aws-ecs:arnFormat": "arn",
                "@aws-cdk/aws-iam:minimizePolicies": True,
                "@aws-cdk/core:validateSnapshotRemovalPolicy": True,
                "@aws-cdk/aws-codepipeline:crossAccountKeyAliasStackSafeResourceName": True,
                "@aws-cdk/aws-s3:createDefaultLoggingPolicy": True,
                "@aws-cdk/aws-sns-subscriptions:restrictSqsDescryption": True,
                "@aws-cdk/aws-apigateway:disableCloudWatchRole": True,
                "@aws-cdk/core:enablePartitionLiterals": True,
                "@aws-cdk/aws-events:eventsTargetQueueSameAccount": True,
                "@aws-cdk/aws-iam:standardizedServicePrincipals": True,
                "@aws-cdk/aws-ecs:disableExplicitDeploymentControllerForCircuitBreaker": True,
                "@aws-cdk/aws-iam:importedRoleStackSafeDefaultPolicyName": True,
                "@aws-cdk/aws-s3:serverAccessLogsUseBucketPolicy": True,
                "@aws-cdk/aws-route53-patters:useCertificate": True,
                "@aws-cdk/customresources:installLatestAwsSdkDefault": False,
                "@aws-cdk/aws-rds:databaseProxyUniqueResourceName": True,
                "@aws-cdk/aws-codedeploy:removeAlarmsFromDeploymentGroup": True,
                "@aws-cdk/aws-apigateway:authorizerChangeDeploymentLogicalId": True,
                "@aws-cdk/aws-ec2:launchTemplateDefaultUserData": True,
                "@aws-cdk/aws-secretsmanager:useAttachedSecretResourcePolicyForSecretTargetAttachments": True,
                "@aws-cdk/aws-redshift:columnId": True,
                "@aws-cdk/aws-stepfunctions-tasks:enableLogging": True,
                "@aws-cdk/aws-ec2:restrictDefaultSecurityGroup": True,
                "@aws-cdk/aws-apigateway:requestValidatorUniqueId": True,
                "@aws-cdk/aws-kms:aliasNameRef": True,
                "@aws-cdk/aws-autoscaling:generateLaunchTemplateInsteadOfLaunchConfig": True,
                "@aws-cdk/core:includePrefixInUniqueNameGeneration": True,
                "@aws-cdk/aws-efs:denyAnonymousAccess": True,
                "@aws-cdk/aws-opensearchservice:enableLogging": True,
                "@aws-cdk/aws-lambda:useLatestRuntimeVersion": True,
                "@aws-cdk/aws-lambda:recognizeVersionProps": True,
                "@aws-cdk/aws-cloudfront:defaultSecurityPolicyTLSv1.2_2021": True,
                "@aws-cdk-containers/ecs-service-extensions:enableLogging": True,
                "@aws-cdk/aws-ec2:ebsDefaultGp3Volume": True,
                "@aws-cdk/aws-ecs:removeDefaultDeploymentAlarm": True
            }
        }
        
        with open(os.path.join(self.cdk_project_path, "cdk.json"), 'w') as f:
            json.dump(cdk_config, f, indent=2)
        
        # Create a mock TypeScript CDK app
        bin_dir = os.path.join(self.cdk_project_path, "bin")
        os.makedirs(bin_dir, exist_ok=True)
        
        app_content = '''
import { App } from 'aws-cdk-lib';
import { TestStack } from '../lib/test-stack';

const app = new App();
new TestStack(app, 'TestStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION,
  },
});
'''
        
        with open(os.path.join(bin_dir, "app.ts"), 'w') as f:
            f.write(app_content)
        
        # Create lib directory and stack
        lib_dir = os.path.join(self.cdk_project_path, "lib")
        os.makedirs(lib_dir, exist_ok=True)
        
        stack_content = '''
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class TestStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create VPC
    const vpc = new ec2.Vpc(this, 'TestVPC', {
      maxAzs: 2,
    });

    // Create EC2 instance
    new ec2.Instance(this, 'TestInstance', {
      vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
      machineImage: ec2.MachineImage.latestAmazonLinux(),
    });
  }
}
'''
        
        with open(os.path.join(lib_dir, "test-stack.ts"), 'w') as f:
            f.write(stack_content)
    
    def test_analyze_cdk_project_success(self):
        """Test successful CDK project analysis"""
        result = analyze_cdk_project(self.cdk_project_path, "production")
        
        assert result["status"] == "success"
        assert result["project_path"] == self.cdk_project_path
        assert result["environment"] == "production"
        assert "project_info" in result
        assert "findings" in result
        assert "recommendations" in result
        assert "summary" in result
    
    def test_analyze_cdk_project_invalid_path(self):
        """Test CDK project analysis with invalid path"""
        result = analyze_cdk_project("/invalid/path", "production")
        
        assert result["status"] == "error"
        assert "not found" in result["error"]
    
    def test_analyze_cdk_project_not_cdk(self):
        """Test CDK project analysis on non-CDK directory"""
        non_cdk_dir = os.path.join(self.temp_dir, "not-cdk")
        os.makedirs(non_cdk_dir, exist_ok=True)
        
        result = analyze_cdk_project(non_cdk_dir, "production")
        
        assert result["status"] == "error"
        assert "Not a valid CDK project" in result["error"]
    
    @patch('subprocess.run')
    def test_synthesize_cdk_project_success(self, mock_run):
        """Test successful CDK synthesis"""
        # Mock successful CDK synth
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Successfully synthesized"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Create mock cdk.out directory
        cdk_out_path = os.path.join(self.cdk_project_path, "cdk.out")
        os.makedirs(cdk_out_path, exist_ok=True)
        
        # Create mock template
        template_content = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {
                "TestVPC": {
                    "Type": "AWS::EC2::VPC",
                    "Properties": {
                        "CidrBlock": "10.0.0.0/16"
                    }
                }
            }
        }
        
        with open(os.path.join(cdk_out_path, "TestStack.template.json"), 'w') as f:
            json.dump(template_content, f)
        
        result = synthesize_cdk_project(self.cdk_project_path)
        
        assert result["status"] == "success"
        assert result["project_path"] == self.cdk_project_path
        assert "generated_templates" in result
        assert "stack_summary" in result
    
    @patch('subprocess.run')
    def test_synthesize_cdk_project_failure(self, mock_run):
        """Test CDK synthesis failure"""
        # Mock failed CDK synth
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "CDK synthesis failed"
        mock_run.return_value = mock_result
        
        result = synthesize_cdk_project(self.cdk_project_path)
        
        assert result["status"] == "error"
        assert "CDK synthesis failed" in result["error"]
    
    def test_analyze_cdk_synthesized_output_success(self):
        """Test analysis of synthesized CDK output"""
        # Create mock cdk.out directory with templates
        cdk_out_path = os.path.join(self.temp_dir, "cdk.out")
        os.makedirs(cdk_out_path, exist_ok=True)
        
        # Create mock template
        template_content = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {
                "TestInstance": {
                    "Type": "AWS::EC2::Instance",
                    "Properties": {
                        "InstanceType": "t3.medium",
                        "ImageId": "ami-12345678"
                    }
                }
            }
        }
        
        with open(os.path.join(cdk_out_path, "TestStack.template.json"), 'w') as f:
            json.dump(template_content, f)
        
        result = analyze_cdk_synthesized_output(cdk_out_path)
        
        assert result["status"] == "success"
        assert result["cdk_output_path"] == cdk_out_path
        assert "templates_analyzed" in result
        assert "cost_analysis" in result
        assert "security_analysis" in result
    
    def test_analyze_cdk_synthesized_output_invalid_path(self):
        """Test analysis with invalid CDK output path"""
        result = analyze_cdk_synthesized_output("/invalid/path")
        
        assert result["status"] == "error"
        assert "not found" in result["error"]
    
    @patch('aws_devops_agent.tools.aws_cdk.cdk_analysis.synthesize_cdk_project')
    @patch('aws_devops_agent.tools.aws_cdk.cdk_analysis.analyze_cdk_synthesized_output')
    def test_generate_cdk_optimization_report_success(self, mock_analyze, mock_synth):
        """Test successful CDK optimization report generation"""
        # Mock successful synthesis
        mock_synth.return_value = {
            "status": "success",
            "cdk_output_path": "/mock/cdk.out",
            "generated_templates": []
        }
        
        # Mock successful analysis
        mock_analyze.return_value = {
            "status": "success",
            "templates_analyzed": [],
            "cost_analysis": {"total_estimated_monthly_cost": 100},
            "security_analysis": {"total_security_findings": 0}
        }
        
        result = generate_cdk_optimization_report(self.cdk_project_path, "production")
        
        assert result["status"] == "success"
        assert result["project_path"] == self.cdk_project_path
        assert result["environment"] == "production"
        assert "executive_summary" in result
        assert "cost_optimization" in result
        assert "security_recommendations" in result
        assert "implementation_roadmap" in result
    
    @patch('aws_devops_agent.tools.aws_cdk.cdk_analysis.synthesize_cdk_project')
    def test_generate_cdk_optimization_report_synthesis_failure(self, mock_synth):
        """Test CDK optimization report generation with synthesis failure"""
        # Mock failed synthesis
        mock_synth.return_value = {
            "status": "error",
            "error": "Synthesis failed"
        }
        
        result = generate_cdk_optimization_report(self.cdk_project_path, "production")
        
        assert result["status"] == "error"
        assert "Synthesis failed" in result["error"]


if __name__ == "__main__":
    pytest.main([__file__])
