#!/usr/bin/env python3
"""
Enhanced Document Generation Demo
Showcases the improved report generation with icons and comprehensive content
"""

import os
import sys
from pathlib import Path

# Add src to path (go up two levels from docs/demos to project root)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def demo_enhanced_reports():
    """Demonstrate enhanced document generation with icons and rich content"""
    print("🎨 Enhanced Document Generation Demo")
    print("=" * 50)
    
    try:
        from aws_devops_agent.tools.reporting.document_generator import (
            generate_cost_analysis_document,
            generate_security_compliance_document,
            generate_infrastructure_document,
            generate_cdk_analysis_document,
            list_generated_documents
        )
        
        print("✅ Successfully imported enhanced document generation tools")
        
        # Demo 1: Enhanced Cost Analysis Report
        print("\n1️⃣ Generating Enhanced Cost Analysis Report...")
        cost_data = {
            "total_monthly_cost": 2500.00,
            "potential_savings": 750.00,
            "optimization_opportunities": [
                {
                    "resource": "EC2 Instance (i-1234567890abcdef0)",
                    "current_cost": 1200.00,
                    "potential_savings": 400.00,
                    "recommendation": "Right-size from m5.large to m5.medium",
                    "priority": "high",
                    "category": "compute"
                },
                {
                    "resource": "RDS Instance (db.t3.large)",
                    "current_cost": 600.00,
                    "potential_savings": 200.00,
                    "recommendation": "Implement Reserved Instances",
                    "priority": "high",
                    "category": "database"
                }
            ],
            "recommendations": [
                {"recommendation": "Implement Reserved Instances for EC2", "priority": "high", "savings": "$400/month"},
                {"recommendation": "Right-size underutilized instances", "priority": "high", "savings": "$300/month"},
                {"recommendation": "Use Spot Instances for non-critical workloads", "priority": "medium", "savings": "$200/month"},
                {"recommendation": "Optimize S3 storage classes", "priority": "low", "savings": "$50/month"}
            ],
            "cost_breakdown": {
                "by_service": {"EC2": 1200, "RDS": 600, "S3": 300, "Lambda": 200, "CloudWatch": 100, "Other": 100},
                "by_region": {"us-east-1": 1500, "us-west-2": 700, "eu-west-1": 300},
                "by_account": {"production": 1800, "staging": 500, "development": 200},
                "monthly_trend": [
                    {"month": "Jan", "cost": 2200},
                    {"month": "Feb", "cost": 2350},
                    {"month": "Mar", "cost": 2500}
                ]
            },
            "resource_analysis": {
                "underutilized": [
                    {"resource": "i-1234567890abcdef0", "utilization": "25%", "recommendation": "Downsize"},
                    {"resource": "i-0987654321fedcba0", "utilization": "30%", "recommendation": "Right-size"}
                ],
                "overprovisioned": [
                    {"resource": "db.t3.large", "cpu_utilization": "15%", "recommendation": "Downsize to db.t3.medium"}
                ],
                "unused": [
                    {"resource": "vol-1234567890abcdef0", "size": "100GB", "cost": "$10/month"},
                    {"resource": "snap-0987654321fedcba0", "size": "50GB", "cost": "$5/month"}
                ]
            },
            "trend_analysis": {
                "cost_trends": ["15% increase over last 3 months", "Peak usage during business hours"],
                "usage_patterns": ["EC2 usage spikes on weekdays", "RDS steady usage", "S3 growth of 20% monthly"],
                "seasonal_variations": ["Higher costs during holiday season", "Lower costs on weekends"],
                "forecast": {"next_month": 2625, "next_quarter": 2750, "next_year": 3000}
            }
        }
        
        result = generate_cost_analysis_document(
            cost_data=cost_data,
            title="Comprehensive AWS Cost Analysis Report"
        )
        
        if result["status"] == "success":
            print(f"✅ Enhanced cost analysis report generated!")
            print(f"   📁 File: {result['file_path']}")
            print(f"   📄 Filename: {result['filename']}")
        else:
            print(f"❌ Cost analysis report generation failed: {result['error']}")
        
        # Demo 2: Enhanced Security Compliance Report
        print("\n2️⃣ Generating Enhanced Security Compliance Report...")
        security_data = {
            "compliance_score": 75,
            "total_findings": 12,
            "findings": [
                {
                    "id": "SEC-001",
                    "title": "S3 Bucket Public Access",
                    "severity": "critical",
                    "category": "access_control",
                    "description": "S3 bucket allows public read access",
                    "recommendation": "Enable S3 bucket public access blocking",
                    "resource": "s3://my-public-bucket"
                },
                {
                    "id": "SEC-002", 
                    "title": "EC2 Security Group Open Ports",
                    "severity": "high",
                    "category": "network_security",
                    "description": "Security group allows SSH from 0.0.0.0/0",
                    "recommendation": "Restrict SSH access to specific IP ranges",
                    "resource": "sg-1234567890abcdef0"
                },
                {
                    "id": "SEC-003",
                    "title": "RDS Encryption Not Enabled",
                    "severity": "medium",
                    "category": "encryption",
                    "description": "RDS instance not encrypted at rest",
                    "recommendation": "Enable encryption for RDS instance",
                    "resource": "db.t3.medium"
                }
            ],
            "recommendations": [
                {"recommendation": "Enable S3 bucket public access blocking", "priority": "critical", "effort": "Low"},
                {"recommendation": "Restrict security group access", "priority": "high", "effort": "Medium"},
                {"recommendation": "Enable RDS encryption", "priority": "medium", "effort": "High"},
                {"recommendation": "Implement CloudTrail logging", "priority": "medium", "effort": "Medium"}
            ],
            "compliance_status": {
                "overall": "Needs Improvement",
                "frameworks": {"SOC2": "60%", "HIPAA": "40%", "PCI-DSS": "30%"},
                "controls": {"access_control": "70%", "encryption": "50%", "monitoring": "60%"},
                "last_assessment": "2025-09-01"
            },
            "remediation_plan": {
                "immediate": ["Fix S3 bucket public access", "Review security groups"],
                "short_term": ["Enable RDS encryption", "Implement CloudTrail"],
                "long_term": ["Complete SOC2 compliance", "Regular security audits"]
            }
        }
        
        result = generate_security_compliance_document(
            security_data=security_data,
            title="AWS Security Compliance Assessment Report"
        )
        
        if result["status"] == "success":
            print(f"✅ Enhanced security compliance report generated!")
            print(f"   📁 File: {result['file_path']}")
            print(f"   📄 Filename: {result['filename']}")
        else:
            print(f"❌ Security compliance report generation failed: {result['error']}")
        
        # Demo 3: Enhanced Infrastructure Report
        print("\n3️⃣ Generating Enhanced Infrastructure Report...")
        iac_data = {
            "total_resources": 45,
            "compliance_score": 80,
            "analysis": {
                "terraform_files": 12,
                "cloudformation_templates": 3,
                "total_lines_of_code": 2500,
                "complexity_score": "Medium"
            },
            "best_practices_analysis": {
                "terraform_best_practices": 85,
                "cloudformation_best_practices": 75,
                "security_best_practices": 70,
                "cost_optimization": 80
            },
            "security_issues": [
                {
                    "file": "main.tf",
                    "line": 45,
                    "issue": "Hardcoded password in variable",
                    "severity": "high",
                    "recommendation": "Use AWS Secrets Manager"
                },
                {
                    "file": "security-groups.tf",
                    "line": 23,
                    "issue": "Security group allows all traffic",
                    "severity": "medium",
                    "recommendation": "Restrict to specific ports and IPs"
                }
            ],
            "recommendations": [
                {"recommendation": "Implement Terraform modules", "priority": "high", "impact": "Maintainability"},
                {"recommendation": "Add input validation", "priority": "medium", "impact": "Security"},
                {"recommendation": "Use remote state backend", "priority": "high", "impact": "Collaboration"}
            ]
        }
        
        result = generate_infrastructure_document(
            iac_data=iac_data,
            title="Infrastructure as Code Analysis Report"
        )
        
        if result["status"] == "success":
            print(f"✅ Enhanced infrastructure report generated!")
            print(f"   📁 File: {result['file_path']}")
            print(f"   📄 Filename: {result['filename']}")
        else:
            print(f"❌ Infrastructure report generation failed: {result['error']}")
        
        # Demo 4: List all generated documents
        print("\n4️⃣ Listing all generated documents...")
        result = list_generated_documents(limit=10)
        
        if result["status"] == "success":
            print(f"✅ Found {result['showing']} documents:")
            for i, doc in enumerate(result["reports"][:5], 1):
                print(f"   {i}. 📄 {doc['filename']} ({doc['report_type']}) - {doc['size_bytes']} bytes")
        else:
            print(f"❌ Document listing failed: {result['error']}")
        
        print("\n🎉 Enhanced document generation demo completed!")
        print("📁 Check the 'reports/' folder for all generated documents")
        print("🎨 Reports now feature:")
        print("   ✨ Rich icons and emojis for better visual appeal")
        print("   📊 Comprehensive executive summaries")
        print("   🔍 Detailed analysis sections")
        print("   💡 Prioritized recommendations")
        print("   🚀 Implementation roadmaps")
        print("   📈 Enhanced metrics and KPIs")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demo_enhanced_reports()
