#!/usr/bin/env python3
"""
Interactive test for CDK analysis functionality
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from aws_devops_agent.tools.aws_cdk.cdk_analysis import (
    analyze_cdk_project,
    synthesize_cdk_project,
    generate_cdk_optimization_report
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
    
    # Create package.json
    package_json = {
        "name": "sample-cdk-project",
        "version": "1.0.0",
        "description": "Sample CDK project for testing",
        "main": "bin/app.ts",
        "scripts": {
            "build": "tsc",
            "watch": "tsc -w",
            "cdk": "cdk"
        },
        "devDependencies": {
            "typescript": "^4.9.5",
            "@types/node": "^18.0.0",
            "aws-cdk": "^2.0.0",
            "aws-cdk-lib": "^2.0.0",
            "constructs": "^10.0.0"
        }
    }
    
    with open(os.path.join(project_path, "package.json"), 'w') as f:
        json.dump(package_json, f, indent=2)


def test_cdk_analysis():
    """Test CDK analysis functionality"""
    print("🧪 Testing CDK Analysis Tools")
    print("=" * 50)
    
    # Create temporary directory for test project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = os.path.join(temp_dir, "sample-cdk-project")
        create_sample_cdk_project(project_path)
        
        print(f"📁 Created sample CDK project at: {project_path}")
        print()
        
        # Test 1: Analyze CDK project
        print("1️⃣ Analyzing CDK project structure...")
        analysis_result = analyze_cdk_project(project_path, "production")
        
        if analysis_result["status"] == "success":
            print("✅ Project analysis successful!")
            print(f"   📊 Files analyzed: {analysis_result['summary']['total_files_analyzed']}")
            print(f"   🔍 Findings: {analysis_result['summary']['total_findings']}")
            print(f"   💡 Recommendations: {analysis_result['summary']['total_recommendations']}")
            print(f"   🔒 Security issues: {analysis_result['summary']['critical_security_issues']}")
            print(f"   💰 Potential savings: ${analysis_result['summary']['potential_monthly_savings']:.2f}/month")
        else:
            print(f"❌ Project analysis failed: {analysis_result['error']}")
        
        print()
        
        # Test 2: Generate optimization report (without synthesis)
        print("2️⃣ Generating CDK optimization report...")
        report_result = generate_cdk_optimization_report(project_path, "production")
        
        if report_result["status"] == "success":
            print("✅ Optimization report generated!")
            exec_summary = report_result["executive_summary"]
            print(f"   📈 Total stacks: {exec_summary.get('total_stacks', 'N/A')}")
            print(f"   🏗️  Total resources: {exec_summary.get('total_resources', 'N/A')}")
            print(f"   💰 Estimated cost: ${exec_summary.get('estimated_monthly_cost', 0):.2f}/month")
            print(f"   🔒 Security findings: {exec_summary.get('security_findings', 0)}")
            print(f"   📋 Key recommendations: {exec_summary.get('key_recommendations', 0)}")
        else:
            print(f"❌ Report generation failed: {report_result['error']}")
        
        print()
        
        # Test 3: Show specific findings
        if analysis_result["status"] == "success":
            print("3️⃣ Detailed findings:")
            
            # Show cost optimization opportunities
            cost_ops = analysis_result.get("cost_optimization_opportunities", [])
            if cost_ops:
                print("   💰 Cost Optimization Opportunities:")
                for i, opp in enumerate(cost_ops[:3], 1):  # Show first 3
                    print(f"      {i}. {opp.get('issue', 'N/A')}")
                    print(f"         💡 {opp.get('recommendation', 'N/A')}")
                    print(f"         💵 Potential savings: ${opp.get('monthly_savings', 0):.2f}/month")
                    print()
            
            # Show security issues
            security_issues = analysis_result.get("security_issues", [])
            if security_issues:
                print("   🔒 Security Issues:")
                for i, issue in enumerate(security_issues[:3], 1):  # Show first 3
                    print(f"      {i}. {issue.get('issue', 'N/A')}")
                    print(f"         ⚠️  Severity: {issue.get('severity', 'N/A')}")
                    print(f"         💡 {issue.get('recommendation', 'N/A')}")
                    print()
            
            # Show best practices violations
            best_practices = analysis_result.get("best_practices_violations", [])
            if best_practices:
                print("   📋 Best Practices Violations:")
                for i, practice in enumerate(best_practices[:3], 1):  # Show first 3
                    print(f"      {i}. {practice.get('issue', 'N/A')}")
                    print(f"         💡 {practice.get('recommendation', 'N/A')}")
                    print()
        
        print("🎉 CDK analysis test completed!")


if __name__ == "__main__":
    test_cdk_analysis()
