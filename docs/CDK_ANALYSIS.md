# CDK Analysis Tools

This document describes the CDK (AWS Cloud Development Kit) analysis capabilities added to the AWS DevOps Agent.

## Overview

The CDK analysis tools provide comprehensive analysis of AWS CDK projects, including:

- **Project Structure Analysis**: Analyze CDK project configuration and structure
- **Source Code Analysis**: Detect patterns, security issues, and optimization opportunities
- **Synthesis Support**: Execute `cdk synth` commands and analyze generated CloudFormation templates
- **Cost Optimization**: Identify cost-saving opportunities in CDK code
- **Security Analysis**: Detect security issues and best practice violations
- **Comprehensive Reporting**: Generate detailed optimization reports

## Available Tools

### 1. `analyze_cdk_project(project_path, environment)`

Analyzes a CDK project for best practices, cost optimization, and security issues.

**Parameters:**
- `project_path` (str): Path to CDK project directory
- `environment` (str): Environment type (production, staging, development)

**Returns:**
- Project structure information
- Source code analysis findings
- Cost optimization opportunities
- Security issues
- Best practices violations
- Executive summary

### 2. `synthesize_cdk_project(project_path, context)`

Synthesizes a CDK project to generate CloudFormation templates.

**Parameters:**
- `project_path` (str): Path to CDK project directory
- `context` (dict): CDK context variables (optional)

**Returns:**
- Synthesis status and logs
- Generated template information
- Stack summary statistics

### 3. `analyze_cdk_synthesized_output(cdk_output_path)`

Analyzes synthesized CDK output for cost optimization and security.

**Parameters:**
- `cdk_output_path` (str): Path to CDK output directory (usually cdk.out)

**Returns:**
- CloudFormation template analysis
- Cost analysis with estimates
- Security analysis findings
- Optimization recommendations

### 4. `generate_cdk_optimization_report(project_path, environment)`

Generates a comprehensive CDK optimization report.

**Parameters:**
- `project_path` (str): Path to CDK project directory
- `environment` (str): Environment type

**Returns:**
- Executive summary
- Cost optimization recommendations
- Security recommendations
- Architecture improvements
- Implementation roadmap

## Usage Examples

### Basic Project Analysis

```python
from aws_devops_agent.tools.aws_cdk.cdk_analysis import analyze_cdk_project

# Analyze a CDK project
result = analyze_cdk_project("/path/to/cdk/project", "production")

if result["status"] == "success":
    print(f"Files analyzed: {result['summary']['total_files_analyzed']}")
    print(f"Potential savings: ${result['summary']['potential_monthly_savings']:.2f}/month")
```

### Complete Analysis Workflow

```python
from aws_devops_agent.tools.aws_cdk.cdk_analysis import (
    analyze_cdk_project,
    synthesize_cdk_project,
    generate_cdk_optimization_report
)

# 1. Analyze project structure
analysis = analyze_cdk_project("/path/to/cdk/project", "production")

# 2. Synthesize project (optional)
synthesis = synthesize_cdk_project("/path/to/cdk/project")

# 3. Generate comprehensive report
report = generate_cdk_optimization_report("/path/to/cdk/project", "production")
```

### Using with AWS DevOps Agent

The CDK tools are automatically available in the AWS DevOps Agent:

```python
from aws_devops_agent.main import AWSDevOpsAgentV2

agent = AWSDevOpsAgentV2()

# The agent can now handle CDK-related queries
response = await agent.chat("Analyze my CDK project for optimization opportunities")
```

## Analysis Capabilities

### Cost Optimization Detection

The tools automatically detect:

- **Large Instance Types**: Identifies t3.large, m5.large, etc.
- **Over-provisioned Resources**: Detects resources that may be oversized
- **Missing Reserved Instances**: Identifies opportunities for RI savings
- **Storage Optimization**: Analyzes EBS and S3 configurations

### Security Analysis

Security checks include:

- **Overly Permissive Security Groups**: Detects 0.0.0.0/0 rules
- **Missing Encryption**: Identifies unencrypted resources
- **Public Access**: Detects publicly accessible resources
- **IAM Permissions**: Analyzes IAM role configurations

### Best Practices Validation

Validates against:

- **Resource Tagging**: Ensures consistent tagging strategy
- **Naming Conventions**: Checks resource naming patterns
- **Modularity**: Analyzes stack and construct organization
- **Documentation**: Identifies missing documentation

## Supported CDK Languages

- **TypeScript** (primary)
- **JavaScript**
- **Python**
- **Java**

## Requirements

- AWS CDK CLI installed (`npm install -g aws-cdk`)
- Node.js (for TypeScript/JavaScript projects)
- Python (for Python projects)
- Java (for Java projects)

## Integration with MCP Servers

The CDK analysis tools can be enhanced with real AWS data through MCP servers:

- **Cost Explorer MCP**: Get real cost data for analysis
- **CloudWatch MCP**: Retrieve resource utilization metrics
- **AWS Pricing MCP**: Get current pricing information

## Demo

Run the demo script to see the CDK analysis in action:

```bash
python docs/demos/demo_cdk_analysis.py
```

This will create a sample CDK project and demonstrate all analysis capabilities.

## Future Enhancements

### Remote Repository Support

Planned features include:

- **GitHub Integration**: Clone and analyze CDK projects from GitHub
- **GitLab Support**: Analyze projects from GitLab repositories
- **Branch Analysis**: Compare different branches for changes
- **PR Analysis**: Analyze CDK changes in pull requests

### Advanced Analysis

- **Dependency Analysis**: Map construct dependencies
- **Performance Analysis**: Analyze stack performance characteristics
- **Compliance Checking**: Validate against specific compliance frameworks
- **Migration Analysis**: Analyze migration paths between CDK versions

## Troubleshooting

### Common Issues

1. **CDK Not Found**: Ensure AWS CDK CLI is installed and in PATH
2. **Synthesis Failures**: Check CDK project configuration and dependencies
3. **Permission Issues**: Ensure proper AWS credentials are configured
4. **Memory Issues**: Large projects may require increased memory limits

### Debug Mode

Enable debug mode for detailed logging:

```python
import os
os.environ["DEBUG_MODE"] = "true"
```

## Contributing

To add new CDK analysis capabilities:

1. Add new functions to `cdk_analysis.py`
2. Update the `__init__.py` exports
3. Add tests in `test_cdk_analysis.py`
4. Update this documentation

## Support

For issues or questions about CDK analysis:

1. Check the troubleshooting section
2. Review the test cases for examples
3. Run the demo script to verify functionality
4. Check AWS CDK documentation for project-specific issues
