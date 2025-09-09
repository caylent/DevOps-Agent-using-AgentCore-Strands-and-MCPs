#!/usr/bin/env python3
"""
Terraform Analysis Demo

This demo showcases the Terraform analysis capabilities of the AWS DevOps Agent.
It demonstrates how to analyze Terraform projects for cost optimization, security,
and best practices.
"""

import os
import sys
import tempfile
import shutil
import json
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from aws_devops_agent.tools.aws_terraform.terraform_analysis import (
    analyze_terraform_project,
    validate_terraform_configuration,
    plan_terraform_changes,
    analyze_terraform_state,
    generate_terraform_optimization_report
)


def create_sample_terraform_project():
    """Create a sample Terraform project for demonstration"""
    project_dir = tempfile.mkdtemp(prefix="terraform_demo_")
    
    # Create main.tf
    main_tf = '''
provider "aws" {
  region = "us-east-1"
}

# EC2 Instance
resource "aws_instance" "web_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.large"  # Could be optimized to t3.medium
  
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  
  tags = {
    Name        = "web-server-${var.environment}"
    Environment = var.environment
    Project     = "terraform-demo"
  }
}

# Security Group
resource "aws_security_group" "web_sg" {
  name_prefix = "web-sg-"
  
  # HTTP access
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Security issue: too permissive
  }
  
  # HTTPS access
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Security issue: too permissive
  }
  
  # SSH access
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Security issue: too permissive
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "web-security-group"
  }
}

# RDS Instance
resource "aws_db_instance" "web_db" {
  identifier = "web-db-${var.environment}"
  
  engine         = "mysql"
  engine_version = "8.0"
  instance_class = "db.t3.medium"  # Could be optimized
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"  # Could be optimized to gp3
  
  db_name  = "webapp"
  username = "admin"
  password = "changeme123"  # Security issue: hardcoded password
  
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = true  # Security issue: should create final snapshot
  
  tags = {
    Name        = "web-database-${var.environment}"
    Environment = var.environment
  }
}

# Database Security Group
resource "aws_security_group" "db_sg" {
  name_prefix = "db-sg-"
  
  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.web_sg.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "db-security-group"
  }
}

# S3 Bucket
resource "aws_s3_bucket" "web_storage" {
  bucket = "web-storage-${var.environment}-${random_string.bucket_suffix.result}"
  
  tags = {
    Name        = "web-storage-${var.environment}"
    Environment = var.environment
  }
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "web_storage_versioning" {
  bucket = aws_s3_bucket.web_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket Public Access Block
resource "aws_s3_bucket_public_access_block" "web_storage_pab" {
  bucket = aws_s3_bucket.web_storage.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Random string for bucket suffix
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}
'''
    
    # Create variables.tf
    variables_tf = '''
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "instance_type" {
  description = "Type of EC2 instance"
  type        = string
  default     = "t3.large"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}
'''
    
    # Create outputs.tf
    outputs_tf = '''
output "web_server_id" {
  description = "ID of the web server instance"
  value       = aws_instance.web_server.id
}

output "web_server_public_ip" {
  description = "Public IP of the web server"
  value       = aws_instance.web_server.public_ip
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.web_db.endpoint
  sensitive   = true
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.web_storage.bucket
}

output "security_group_ids" {
  description = "IDs of the security groups"
  value = {
    web = aws_security_group.web_sg.id
    db  = aws_security_group.db_sg.id
  }
}
'''
    
    # Create terraform.tfvars
    tfvars = '''
environment = "production"
instance_type = "t3.large"
db_instance_class = "db.t3.medium"
'''
    
    # Write files
    files = {
        'main.tf': main_tf,
        'variables.tf': variables_tf,
        'outputs.tf': outputs_tf,
        'terraform.tfvars': tfvars
    }
    
    for filename, content in files.items():
        with open(os.path.join(project_dir, filename), 'w') as f:
            f.write(content)
    
    return project_dir


def demo_terraform_analysis():
    """Demonstrate Terraform analysis capabilities"""
    print("🏗️  TERRAFORM ANALYSIS DEMO")
    print("=" * 50)
    print()
    
    # Create sample project
    print("📁 Creating sample Terraform project...")
    project_dir = create_sample_terraform_project()
    print(f"   ✅ Project created at: {project_dir}")
    print()
    
    try:
        # 1. Analyze Terraform Project
        print("🔍 1. ANALYZING TERRAFORM PROJECT")
        print("-" * 30)
        
        analysis_result = analyze_terraform_project(project_dir, "production")
        
        if analysis_result["status"] == "success":
            print("   ✅ Project analysis completed successfully")
            data = analysis_result["data"]
            print(f"   📊 Environment: {data['environment']}")
            print(f"   📅 Analysis timestamp: {data['analysis_timestamp']}")
            print(f"   💰 Cost impact: {analysis_result.get('cost_impact', 'N/A')}")
            print(f"   📋 Recommendations: {len(data.get('recommendations', []))}")
        else:
            print(f"   ⚠️  Project analysis: {analysis_result['status']}")
            print(f"   📝 Error: {analysis_result.get('error', 'Unknown error')}")
            print(f"   💡 Suggestion: {analysis_result.get('suggestion', 'N/A')}")
        
        print()
        
        # 2. Validate Configuration
        print("✅ 2. VALIDATING TERRAFORM CONFIGURATION")
        print("-" * 40)
        
        validation_result = validate_terraform_configuration(project_dir)
        
        if validation_result["status"] == "success":
            print("   ✅ Configuration validation completed")
            if validation_result["data"]["validation_passed"]:
                print("   ✅ Configuration is valid")
            else:
                print("   ❌ Configuration has errors")
                print(f"   📝 Errors: {validation_result['data'].get('errors', 'N/A')}")
        else:
            print(f"   ⚠️  Validation: {validation_result['status']}")
            print(f"   📝 Error: {validation_result.get('error', 'Unknown error')}")
        
        print()
        
        # 3. Generate Plan
        print("📋 3. GENERATING TERRAFORM PLAN")
        print("-" * 30)
        
        plan_result = plan_terraform_changes(project_dir, "production")
        
        if plan_result["status"] == "success":
            print("   ✅ Plan generation completed")
            print(f"   📊 Environment: {plan_result['data']['environment']}")
            print(f"   📁 Plan file: {plan_result['data'].get('plan_file', 'N/A')}")
        else:
            print(f"   ⚠️  Plan generation: {plan_result['status']}")
            print(f"   📝 Error: {plan_result.get('error', 'Unknown error')}")
        
        print()
        
        # 4. Analyze State (if exists)
        print("🗃️  4. ANALYZING TERRAFORM STATE")
        print("-" * 30)
        
        state_result = analyze_terraform_state(project_dir)
        
        if state_result["status"] == "success":
            print("   ✅ State analysis completed")
            print(f"   📊 Resource count: {state_result['data']['resource_count']}")
            print(f"   🔧 Terraform version: {state_result['data'].get('terraform_version', 'N/A')}")
        else:
            print(f"   ⚠️  State analysis: {state_result['status']}")
            print(f"   📝 Message: {state_result.get('error', 'No state file found (expected)')}")
        
        print()
        
        # 5. Generate Optimization Report
        print("📊 5. GENERATING OPTIMIZATION REPORT")
        print("-" * 35)
        
        # Create mock analysis results for demonstration
        mock_analysis_results = {
            "status": "success",
            "data": {
                "project_path": project_dir,
                "environment": "production",
                "security": {
                    "overall_security_score": 65,
                    "security_issues": [
                        {
                            "type": "Hardcoded Secrets",
                            "severity": "High",
                            "count": 1,
                            "description": "Hardcoded password in RDS configuration"
                        },
                        {
                            "type": "Public Resources",
                            "severity": "Medium",
                            "count": 3,
                            "description": "Security groups allow access from 0.0.0.0/0"
                        },
                        {
                            "type": "Missing Encryption",
                            "severity": "Medium",
                            "count": 1,
                            "description": "RDS instance missing encryption configuration"
                        }
                    ]
                },
                "cost_optimization": {
                    "estimated_monthly_cost": "$1,250.00",
                    "potential_savings": "$300.00/month",
                    "savings_percentage": 24,
                    "optimization_opportunities": [
                        {
                            "resource_type": "EC2 Instances",
                            "current_cost": "$800.00",
                            "optimized_cost": "$600.00",
                            "savings": "$200.00",
                            "recommendation": "Use t3.medium instead of t3.large for non-production workloads"
                        },
                        {
                            "resource_type": "RDS Instances",
                            "current_cost": "$300.00",
                            "optimized_cost": "$200.00",
                            "savings": "$100.00",
                            "recommendation": "Use gp3 storage instead of gp2 and enable automated backups"
                        }
                    ]
                },
                "best_practices": {
                    "overall_score": 75,
                    "violations": [
                        {
                            "practice": "Resource naming conventions",
                            "severity": "Low",
                            "count": 2,
                            "description": "Some resources don't follow consistent naming patterns"
                        },
                        {
                            "practice": "Module usage",
                            "severity": "Medium",
                            "count": 1,
                            "description": "Consider using modules for repeated security group configurations"
                        },
                        {
                            "practice": "Variable usage",
                            "severity": "Low",
                            "count": 1,
                            "description": "Some hardcoded values could be parameterized"
                        }
                    ]
                },
                "recommendations": [
                    {
                        "category": "Security",
                        "priority": "High",
                        "description": "Address Hardcoded Secrets: Hardcoded password in RDS configuration",
                        "impact": "High"
                    },
                    {
                        "category": "Security",
                        "priority": "Medium",
                        "description": "Address Public Resources: Security groups allow access from 0.0.0.0/0",
                        "impact": "High"
                    },
                    {
                        "category": "Cost Optimization",
                        "priority": "High",
                        "description": "EC2 Instance Optimization: Use t3.medium instead of t3.large (Save $200.00/month)",
                        "impact": "Medium"
                    },
                    {
                        "category": "Best Practices",
                        "priority": "Medium",
                        "description": "Fix Module usage: Consider using modules for repeated security group configurations",
                        "impact": "Low"
                    }
                ]
            }
        }
        
        report_result = generate_terraform_optimization_report(mock_analysis_results)
        
        if report_result["status"] == "success":
            print("   ✅ Optimization report generated successfully")
            print(f"   📊 Overall score: {report_result['data']['overall_score']}/100")
            print(f"   💰 Potential savings: {report_result.get('cost_impact', 'N/A')}")
            print(f"   📋 Recommendations: {len(report_result['data']['sections']['recommendations'])}")
            
            # Display report sections
            sections = report_result['data']['sections']
            print()
            print("   📋 REPORT SECTIONS:")
            print(f"   • Executive Summary: {len(sections['executive_summary'])} characters")
            print(f"   • Security Findings: {len(sections['security_findings'])} characters")
            print(f"   • Cost Optimization: {len(sections['cost_optimization'])} characters")
            print(f"   • Best Practices: {len(sections['best_practices'])} characters")
            print(f"   • Recommendations: {len(sections['recommendations'])} characters")
            print(f"   • Next Steps: {len(sections['next_steps'])} characters")
        else:
            print(f"   ⚠️  Report generation: {report_result['status']}")
            print(f"   📝 Error: {report_result.get('error', 'Unknown error')}")
        
        print()
        
        # 6. Display Sample Report Content
        print("📄 6. SAMPLE REPORT CONTENT")
        print("-" * 25)
        
        if report_result["status"] == "success":
            sections = report_result['data']['sections']
            
            print("   📊 EXECUTIVE SUMMARY:")
            print(f"   {sections['executive_summary'].strip()}")
            print()
            
            print("   🔒 SECURITY FINDINGS:")
            print(f"   {sections['security_findings'].strip()}")
            print()
            
            print("   💰 COST OPTIMIZATION:")
            print(f"   {sections['cost_optimization'].strip()}")
            print()
            
            print("   📋 RECOMMENDATIONS:")
            print(f"   {sections['recommendations'].strip()}")
            print()
            
            print("   🎯 NEXT STEPS:")
            print(f"   {sections['next_steps'].strip()}")
        
        print()
        
        # 7. Summary
        print("📊 7. DEMO SUMMARY")
        print("-" * 15)
        print("   ✅ Terraform project analysis completed")
        print("   ✅ Configuration validation tested")
        print("   ✅ Plan generation demonstrated")
        print("   ✅ State analysis showcased")
        print("   ✅ Optimization report generated")
        print("   ✅ Security, cost, and best practices analysis provided")
        print()
        print("   🎯 KEY CAPABILITIES DEMONSTRATED:")
        print("   • Comprehensive Terraform project analysis")
        print("   • Security vulnerability detection")
        print("   • Cost optimization recommendations")
        print("   • Best practices validation")
        print("   • Detailed reporting and recommendations")
        print("   • Integration with AWS DevOps Agent")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print()
        print("🧹 Cleaning up demo project...")
        shutil.rmtree(project_dir, ignore_errors=True)
        print("   ✅ Demo project cleaned up")


def main():
    """Main demo function"""
    print("🚀 AWS DevOps Agent - Terraform Analysis Demo")
    print("=" * 50)
    print()
    print("This demo showcases the Terraform analysis capabilities")
    print("of the AWS DevOps Agent, including:")
    print("• Project analysis and validation")
    print("• Security vulnerability detection")
    print("• Cost optimization recommendations")
    print("• Best practices validation")
    print("• Comprehensive reporting")
    print()
    
    try:
        demo_terraform_analysis()
        print()
        print("🎉 Demo completed successfully!")
        print()
        print("💡 To use these capabilities in your own projects:")
        print("   1. Install Terraform CLI: https://terraform.io/downloads")
        print("   2. Run: python src/aws_devops_agent/main.py")
        print("   3. Ask: 'Analyze my Terraform project at /path/to/project'")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
