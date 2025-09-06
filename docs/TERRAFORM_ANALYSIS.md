# 🏗️ Terraform Analysis - AWS DevOps Agent

This document describes the comprehensive Terraform analysis capabilities of the AWS DevOps Agent, including project analysis, configuration validation, cost optimization, security analysis, and best practices validation.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The Terraform analysis module provides comprehensive analysis capabilities for Terraform projects, including:

- **Project Analysis**: Complete analysis of Terraform projects for optimization opportunities
- **Configuration Validation**: Syntax and logic validation of Terraform configurations
- **Plan Generation**: Generate and analyze Terraform plans for proposed changes
- **State Analysis**: Analyze Terraform state files for resource inventory and drift
- **Optimization Reporting**: Generate detailed optimization reports with recommendations

## ✨ Features

### 🔍 **Project Analysis**
- Comprehensive analysis of Terraform projects
- Security vulnerability detection
- Cost optimization opportunities identification
- Best practices validation
- Resource inventory and configuration analysis

### ✅ **Configuration Validation**
- Syntax validation of Terraform files
- Logic validation of resource configurations
- Provider configuration validation
- Variable and output validation
- Dependency analysis

### 📋 **Plan Generation**
- Generate Terraform plans for proposed changes
- Analyze resource additions, modifications, and deletions
- Change impact analysis
- Resource dependency validation

### 🗃️ **State Analysis**
- Analyze Terraform state files
- Resource inventory and configuration tracking
- Configuration drift detection
- State file integrity validation

### 📊 **Optimization Reporting**
- Generate comprehensive optimization reports
- Security findings and recommendations
- Cost optimization opportunities
- Best practices violations and fixes
- Executive summary and next steps

## 🚀 Installation

### Prerequisites

1. **Terraform CLI**: Install Terraform CLI for project analysis
   ```bash
   # macOS
   brew install terraform
   
   # Linux
   wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
   unzip terraform_1.5.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   
   # Windows
   # Download from https://terraform.io/downloads
   ```

2. **AWS DevOps Agent**: Ensure the agent is installed and configured
   ```bash
   # Install dependencies
   pip install -r requirements_production.txt
   
   # Verify installation
   python src/aws_devops_agent/main.py --help
   ```

### Optional Dependencies

- **AWS CLI**: For AWS resource analysis
- **Terraform Cloud**: For remote state analysis
- **Terraform Enterprise**: For enterprise features

## 📖 Usage

### Interactive Mode

Start the agent in interactive mode and ask about Terraform analysis:

```bash
python src/aws_devops_agent/main.py
```

Example conversations:
```
User: Analyze my Terraform project at /path/to/terraform/project
User: Validate my Terraform configuration for security issues
User: Generate a cost optimization report for my Terraform project
User: Plan changes for my Terraform project in production
```

### Programmatic Usage

```python
from aws_devops_agent.tools.aws_terraform.terraform_analysis import (
    analyze_terraform_project,
    validate_terraform_configuration,
    plan_terraform_changes,
    analyze_terraform_state,
    generate_terraform_optimization_report
)

# Analyze a Terraform project
result = analyze_terraform_project("/path/to/project", "production")
print(result)

# Validate configuration
validation = validate_terraform_configuration("/path/to/project")
print(validation)

# Generate plan
plan = plan_terraform_changes("/path/to/project", "production")
print(plan)

# Analyze state
state = analyze_terraform_state("/path/to/project")
print(state)

# Generate optimization report
report = generate_terraform_optimization_report(analysis_result)
print(report)
```

## 📚 API Reference

### `analyze_terraform_project(project_path: str, environment: str = "production") -> Dict[str, Any]`

Analyze a Terraform project for cost optimization, security, and best practices.

**Parameters:**
- `project_path` (str): Path to the Terraform project directory
- `environment` (str): Target environment (production, staging, development)

**Returns:**
- `Dict[str, Any]`: Comprehensive analysis results including security, cost, and best practices

**Example:**
```python
result = analyze_terraform_project("/path/to/terraform/project", "production")
if result["status"] == "success":
    print(f"Security score: {result['data']['security']['overall_security_score']}")
    print(f"Potential savings: {result['data']['cost_optimization']['potential_savings']}")
```

### `validate_terraform_configuration(project_path: str) -> Dict[str, Any]`

Validate Terraform configuration files for syntax and logic errors.

**Parameters:**
- `project_path` (str): Path to the Terraform project directory

**Returns:**
- `Dict[str, Any]`: Validation results with error details if any

**Example:**
```python
validation = validate_terraform_configuration("/path/to/terraform/project")
if validation["data"]["validation_passed"]:
    print("Configuration is valid")
else:
    print(f"Validation errors: {validation['data']['errors']}")
```

### `plan_terraform_changes(project_path: str, environment: str = "production") -> Dict[str, Any]`

Generate a Terraform plan to show proposed infrastructure changes.

**Parameters:**
- `project_path` (str): Path to the Terraform project directory
- `environment` (str): Target environment for the plan

**Returns:**
- `Dict[str, Any]`: Plan results and change analysis

**Example:**
```python
plan = plan_terraform_changes("/path/to/terraform/project", "production")
if plan["status"] == "success":
    print(f"Resources to add: {plan['data']['changes']['resources_to_add']}")
    print(f"Resources to change: {plan['data']['changes']['resources_to_change']}")
```

### `analyze_terraform_state(project_path: str) -> Dict[str, Any]`

Analyze Terraform state file for resource inventory and configuration drift.

**Parameters:**
- `project_path` (str): Path to the Terraform project directory

**Returns:**
- `Dict[str, Any]`: State analysis and resource inventory

**Example:**
```python
state = analyze_terraform_state("/path/to/terraform/project")
if state["status"] == "success":
    print(f"Resource count: {state['data']['resource_count']}")
    print(f"Terraform version: {state['data']['terraform_version']}")
```

### `generate_terraform_optimization_report(analysis_results: Dict[str, Any]) -> Dict[str, Any]`

Generate a comprehensive optimization report for Terraform project analysis.

**Parameters:**
- `analysis_results` (Dict[str, Any]): Results from terraform project analysis

**Returns:**
- `Dict[str, Any]`: Formatted optimization report with recommendations

**Example:**
```python
report = generate_terraform_optimization_report(analysis_result)
if report["status"] == "success":
    print(f"Overall score: {report['data']['overall_score']}/100")
    print(f"Recommendations: {len(report['data']['sections']['recommendations'])}")
```

## 💡 Examples

### Basic Project Analysis

```python
from aws_devops_agent.tools.aws_terraform.terraform_analysis import analyze_terraform_project

# Analyze a Terraform project
result = analyze_terraform_project("/path/to/terraform/project", "production")

if result["status"] == "success":
    data = result["data"]
    
    # Security analysis
    security = data["security"]
    print(f"Security score: {security['overall_security_score']}/100")
    
    for issue in security["security_issues"]:
        if issue["count"] > 0:
            print(f"Security issue: {issue['type']} - {issue['description']}")
    
    # Cost optimization
    cost = data["cost_optimization"]
    print(f"Estimated monthly cost: {cost['estimated_monthly_cost']}")
    print(f"Potential savings: {cost['potential_savings']}")
    
    # Best practices
    best_practices = data["best_practices"]
    print(f"Best practices score: {best_practices['overall_score']}/100")
    
    for violation in best_practices["violations"]:
        print(f"Violation: {violation['practice']} - {violation['description']}")
```

### Configuration Validation

```python
from aws_devops_agent.tools.aws_terraform.terraform_analysis import validate_terraform_configuration

# Validate Terraform configuration
validation = validate_terraform_configuration("/path/to/terraform/project")

if validation["status"] == "success":
    if validation["data"]["validation_passed"]:
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration has errors:")
        print(validation["data"]["errors"])
else:
    print(f"❌ Validation failed: {validation['error']}")
```

### Plan Generation and Analysis

```python
from aws_devops_agent.tools.aws_terraform.terraform_analysis import plan_terraform_changes

# Generate Terraform plan
plan = plan_terraform_changes("/path/to/terraform/project", "production")

if plan["status"] == "success":
    changes = plan["data"]["changes"]
    print(f"Resources to add: {changes['resources_to_add']}")
    print(f"Resources to change: {changes['resources_to_change']}")
    print(f"Resources to destroy: {changes['resources_to_destroy']}")
    
    # Review changes
    if changes["resources_to_add"] > 0:
        print("⚠️  New resources will be created")
    if changes["resources_to_destroy"] > 0:
        print("⚠️  Resources will be destroyed")
else:
    print(f"❌ Plan generation failed: {plan['error']}")
```

### Optimization Report Generation

```python
from aws_devops_agent.tools.aws_terraform.terraform_analysis import (
    analyze_terraform_project,
    generate_terraform_optimization_report
)

# Analyze project
analysis = analyze_terraform_project("/path/to/terraform/project", "production")

if analysis["status"] == "success":
    # Generate optimization report
    report = generate_terraform_optimization_report(analysis)
    
    if report["status"] == "success":
        data = report["data"]
        sections = data["sections"]
        
        print("📊 TERRAFORM OPTIMIZATION REPORT")
        print("=" * 40)
        print()
        
        print("📋 EXECUTIVE SUMMARY:")
        print(sections["executive_summary"])
        print()
        
        print("🔒 SECURITY FINDINGS:")
        print(sections["security_findings"])
        print()
        
        print("💰 COST OPTIMIZATION:")
        print(sections["cost_optimization"])
        print()
        
        print("📋 RECOMMENDATIONS:")
        print(sections["recommendations"])
        print()
        
        print("🎯 NEXT STEPS:")
        print(sections["next_steps"])
```

## 🧪 Testing

### Run Tests

```bash
# Run all Terraform tests
python -m pytest tests/terraform/ -v

# Run specific test file
python -m pytest tests/terraform/test_terraform_analysis.py -v

# Run integration tests
python -m pytest tests/terraform/test_terraform_integration.py -v

# Run simple tests
python tests/terraform/test_terraform_simple.py
```

### Test Categories

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test integration with main agent
- **Mock Tests**: Test with mocked Terraform CLI responses
- **Error Handling Tests**: Test error scenarios and edge cases

### Demo Script

Run the Terraform analysis demo:

```bash
python docs/demos/demo_terraform_analysis.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Terraform CLI Not Found

**Error**: `Terraform CLI not found`

**Solution**: Install Terraform CLI
```bash
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.5.0/terraform_1.5.0_linux_amd64.zip
unzip terraform_1.5.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform version
```

#### 2. Project Path Does Not Exist

**Error**: `Project path does not exist`

**Solution**: Verify the project path is correct
```bash
# Check if path exists
ls -la /path/to/terraform/project

# Use absolute path
python -c "import os; print(os.path.abspath('/path/to/terraform/project'))"
```

#### 3. Terraform Init Failed

**Error**: `Terraform init failed`

**Solution**: Check provider configurations and network connectivity
```bash
# Navigate to project directory
cd /path/to/terraform/project

# Run terraform init manually
terraform init

# Check for errors
terraform init -upgrade
```

#### 4. Configuration Validation Errors

**Error**: `Configuration has errors`

**Solution**: Fix Terraform configuration issues
```bash
# Navigate to project directory
cd /path/to/terraform/project

# Run terraform validate manually
terraform validate

# Check for syntax errors
terraform fmt -check

# Format files
terraform fmt
```

### Debug Mode

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run analysis with debug logging
result = analyze_terraform_project("/path/to/project", "production")
```

### Verbose Output

Use verbose output for detailed information:

```bash
# Run with verbose output
python -m pytest tests/terraform/ -v -s

# Run demo with verbose output
python docs/demos/demo_terraform_analysis.py --verbose
```

## 📊 Performance Considerations

### Optimization Tips

1. **Use Terraform Workspaces**: Organize environments using workspaces
2. **Remote State**: Use remote state for team collaboration
3. **State Locking**: Enable state locking to prevent conflicts
4. **Resource Tagging**: Use consistent tagging for cost analysis
5. **Module Usage**: Use modules for reusable configurations

### Resource Limits

- **State File Size**: Large state files may impact analysis performance
- **Resource Count**: Projects with many resources may take longer to analyze
- **Network Connectivity**: AWS API calls require stable network connection

## 🔗 Related Documentation

- [AWS DevOps Agent Overview](../README_production.md)
- [CDK Analysis](./CDK_ANALYSIS.md)
- [Document Generation](./DOCUMENT_GENERATION.md)
- [Safety Guidelines](./SAFETY_GUIDELINES.md)
- [Quick Setup](../QUICK_SETUP.md)

## 🤝 Contributing

To contribute to Terraform analysis features:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Happy Terraforming! 🏗️✨**
