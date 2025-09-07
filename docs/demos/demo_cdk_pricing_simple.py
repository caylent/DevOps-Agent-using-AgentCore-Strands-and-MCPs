#!/usr/bin/env python3
"""
Demo: CDK Cost Estimation with Real AWS Pricing
Demonstrates CDK cost analysis using real AWS pricing data
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aws_devops_agent.tools.aws_cdk.cdk_analysis import _estimate_ec2_cost, _estimate_aws_service_cost


def demo_cdk_pricing_simple():
    """Simple, focused CDK pricing demo"""
    print("💰 CDK Cost Estimation - Real AWS Pricing Demo")
    print("=" * 55)
    print("Purpose: Show how CDK cost estimation uses real AWS pricing data")
    print("Scope: EC2 instances and other AWS services")
    print()
    
    # Test EC2 pricing
    print("🖥️ EC2 Instance Pricing:")
    print("-" * 30)
    
    instance_types = ["t3.micro", "t3.small", "m5.large", "c5.xlarge"]
    for instance_type in instance_types:
        try:
            cost = _estimate_ec2_cost(instance_type)
            print(f"   {instance_type}: ${cost:.2f}/month")
        except Exception as e:
            print(f"   {instance_type}: Error - {e}")
    
    print()
    
    # Test other AWS services
    print("☁️ Other AWS Services Pricing:")
    print("-" * 35)
    
    test_services = [
        ("RDS", "AWS::RDS::DBInstance", {"DBInstanceClass": "db.t3.micro", "AllocatedStorage": 20}),
        ("S3", "AWS::S3::Bucket", {}),
        ("Lambda", "AWS::Lambda::Function", {"MemorySize": 512}),
        ("ELB", "AWS::ElasticLoadBalancingV2::LoadBalancer", {}),
        ("DynamoDB", "AWS::DynamoDB::Table", {})
    ]
    
    for service_name, resource_type, properties in test_services:
        try:
            cost = _estimate_aws_service_cost(service_name, resource_type, properties)
            print(f"   {service_name} ({resource_type}): ${cost:.2f}/month")
        except Exception as e:
            print(f"   {service_name}: Error - {e}")
    
    print()
    print("🎉 Demo completed!")
    print("This shows how CDK cost estimation now uses real AWS pricing data.")


if __name__ == "__main__":
    demo_cdk_pricing_simple()
