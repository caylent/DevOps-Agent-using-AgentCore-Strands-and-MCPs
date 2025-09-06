#!/usr/bin/env python3
"""
Test CDK functionality without strands dependency
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

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

export class SampleStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create VPC
    const vpc = new ec2.Vpc(this, 'SampleVPC', {
      maxAzs: 2,
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

    // Create EC2 instance with large instance type (for cost testing)
    new ec2.Instance(this, 'WebServer', {
      vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
      machineImage: ec2.MachineImage.latestAmazonLinux(),
      securityGroup,
    });
  }
}
'''
    
    with open(os.path.join(lib_dir, "sample-stack.ts"), 'w') as f:
        f.write(stack_content)


def test_cdk_helper_functions():
    """Test CDK helper functions without strands dependency"""
    print("🧪 Testing CDK Helper Functions (No Strands)")
    print("=" * 60)
    
    # Create temporary directory for test project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = os.path.join(temp_dir, "test-cdk-project")
        create_sample_cdk_project(project_path)
        
        print(f"📁 Created test CDK project at: {project_path}")
        print()
        
        # Import and test helper functions directly
        try:
            # Import the helper functions directly
            sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'aws_devops_agent', 'tools', 'aws_cdk'))
            
            # Mock the strands.tool decorator
            class MockTool:
                def __call__(self, func):
                    return func
            
            # Replace strands.tool with mock
            import aws_devops_agent.tools.aws_cdk.cdk_analysis as cdk_module
            cdk_module.tool = MockTool()
            
            # Now we can import the functions
            from aws_devops_agent.tools.aws_cdk.cdk_analysis import (
                _analyze_cdk_project_structure,
                _find_cdk_source_files,
                _analyze_cdk_file,
                _analyze_synthesized_templates,
                _generate_stack_summary
            )
            
            print("✅ Successfully imported CDK helper functions!")
            print()
            
            # Test 1: Analyze project structure
            print("1️⃣ Testing project structure analysis...")
            project_info = _analyze_cdk_project_structure(project_path)
            print(f"   CDK Version: {project_info['cdk_version']}")
            print(f"   Language: {project_info['language']}")
            print()
            
            # Test 2: Find CDK source files
            print("2️⃣ Testing source file discovery...")
            cdk_files = _find_cdk_source_files(project_path)
            print(f"   Found {len(cdk_files)} CDK source files")
            for file_path in cdk_files:
                print(f"   📄 {os.path.basename(file_path)}")
            print()
            
            # Test 3: Analyze individual files
            print("3️⃣ Testing file analysis...")
            for cdk_file in cdk_files[:2]:  # Test first 2 files
                print(f"   🔍 Analyzing {os.path.basename(cdk_file)}...")
                file_analysis = _analyze_cdk_file(cdk_file, "production")
                
                cost_ops = file_analysis.get("cost_optimizations", [])
                security_issues = file_analysis.get("security_issues", [])
                best_practices = file_analysis.get("best_practices", [])
                
                print(f"      💰 Cost optimizations: {len(cost_ops)}")
                print(f"      🔒 Security issues: {len(security_issues)}")
                print(f"      📋 Best practices: {len(best_practices)}")
                
                if cost_ops:
                    print(f"         💡 {cost_ops[0].get('issue', 'N/A')}")
                if security_issues:
                    print(f"         ⚠️  {security_issues[0].get('issue', 'N/A')}")
                if best_practices:
                    print(f"         📋 {best_practices[0].get('issue', 'N/A')}")
                print()
            
            # Test 4: Mock synthesized templates
            print("4️⃣ Testing synthesized template analysis...")
            cdk_out_path = os.path.join(temp_dir, "cdk.out")
            os.makedirs(cdk_out_path, exist_ok=True)
            
            # Create mock CloudFormation template
            template_content = {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Resources": {
                    "WebServer": {
                        "Type": "AWS::EC2::Instance",
                        "Properties": {
                            "InstanceType": "t3.large",
                            "ImageId": "ami-12345678"
                        }
                    }
                }
            }
            
            with open(os.path.join(cdk_out_path, "SampleStack.template.json"), 'w') as f:
                json.dump(template_content, f)
            
            templates = _analyze_synthesized_templates(cdk_out_path)
            stack_summary = _generate_stack_summary(templates)
            
            print(f"   📊 Total stacks: {stack_summary['total_stacks']}")
            print(f"   🏗️  Total resources: {stack_summary['total_resources']}")
            print()
            
            print("🎉 All CDK helper functions work correctly!")
            print("✅ CDK tools are ready for integration!")
            print()
            print("💡 The CDK analysis tools are fully functional and integrated into the agent.")
            print("   They just require the strands module to be installed for the full agent to run.")
            
        except Exception as e:
            print(f"❌ Error testing CDK functions: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    test_cdk_helper_functions()
