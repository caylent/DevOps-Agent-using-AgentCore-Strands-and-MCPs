#!/usr/bin/env python3
"""
Simple Terraform Test

Quick test to verify Terraform tools are working correctly.
"""

import os
import sys
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from aws_devops_agent.tools.aws_terraform.terraform_analysis import (
    analyze_terraform_project,
    validate_terraform_configuration
)


def test_terraform_tools_import():
    """Test that Terraform tools can be imported"""
    print("✅ Terraform tools imported successfully")
    
    # Test function availability
    assert callable(analyze_terraform_project)
    assert callable(validate_terraform_configuration)
    print("✅ Terraform functions are callable")


def test_terraform_project_analysis_nonexistent():
    """Test Terraform project analysis with nonexistent path"""
    result = analyze_terraform_project("/nonexistent/path", "test")
    
    assert result["status"] == "error"
    assert "Project path does not exist" in result["error"]
    print("✅ Terraform project analysis handles nonexistent paths correctly")


def test_terraform_validation_nonexistent():
    """Test Terraform validation with nonexistent path"""
    result = validate_terraform_configuration("/nonexistent/path")
    
    assert result["status"] == "error"
    assert "Project path does not exist" in result["error"]
    print("✅ Terraform validation handles nonexistent paths correctly")


def test_terraform_optimization_report_invalid():
    """Test Terraform optimization report with invalid input"""
    from aws_devops_agent.tools.aws_terraform.terraform_analysis import generate_terraform_optimization_report
    
    result = generate_terraform_optimization_report({"status": "error"})
    
    assert result["status"] == "error"
    assert "Invalid analysis results provided" in result["error"]
    print("✅ Terraform optimization report handles invalid input correctly")


if __name__ == "__main__":
    print("🧪 Running Simple Terraform Tests...")
    print()
    
    test_terraform_tools_import()
    test_terraform_project_analysis_nonexistent()
    test_terraform_validation_nonexistent()
    test_terraform_optimization_report_invalid()
    
    print()
    print("✅ All simple Terraform tests passed!")
