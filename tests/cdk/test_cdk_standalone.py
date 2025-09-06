#!/usr/bin/env python3
"""
Standalone test for CDK analysis functionality
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import only the CDK analysis functions directly without going through __init__.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'aws_devops_agent', 'tools', 'aws_cdk'))

from cdk_analysis import (
    _analyze_cdk_project_structure,
    _find_cdk_source_files,
    _analyze_cdk_file,
    _analyze_synthesized_templates,
    _generate_stack_summary
)


def create_sample_cdk_project(project_path: str):
    """Create a sample CDK project for testing"""
    os.makedirs(project_path, exist_ok=True)
    
    # Create cdk.json
    cdk_config = {
        "version": "2.0.0",
        "language": "typescript",
        "app": "npx ts-node --prefer-ts-exts bin/app.ts",
        "context": {
            "@aws-cdk/aws-lambda:recognizeLayerVersion": True,
            "@aws-cdk/core:checkSecretUsage": True
        }
    }
    
    with open(os.path.join(project_path, "cdk.json"), 'w') as f:
        json.dump(cdk_config, f, indent=2)
    
    # Create bin/app.ts
    bin_dir = os.path.join(project_path, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    
    app_content = '''
import { App } from 'aws-cdk-lib';
import { SampleStack } from '../lib/sample-stack';

const app = new App();
new SampleStack(app, 'SampleStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT || '123456789012',
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1',
  },
});
'''
    
    with open(os.path.join(bin_dir, "app.ts"), 'w') as f:
        f.write(app_content)
    
    # Create lib/sample-stack.ts
    lib_dir = os.path.join(project_path, "lib")
    os.makedirs(lib_dir, exist_ok=True)
    
    stack_content = '''
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';

export class SampleStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create VPC
    const vpc = new ec2.Vpc(this, 'SampleVPC', {
      maxAzs: 2,
      natGateways: 1,
    });

    // Create security group with overly permissive rule (for testing)
    const securityGroup = new ec2.SecurityGroup(this, 'SampleSecurityGroup', {
      vpc,
      description: 'Sample security group',
    });
    
    securityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(22),
      'SSH access from anywhere' // This is a security issue for testing
    );

    // Create EC2 instance
    new ec2.Instance(this, 'WebServer', {
      vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE), // Large instance for cost testing
      machineImage: ec2.MachineImage.latestAmazonLinux(),
      securityGroup,
    });

    // Create RDS instance
    new rds.DatabaseInstance(this, 'Database', {
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13_7,
      }),
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
      },
    });
  }
}
'''
    
    with open(os.path.join(lib_dir, "sample-stack.ts"), 'w') as f:
        f.write(stack_content)


def test_cdk_helper_functions():
    """Test CDK helper functions"""
    print("🧪 Testing CDK Helper Functions")
    print("=" * 50)
    
    # Create temporary directory for test project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = os.path.join(temp_dir, "sample-cdk-project")
        create_sample_cdk_project(project_path)
        
        print(f"📁 Created sample CDK project at: {project_path}")
        print()
        
        # Test 1: Analyze project structure
        print("1️⃣ Analyzing CDK project structure...")
        project_info = _analyze_cdk_project_structure(project_path)
        
        print("✅ Project structure analysis:")
        print(f"   📦 CDK Version: {project_info['cdk_version']}")
        print(f"   🔤 Language: {project_info['language']}")
        print(f"   📊 Stacks: {project_info['stacks_count']}")
        print(f"   🧩 Constructs: {project_info['constructs_count']}")
        print()
        
        # Test 2: Find CDK source files
        print("2️⃣ Finding CDK source files...")
        cdk_files = _find_cdk_source_files(project_path)
        
        print(f"✅ Found {len(cdk_files)} CDK source files:")
        for file_path in cdk_files:
            print(f"   📄 {os.path.basename(file_path)}")
        print()
        
        # Test 3: Analyze individual CDK files
        print("3️⃣ Analyzing individual CDK files...")
        for cdk_file in cdk_files[:2]:  # Analyze first 2 files
            print(f"   🔍 Analyzing {os.path.basename(cdk_file)}...")
            file_analysis = _analyze_cdk_file(cdk_file, "production")
            
            findings = file_analysis.get("findings", [])
            cost_ops = file_analysis.get("cost_optimizations", [])
            security_issues = file_analysis.get("security_issues", [])
            best_practices = file_analysis.get("best_practices", [])
            
            print(f"      📊 Findings: {len(findings)}")
            print(f"      💰 Cost optimizations: {len(cost_ops)}")
            print(f"      🔒 Security issues: {len(security_issues)}")
            print(f"      📋 Best practices: {len(best_practices)}")
            
            # Show specific findings
            if cost_ops:
                for opp in cost_ops[:1]:  # Show first cost optimization
                    print(f"         💡 {opp.get('issue', 'N/A')}")
                    print(f"         💵 Potential savings: ${opp.get('monthly_savings', 0):.2f}/month")
            
            if security_issues:
                for issue in security_issues[:1]:  # Show first security issue
                    print(f"         ⚠️  {issue.get('issue', 'N/A')} (Severity: {issue.get('severity', 'N/A')})")
            
            if best_practices:
                for practice in best_practices[:1]:  # Show first best practice
                    print(f"         📋 {practice.get('issue', 'N/A')}")
            
            print()
        
        # Test 4: Create mock synthesized templates
        print("4️⃣ Testing synthesized template analysis...")
        cdk_out_path = os.path.join(temp_dir, "cdk.out")
        os.makedirs(cdk_out_path, exist_ok=True)
        
        # Create mock CloudFormation template
        template_content = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "Sample CDK Stack",
            "Resources": {
                "SampleVPC": {
                    "Type": "AWS::EC2::VPC",
                    "Properties": {
                        "CidrBlock": "10.0.0.0/16",
                        "EnableDnsHostnames": True,
                        "EnableDnsSupport": True,
                        "Tags": [
                            {
                                "Key": "Name",
                                "Value": "SampleVPC"
                            }
                        ]
                    }
                },
                "WebServer": {
                    "Type": "AWS::EC2::Instance",
                    "Properties": {
                        "InstanceType": "t3.large",
                        "ImageId": "ami-12345678",
                        "Tags": [
                            {
                                "Key": "Name",
                                "Value": "WebServer"
                            }
                        ]
                    }
                }
            },
            "Outputs": {
                "VPCId": {
                    "Value": {"Ref": "SampleVPC"},
                    "Description": "VPC ID"
                }
            }
        }
        
        with open(os.path.join(cdk_out_path, "SampleStack.template.json"), 'w') as f:
            json.dump(template_content, f)
        
        # Analyze synthesized templates
        templates = _analyze_synthesized_templates(cdk_out_path)
        stack_summary = _generate_stack_summary(templates)
        
        print("✅ Synthesized template analysis:")
        print(f"   📊 Total stacks: {stack_summary['total_stacks']}")
        print(f"   🏗️  Total resources: {stack_summary['total_resources']}")
        print(f"   📋 Total parameters: {stack_summary['total_parameters']}")
        print(f"   📤 Total outputs: {stack_summary['total_outputs']}")
        print(f"   📈 Avg resources per stack: {stack_summary['average_resources_per_stack']:.1f}")
        print()
        
        print("🎉 CDK helper functions test completed!")


if __name__ == "__main__":
    test_cdk_helper_functions()
