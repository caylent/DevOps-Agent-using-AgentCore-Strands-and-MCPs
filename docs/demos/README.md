# 🎯 AWS DevOps Agent - Demo Scripts

This folder contains demonstration scripts that showcase the various capabilities of the AWS DevOps Agent.

## 📁 Available Demos

### 1. `demo_cdk_analysis.py`
**CDK Project Analysis Demo**

Demonstrates the CDK analysis capabilities of the AWS DevOps Agent:
- ✅ **CDK Project Synthesis**: Synthesizes CDK projects to CloudFormation
- ✅ **Project Analysis**: Analyzes CDK project structure and configuration
- ✅ **Real AWS Pricing**: Uses live AWS pricing data via MCP servers
- ✅ **Optimization Recommendations**: Provides cost and security optimization suggestions
- ✅ **Comprehensive Reporting**: Generates detailed analysis reports

**Usage:**
```bash
python docs/demos/demo_cdk_analysis.py
```

**Features Demonstrated:**
- CDK project structure analysis
- CloudFormation template synthesis
- Real-time AWS pricing integration
- Cost optimization recommendations
- Security best practices validation
- Architecture improvement suggestions

### 2. `demo_aws_security_analysis.py`
**AWS Security Analysis Demo**

Comprehensive security analysis using real AWS APIs:
- ✅ **Security Hub**: Real security findings and insights
- ✅ **Config Compliance**: Real compliance status and violations
- ✅ **Inspector Analysis**: Real vulnerability assessments
- ✅ **Trusted Advisor**: Real security recommendations
- ✅ **Comprehensive Analysis**: Combined security posture assessment

**Usage:**
```bash
python docs/demos/demo_aws_security_analysis.py
```

**Features Demonstrated:**
- Real-time security findings from AWS Security Hub
- Compliance validation with AWS Config
- Vulnerability scanning with Amazon Inspector
- Best practices recommendations from Trusted Advisor
- Comprehensive security posture analysis

### 3. `demo_terraform_analysis.py`
**Terraform Analysis Demo**

Complete Terraform project analysis with real AWS integration:
- ✅ **Terraform Plan Analysis**: Real plan parsing and resource extraction
- ✅ **Real AWS Pricing**: Live pricing data via MCP servers
- ✅ **Security Analysis**: Real AWS security APIs integration
- ✅ **Best Practices**: Real validation using AWS services
- ✅ **Cost Optimization**: Detailed cost analysis and recommendations

**Usage:**
```bash
python docs/demos/demo_terraform_analysis.py
```

**Features Demonstrated:**
- Terraform plan parsing and resource analysis
- Real-time AWS pricing for all resources
- Security analysis using AWS Security Hub
- Best practices validation with AWS Config
- Comprehensive cost optimization recommendations

### 4. `demo_enhanced_reports.py`
**Enhanced Document Generation Demo**

Showcases the enhanced document generation capabilities with rich icons and comprehensive content:
- ✅ **Rich Visual Reports**: Reports with 200+ contextual icons
- ✅ **Multiple Report Types**: Cost, Security, Infrastructure, CDK analysis
- ✅ **Comprehensive Content**: Executive summaries, detailed analysis, recommendations
- ✅ **Professional Formatting**: Ready for stakeholder presentation

**Usage:**
```bash
python docs/demos/demo_enhanced_reports.py
```

**Features Demonstrated:**
- Enhanced cost analysis reports with icons
- Security compliance reports with severity categorization
- Infrastructure as Code analysis reports
- CDK project analysis reports
- Document listing and management

### 5. `demo_data_sources_simple.py`
**Data Source Transparency Demo**

Demonstrates clear data source indicators in tool responses:
- ✅ **Data Source Indicators**: Clear indication of data authenticity
- ✅ **Real vs Mock Data**: Easy identification of data sources
- ✅ **Error Transparency**: Even errors show data source context
- ✅ **Consistent Format**: Standardized indicators across all tools

**Usage:**
```bash
python docs/demos/demo_data_sources_simple.py
```

**Features Demonstrated:**
- Data source indicators in all tool responses
- Clear distinction between real AWS data and mock data
- Error case transparency
- Consistent data source formatting

## 🚀 Quick Start

### Prerequisites
1. **Virtual Environment**: Ensure you're in the project's virtual environment
   ```bash
   source .venv/bin/activate
   ```

2. **Dependencies**: All required dependencies should be installed
   ```bash
   pip install -r requirements.txt
   ```

### Running Demos

#### CDK Analysis Demo
```bash
# Run CDK analysis demonstration
python docs/demos/demo_cdk_analysis.py
```

#### AWS Security Analysis Demo
```bash
# Run comprehensive security analysis demonstration
python docs/demos/demo_aws_security_analysis.py
```

#### Terraform Analysis Demo
```bash
# Run Terraform analysis demonstration
python docs/demos/demo_terraform_analysis.py
```

#### Enhanced Reports Demo
```bash
# Run enhanced document generation demonstration
python docs/demos/demo_enhanced_reports.py
```

#### Data Sources Demo
```bash
# Run data source transparency demonstration
python docs/demos/demo_data_sources_simple.py
```

## 📊 Expected Outputs

### CDK Analysis Demo
- **Console Output**: Step-by-step analysis process with real AWS pricing
- **Generated Reports**: CDK analysis reports in `reports/cdk-analysis/`
- **Analysis Results**: Detailed findings and recommendations with real data

### AWS Security Analysis Demo
- **Console Output**: Real-time security analysis from AWS APIs
- **Generated Reports**: Security analysis reports in `reports/security-compliance/`
- **Analysis Results**: Real security findings and compliance status

### Terraform Analysis Demo
- **Console Output**: Terraform plan analysis with real AWS integration
- **Generated Reports**: Terraform analysis reports in `reports/terraform-analysis/`
- **Analysis Results**: Real pricing data and security analysis

### Enhanced Reports Demo
- **Console Output**: Demo progress and results
- **Generated Reports**: Multiple report types in organized folders
- **Visual Confirmation**: Rich, icon-enhanced reports

### Data Sources Demo
- **Console Output**: Data source indicators for different tool types
- **Analysis Results**: Clear indication of real vs mock data sources

## 📁 Generated Files

After running the demos, you'll find generated reports in:

```
reports/
├── cdk-analysis/          # CDK project analysis reports
├── cost-analysis/         # Cost optimization reports
├── security-compliance/   # Security and compliance reports
├── infrastructure-as-code/ # IaC analysis reports
├── compliance-reports/    # Compliance framework reports
├── multi-account/         # Multi-account analysis reports
└── general/               # General purpose reports
```

## 🔧 Customization

### Modifying Demo Data
Each demo uses sample data that you can customize:

- **CDK Demo**: Modify the `project_path` variable to point to your CDK project
- **Reports Demo**: Update the sample data dictionaries to reflect your infrastructure

### Adding New Demos
To add new demonstration scripts:

1. Create a new Python file in this directory
2. Follow the naming convention: `demo_<feature_name>.py`
3. Include comprehensive docstrings and comments
4. Update this README with the new demo information

## 📚 Related Documentation

- [CDK Analysis Documentation](../CDK_ANALYSIS.md)
- [Document Generation Documentation](../DOCUMENT_GENERATION.md)
- [Safety Guidelines](../SAFETY_GUIDELINES.md)
- [App Usage Guide](../APP_USAGE.md)

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root directory
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Permission Errors**: Check file permissions for the reports directory
4. **AWS Credentials**: Some demos may require AWS credentials for full functionality

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your Python environment and dependencies
3. Ensure you're running from the correct directory
4. Check the main project documentation

## 🎯 Demo Goals

These demos are designed to:
- **Showcase Capabilities**: Demonstrate the full range of agent features
- **Provide Examples**: Show how to use the agent programmatically
- **Generate Sample Reports**: Create example reports for reference
- **Validate Functionality**: Ensure all features work as expected
- **Guide Users**: Help users understand how to use the agent effectively

---

**Happy Demo-ing! 🚀✨**
