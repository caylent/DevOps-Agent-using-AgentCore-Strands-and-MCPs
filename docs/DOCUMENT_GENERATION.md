# 📄 Document Generation - AWS DevOps Agent

## Overview

The AWS DevOps Agent now includes comprehensive document generation capabilities that automatically create and save reports to a `reports/` folder when users request document or report generation.

## 🚀 Features

### Automatic File Creation
- **Reports Folder**: All documents are saved to `reports/` directory
- **Organized Structure**: Documents are automatically organized by type
- **Multiple Formats**: Support for Markdown, JSON, CSV, and Excel formats
- **Timestamped Files**: Automatic timestamping to prevent overwrites

### Document Types
- **Cost Analysis**: Detailed cost optimization reports
- **Security Compliance**: Security and compliance assessment reports
- **Infrastructure**: IaC analysis and best practices reports
- **CDK Analysis**: CDK project analysis and optimization reports
- **General**: Custom documents and reports

## 📁 Folder Structure

```
reports/
├── cost-analysis/          # Cost optimization reports
├── security-compliance/    # Security and compliance reports
├── infrastructure-as-code/ # IaC analysis reports
├── cdk-analysis/          # CDK project reports
├── compliance-reports/    # Compliance framework reports
├── multi-account/         # Multi-account analysis reports
└── general/               # General purpose reports
```

## 🛠️ Available Tools

### 1. `generate_document(content, title, document_type, format, filename)`

Generate and save any type of document.

**Parameters:**
- `content`: Document content (text, JSON data, or structured data)
- `title`: Document title
- `document_type`: Type of document (general, cost, security, iac, cdk, compliance, multi-account)
- `format`: Output format (markdown, json, csv, excel)
- `filename`: Custom filename (auto-generated if None)

**Example:**
```python
result = generate_document(
    content={"summary": "Test report", "findings": ["Finding 1", "Finding 2"]},
    title="Test Report",
    document_type="general",
    format="markdown"
)
```

### 2. `generate_cost_analysis_document(cost_data, title, filename)`

Generate a comprehensive cost analysis document.

**Parameters:**
- `cost_data`: Cost analysis data from cost tools
- `title`: Document title (default: "Cost Analysis Report")
- `filename`: Custom filename (auto-generated if None)

### 3. `generate_security_compliance_document(security_data, title, filename)`

Generate a comprehensive security compliance document.

**Parameters:**
- `security_data`: Security analysis data from security tools
- `title`: Document title (default: "Security Compliance Report")
- `filename`: Custom filename (auto-generated if None)

### 4. `generate_infrastructure_document(iac_data, title, filename)`

Generate a comprehensive infrastructure analysis document.

**Parameters:**
- `iac_data`: Infrastructure analysis data from IaC tools
- `title`: Document title (default: "Infrastructure Analysis Report")
- `filename`: Custom filename (auto-generated if None)

### 5. `generate_cdk_analysis_document(cdk_data, title, filename)`

Generate a comprehensive CDK analysis document.

**Parameters:**
- `cdk_data`: CDK analysis data from CDK tools
- `title`: Document title (default: "CDK Analysis Report")
- `filename`: Custom filename (auto-generated if None)

### 6. `list_generated_documents(document_type, limit)`

List all generated documents in the reports folder.

**Parameters:**
- `document_type`: Filter by document type (optional)
- `limit`: Maximum number of documents to return (default: 20)

### 7. `get_document_info(file_path)`

Get information about a specific document.

**Parameters:**
- `file_path`: Path to the document file

## 💬 Usage Examples

### Basic Document Generation

```
User: "Generate a cost analysis report"
Agent: [Analyzes costs and creates a detailed report in reports/cost-analysis/]
```

### Custom Document

```
User: "Create a security compliance document for my infrastructure"
Agent: [Analyzes security and creates a compliance report in reports/security-compliance/]
```

### CDK Analysis Report

```
User: "Generate a CDK optimization report for my project"
Agent: [Analyzes CDK project and creates an optimization report in reports/cdk-analysis/]
```

### List Generated Documents

```
User: "Show me all the reports I've generated"
Agent: [Lists all documents in the reports folder with details]
```

## 📋 Document Formats

### Markdown (.md)
- **Best for**: Human-readable reports, documentation
- **Features**: Rich formatting, headers, lists, tables
- **Metadata**: YAML frontmatter with generation info

### JSON (.json)
- **Best for**: Machine-readable data, API responses
- **Features**: Structured data, easy to parse
- **Metadata**: Included in the data structure

### CSV (.csv)
- **Best for**: Tabular data, spreadsheet import
- **Features**: Comma-separated values, Excel compatible
- **Use case**: Cost breakdowns, resource lists

### Excel (.xlsx)
- **Best for**: Complex reports with multiple sheets
- **Features**: Multiple worksheets, rich formatting
- **Use case**: Executive reports, detailed analysis

## 🔧 Configuration

### Reports Directory
The reports directory can be configured by modifying the `ReportGenerator` class:

```python
from aws_devops_agent.utils.report_generator import ReportGenerator

# Custom reports directory
report_gen = ReportGenerator(reports_dir="custom_reports")
```

### File Naming
Files are automatically named with timestamps to prevent overwrites:
- Format: `{title}_{YYYYMMDD_HHMMSS}.{extension}`
- Example: `cost_analysis_20250906_192643.md`

## 📊 Document Structure

### Markdown Documents
```markdown
---
title: Document Title
generated_at: 2025-09-06T19:26:43.955348
report_type: cost
file_path: reports/cost-analysis/document.md
format: markdown
---

# Document Title

**Generated:** 2025-09-06 19:26:43

## Executive Summary
[Summary content]

## Detailed Analysis
[Analysis content]
```

### JSON Documents
```json
{
  "report_metadata": {
    "generated_at": "2025-09-06T19:26:43.955348",
    "report_type": "cost",
    "file_path": "reports/cost-analysis/document.json",
    "format": "json"
  },
  "report_data": {
    "executive_summary": {...},
    "detailed_analysis": {...}
  }
}
```

## 🚀 Integration with Agent

The document generation tools are fully integrated with the AWS DevOps Agent:

1. **Automatic Detection**: Agent recognizes document generation requests
2. **Safe Operation**: Document generation is considered safe (no consent required)
3. **Smart Routing**: Agent automatically selects appropriate document type
4. **Rich Content**: Agent populates documents with comprehensive analysis

## 📈 Benefits

### For Users
- **Tangible Outputs**: Get actual files you can share and review
- **Organized Storage**: All reports in one place, organized by type
- **Multiple Formats**: Choose the format that works best for your needs
- **Timestamped**: Never lose previous reports

### For Teams
- **Shareable Reports**: Easy to share with stakeholders
- **Consistent Format**: Standardized report structure
- **Version Control**: Timestamped files for version tracking
- **Integration Ready**: JSON/CSV formats for tool integration

## 🔍 Monitoring and Management

### List Documents
```bash
# List all documents
make query QUERY="Show me all generated documents"

# List specific type
make query QUERY="List all cost analysis reports"
```

### Document Information
```bash
# Get document details
make query QUERY="Get information about reports/cost-analysis/cost_report.md"
```

## 🧪 Testing

Test the document generation functionality:

```bash
# Run document generation test
python test_document_generation.py

# Run enhanced reports demo
python docs/demos/demo_enhanced_reports.py

# Test with agent
make example-report
```

## 📝 Best Practices

### Document Naming
- Use descriptive titles for better organization
- Let the system auto-generate filenames with timestamps
- Use appropriate document types for better categorization

### Content Structure
- Provide structured data for better formatting
- Include executive summaries for quick understanding
- Use consistent terminology across documents

### File Management
- Regularly review and archive old reports
- Use the listing tools to find specific documents
- Consider the appropriate format for your use case

## 🎯 Summary

The document generation feature provides:

- ✅ **Automatic file creation** in organized `reports/` folder
- ✅ **Multiple formats** (Markdown, JSON, CSV, Excel)
- ✅ **Type-based organization** for easy management
- ✅ **Timestamped files** to prevent overwrites
- ✅ **Rich content** with comprehensive analysis
- ✅ **Easy integration** with existing workflows
- ✅ **Safe operation** (no consent required)

**The agent now creates tangible, shareable documents that you can use for reporting, analysis, and team collaboration!** 📄✨
