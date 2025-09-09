#!/usr/bin/env python3
"""
Demo script for CDK analysis functionality
This demonstrates the CDK analysis tools without requiring the full agent setup
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# Add src to path (go up two levels from docs/demos to project root)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Import CDK analysis functions directly
from aws_devops_agent.tools.aws_cdk.cdk_analysis import (
    analyze_cdk_project,
    synthesize_cdk_project,
    analyze_cdk_synthesized_output,
    generate_cdk_optimization_report
)


def create_sample_cdk_project(project_path: str):
    """Create a sample CDK project for demonstration"""
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


def demo_cdk_analysis():
    """Demonstrate CDK analysis functionality"""
    print("🚀 AWS DevOps Agent - CDK Analysis Demo")
    print("=" * 60)
    print()
    
    # Create temporary directory for demo project
    with tempfile.TemporaryDirectory() as temp_dir:
        project_path = os.path.join(temp_dir, "demo-cdk-project")
        create_sample_cdk_project(project_path)
        
        print(f"📁 Created demo CDK project at: {project_path}")
        print()
        
        # Demo 1: Analyze CDK project
        print("1️⃣ Analyzing CDK project structure...")
        print("-" * 40)
        
        try:
            analysis_result = analyze_cdk_project(project_path, "production")
            
            if analysis_result["status"] == "success":
                print("✅ Project analysis successful!")
                print()
                
                # Show project info
                project_info = analysis_result["project_info"]
                print("📊 Project Information:")
                print(f"   CDK Version: {project_info['cdk_version']}")
                print(f"   Language: {project_info['language']}")
                print(f"   Stacks: {project_info['stacks_count']}")
                print(f"   Constructs: {project_info['constructs_count']}")
                print()
                
                # Show summary
                summary = analysis_result["summary"]
                print("📈 Analysis Summary:")
                print(f"   Files analyzed: {summary['total_files_analyzed']}")
                print(f"   Total findings: {summary['total_findings']}")
                print(f"   Recommendations: {summary['total_recommendations']}")
                print(f"   Critical security issues: {summary['critical_security_issues']}")
                print(f"   Potential monthly savings: ${summary['potential_monthly_savings']:.2f}")
                print()
                
                # Show specific findings
                print("🔍 Detailed Findings:")
                
                # Cost optimization opportunities
                cost_ops = analysis_result.get("cost_optimization_opportunities", [])
                if cost_ops:
                    print("   💰 Cost Optimization Opportunities:")
                    for i, opp in enumerate(cost_ops[:3], 1):
                        print(f"      {i}. {opp.get('issue', 'N/A')}")
                        print(f"         💡 {opp.get('recommendation', 'N/A')}")
                        print(f"         💵 Potential savings: ${opp.get('monthly_savings', 0):.2f}/month")
                        print()
                
                # Security issues
                security_issues = analysis_result.get("security_issues", [])
                if security_issues:
                    print("   🔒 Security Issues:")
                    for i, issue in enumerate(security_issues[:3], 1):
                        print(f"      {i}. {issue.get('issue', 'N/A')}")
                        print(f"         ⚠️  Severity: {issue.get('severity', 'N/A')}")
                        print(f"         💡 {issue.get('recommendation', 'N/A')}")
                        print()
                
                # Best practices violations
                best_practices = analysis_result.get("best_practices_violations", [])
                if best_practices:
                    print("   📋 Best Practices Violations:")
                    for i, practice in enumerate(best_practices[:3], 1):
                        print(f"      {i}. {practice.get('issue', 'N/A')}")
                        print(f"         💡 {practice.get('recommendation', 'N/A')}")
                        print()
                
            else:
                print(f"❌ Project analysis failed: {analysis_result['error']}")
                
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
        
        print()
        
        # Demo 2: Generate optimization report
        print("2️⃣ Generating comprehensive optimization report...")
        print("-" * 40)
        
        try:
            report_result = generate_cdk_optimization_report(project_path, "production")
            
            if report_result["status"] == "success":
                print("✅ Optimization report generated!")
                print()
                
                # Show executive summary
                exec_summary = report_result["executive_summary"]
                print("📊 Executive Summary:")
                print(f"   Total stacks: {exec_summary.get('total_stacks', 'N/A')}")
                print(f"   Total resources: {exec_summary.get('total_resources', 'N/A')}")
                print(f"   Estimated monthly cost: ${exec_summary.get('estimated_monthly_cost', 0):.2f}")
                print(f"   Security findings: {exec_summary.get('security_findings', 0)}")
                print(f"   Key recommendations: {exec_summary.get('key_recommendations', 0)}")
                print()
                
                # Show cost optimization section
                cost_opt = report_result["cost_optimization"]
                print("💰 Cost Optimization:")
                print(f"   Current estimated cost: ${cost_opt.get('current_estimated_cost', 0):.2f}/month")
                print(f"   Potential savings: ${cost_opt.get('potential_savings', 0):.2f}/month")
                print()
                
                # Show implementation roadmap
                roadmap = report_result["implementation_roadmap"]
                if roadmap:
                    print("🗺️  Implementation Roadmap:")
                    for phase in roadmap:
                        print(f"   Phase {phase['phase']}: {phase['title']}")
                        print(f"      Duration: {phase['duration']}")
                        print(f"      Priority: {phase['priority']}")
                        print(f"      Tasks: {', '.join(phase['tasks'])}")
                        print()
                
            else:
                print(f"❌ Report generation failed: {report_result['error']}")
                
        except Exception as e:
            print(f"❌ Error during report generation: {str(e)}")
        
        print("🎉 CDK Analysis Demo completed!")
        print()
        print("💡 Key Features Demonstrated:")
        print("   • CDK project structure analysis")
        print("   • Source code pattern detection")
        print("   • Cost optimization identification")
        print("   • Security issue detection")
        print("   • Best practices validation")
        print("   • Comprehensive reporting")
        print()
        print("🚀 Ready for integration with AWS DevOps Agent!")


if __name__ == "__main__":
    demo_cdk_analysis()
