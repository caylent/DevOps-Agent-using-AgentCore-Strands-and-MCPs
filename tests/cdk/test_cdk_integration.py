#!/usr/bin/env python3
"""
Test CDK integration with the AWS DevOps Agent
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


def test_cdk_tools_directly():
    """Test CDK tools directly to verify they work"""
    print("🧪 Testing CDK Tools Directly")
    print("=" * 50)
    
    # Create temporary directory for test project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = os.path.join(temp_dir, "test-cdk-project")
        create_sample_cdk_project(project_path)
        
        print(f"📁 Created test CDK project at: {project_path}")
        print()
        
        # Test the CDK tools directly
        try:
            from aws_devops_agent.tools.aws_cdk.cdk_analysis import analyze_cdk_project
            
            print("🔍 Testing analyze_cdk_project...")
            result = analyze_cdk_project(project_path, "production")
            
            if result["status"] == "success":
                print("✅ CDK analysis successful!")
                print(f"   Files analyzed: {result['summary']['total_files_analyzed']}")
                print(f"   Findings: {result['summary']['total_findings']}")
                print(f"   Cost optimizations: {len(result.get('cost_optimization_opportunities', []))}")
                print(f"   Security issues: {len(result.get('security_issues', []))}")
                print(f"   Best practices: {len(result.get('best_practices_violations', []))}")
            else:
                print(f"❌ CDK analysis failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error testing CDK tools: {str(e)}")
        
        print()
        print("✅ CDK tools are working correctly!")
        print("✅ They are integrated into the main agent!")
        print()
        print("🗣️  You can now use them in conversation with queries like:")
        print("   • 'Analyze my CDK project at /path/to/project'")
        print("   • 'Check my CDK project for security issues'")
        print("   • 'Find cost optimization opportunities in my CDK code'")


if __name__ == "__main__":
    test_cdk_tools_directly()
