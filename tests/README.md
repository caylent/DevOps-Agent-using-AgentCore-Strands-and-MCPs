# 🧪 AWS DevOps Agent - Test Suite

This directory contains the comprehensive test suite for the AWS DevOps Agent, organized by test type and functionality.

## 📁 Test Organization

### 🏗️ **CDK Tests** (`cdk/`)
Tests for AWS CDK analysis functionality:
- `test_cdk_analysis.py` - Core CDK analysis functions
- `test_cdk_integration.py` - CDK integration with main agent
- `test_cdk_interactive.py` - Interactive CDK testing
- `test_cdk_no_strands.py` - CDK tests without Strands dependency
- `test_cdk_simple.py` - Simple CDK functionality tests
- `test_cdk_standalone.py` - Standalone CDK analysis tests

### 📄 **Document Generation Tests** (`document_generation/`)
Tests for document generation and reporting:
- `test_document_generation.py` - Core document generation functionality
- `test_agent_document_generation.py` - Document generation through agent

### 🔗 **Integration Tests** (`integration/`)
End-to-end integration tests:
- `test_complete_workflow.py` - Complete agent workflow testing
- `test_github_mcp.py` - GitHub MCP integration tests
- `test_mcp_integration.py` - MCP server integration tests
- `test_simple_mcp.py` - Basic MCP functionality tests

### 🧩 **Unit Tests** (`unit/`)
Individual component unit tests:
- `test_aws_devops_agent.py` - Main agent unit tests
- `test_strands_mcp.py` - Strands MCP client tests
- `test_terraform_mcp.py` - Terraform MCP integration tests

### 🚀 **Quick Tests** (Root)
Quick testing and interactive scripts:
- `quick_test.py` - Quick functionality verification
- `interactive_test.py` - Interactive testing interface

## 🧪 Running Tests

### Run All Tests
```bash
# From project root
python -m pytest tests/

# With verbose output
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=src/aws_devops_agent
```

### Run Specific Test Categories
```bash
# CDK tests only
python -m pytest tests/cdk/

# Document generation tests
python -m pytest tests/document_generation/

# Integration tests
python -m pytest tests/integration/

# Unit tests
python -m pytest tests/unit/
```

### Run Individual Tests
```bash
# Specific test file
python -m pytest tests/cdk/test_cdk_analysis.py

# Specific test function
python -m pytest tests/cdk/test_cdk_analysis.py::test_analyze_cdk_project
```

### Quick Testing
```bash
# Quick functionality check
python tests/quick_test.py

# Interactive testing
python tests/interactive_test.py
```

## 📊 Test Categories

### 🏗️ **CDK Tests**
- **Purpose**: Test AWS CDK project analysis and synthesis
- **Coverage**: Project analysis, synthesis, optimization, reporting
- **Dependencies**: CDK CLI (optional), Strands SDK

### 📄 **Document Generation Tests**
- **Purpose**: Test report generation and document creation
- **Coverage**: Markdown, JSON, CSV, Excel report generation
- **Dependencies**: Report generator utilities

### 🔗 **Integration Tests**
- **Purpose**: Test end-to-end workflows and external integrations
- **Coverage**: MCP servers, GitHub integration, complete workflows
- **Dependencies**: AWS credentials, MCP servers

### 🧩 **Unit Tests**
- **Purpose**: Test individual components in isolation
- **Coverage**: Core functions, utilities, client classes
- **Dependencies**: Minimal external dependencies

## 🔧 Test Configuration

### Environment Setup
```bash
# Activate virtual environment
source .venv/bin/activate

# Install test dependencies
pip install -r requirements_dev.txt

# Set up test environment
export AWS_REGION=us-east-1
export LOG_LEVEL=INFO
```

### Test Data
- **Fixtures**: Located in `tests/fixtures/`
- **Mock Data**: Generated during test execution
- **Sample Projects**: Created for CDK testing

## 📈 Test Coverage

### Current Coverage Areas
- ✅ **CDK Analysis**: Project synthesis, analysis, optimization
- ✅ **Document Generation**: Report creation, formatting, organization
- ✅ **MCP Integration**: AWS MCP servers, GitHub integration
- ✅ **Agent Core**: Main agent functionality, tool integration
- ✅ **Safety Features**: Consent requirements, safety checks

### Coverage Goals
- 🎯 **90%+ Code Coverage**: Comprehensive test coverage
- 🎯 **All Critical Paths**: Test all major workflows
- 🎯 **Error Scenarios**: Test error handling and edge cases
- 🎯 **Integration Points**: Test all external integrations

## 🐛 Debugging Tests

### Common Issues
1. **Import Errors**: Ensure you're running from project root
2. **Missing Dependencies**: Install test requirements
3. **AWS Credentials**: Some tests require AWS access
4. **MCP Servers**: Integration tests need MCP servers running

### Debug Commands
```bash
# Run with debug output
python -m pytest tests/ -v -s

# Run specific test with debug
python -m pytest tests/cdk/test_cdk_analysis.py -v -s

# Run with logging
python -m pytest tests/ --log-cli-level=DEBUG
```

## 📝 Adding New Tests

### Test Naming Convention
- **File Names**: `test_<feature_name>.py`
- **Function Names**: `test_<specific_functionality>`
- **Class Names**: `Test<FeatureName>`

### Test Structure
```python
def test_feature_functionality():
    """Test description"""
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result.status == "success"
    assert result.data is not None
```

### Test Categories
- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test performance characteristics

## 🎯 Test Goals

### Quality Assurance
- ✅ **Functionality**: All features work as expected
- ✅ **Reliability**: Tests catch regressions
- ✅ **Performance**: Tests validate performance requirements
- ✅ **Security**: Tests verify safety features

### Development Support
- ✅ **Fast Feedback**: Quick test execution
- ✅ **Clear Failures**: Descriptive error messages
- ✅ **Easy Debugging**: Clear test structure
- ✅ **Maintainable**: Well-organized test code

---

**Happy Testing! 🧪✨**
