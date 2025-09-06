# 🔒 Safety Guidelines - AWS DevOps Agent

## Critical Security Measures

This document outlines the comprehensive safety measures implemented in the AWS DevOps Agent to prevent unauthorized actions and ensure user control over all potentially dangerous operations.

## 🚨 CRITICAL SAFETY RULES

### 1. **NEVER Create PRs Without Explicit Consent**
- ❌ **FORBIDDEN**: Automatic PR creation
- ✅ **REQUIRED**: Explicit user approval for any PR creation
- 🔒 **ENFORCED**: All PR functions require `user_consent=True` parameter

### 2. **NEVER Modify Infrastructure Without Permission**
- ❌ **FORBIDDEN**: Automatic infrastructure changes
- ✅ **REQUIRED**: User must explicitly approve all modifications
- 🔒 **ENFORCED**: Safety checks prevent unauthorized actions

### 3. **NEVER Push Code Without Consent**
- ❌ **FORBIDDEN**: Automatic pushes to repositories
- ✅ **REQUIRED**: Explicit approval for any code changes
- 🔒 **ENFORCED**: All write operations require consent

## 🛡️ Safety Implementation

### Function-Level Protection

All dangerous functions now include:

```python
@tool
def dangerous_function(param1: str, user_consent: bool = False) -> Dict[str, Any]:
    """
    ⚠️  CRITICAL: This function requires explicit user consent!
    ⚠️  NEVER call this function without user_consent=True
    """
    # CRITICAL SAFETY CHECK
    if not user_consent:
        return {
            "status": "error",
            "error": "CRITICAL: User consent required!",
            "safety_message": "This function requires explicit user approval.",
            "recommendation": "Ask the user for explicit approval."
        }
    # ... function logic
```

### Message-Level Protection

The agent now checks all incoming messages for dangerous patterns:

```python
dangerous_patterns = [
    "create pull request",
    "create pr", 
    "push to",
    "commit changes",
    "modify infrastructure",
    "deploy",
    "update",
    "change",
    "alter"
]
```

### System Prompt Protection

The system prompt explicitly prohibits automatic actions:

```
IMPORTANTE - REGLAS DE SEGURIDAD CRÍTICAS:
- NUNCA crees PRs, commits, o pushes sin consentimiento explícito del usuario
- SIEMPRE pregunta antes de realizar cualquier acción que modifique código o infraestructura
- Solo proporciona análisis, recomendaciones y preparación de cambios
- Los usuarios deben aprobar explícitamente cualquier acción antes de ejecutarla
```

## 🔍 Protected Functions

### GitHub Integration Functions
- `create_optimization_pull_request()` - Requires `user_consent=True`
- `update_iac_via_github()` - Requires `user_consent=True`
- `create_pull_request()` - Requires `user_consent=True`
- `create_terraform_security_pr()` - Requires `user_consent=True`

### Safety Checks Applied
1. **Parameter Validation**: All dangerous functions check `user_consent` parameter
2. **Message Analysis**: Incoming messages are scanned for dangerous patterns
3. **Function Blocking**: Functions return error if consent not provided
4. **Clear Messaging**: Users receive clear safety warnings and recommendations

## 📋 Safe Operations (No Consent Required)

These operations are considered safe and don't require explicit consent:

- **Analysis**: `analyze_*`, `scan_*`, `check_*`, `validate_*`
- **Monitoring**: `monitor_*`, `list_*`, `get_*`, `read_*`
- **Reporting**: `generate_report`, `prepare_recommendations`
- **Review**: `review_*`, `inspect_*`, `examine_*`

## ⚠️ Dangerous Operations (Consent Required)

These operations require explicit user consent:

- **Creation**: `create_*`, `generate_*` (when modifying)
- **Modification**: `update_*`, `modify_*`, `change_*`, `alter_*`
- **Deployment**: `deploy_*`, `push_*`, `commit_*`
- **Infrastructure**: Any operation that changes AWS resources
- **Code**: Any operation that modifies repository code

## 🚨 Emergency Safety Override

If a dangerous action is detected without consent, the agent will:

1. **Block the action immediately**
2. **Display a clear safety warning**
3. **Ask for explicit user confirmation**
4. **Provide clear instructions for safe operation**

## 🔧 Configuration

Safety settings can be configured in `src/aws_devops_agent/config/safety_config.py`:

```python
@dataclass
class SafetyConfig:
    require_explicit_consent_for_prs: bool = True
    require_explicit_consent_for_commits: bool = True
    require_explicit_consent_for_pushes: bool = True
    require_explicit_consent_for_infrastructure_changes: bool = True
```

## 📖 Usage Examples

### ✅ Safe Usage
```
User: "Analyze my AWS costs"
Agent: [Proceeds safely - analysis only]

User: "Check security compliance for my EC2 instances"
Agent: [Proceeds safely - read-only operation]
```

### ⚠️ Dangerous Usage (Blocked)
```
User: "Create a pull request with cost optimizations"
Agent: 🔒 SAFETY CHECK FAILED
       ⚠️ DANGER: Message contains 'create pull request' which requires explicit user consent!
       Please explicitly confirm this action if you want to proceed.

User: "Deploy my infrastructure changes"
Agent: 🔒 SAFETY CHECK FAILED
       ⚠️ DANGER: Message contains 'deploy' which requires explicit user consent!
       Please explicitly confirm this action if you want to proceed.
```

### ✅ Safe Usage with Consent
```
User: "I want to create a pull request with cost optimizations - I explicitly approve this action"
Agent: [Proceeds with user_consent=True]
```

## 🛠️ Development Guidelines

When adding new functions:

1. **Check if function modifies anything** (code, infrastructure, data)
2. **If yes, add `user_consent: bool = False` parameter**
3. **Add safety check at function start**
4. **Update function documentation with safety warnings**
5. **Test safety behavior thoroughly**

## 🔍 Testing Safety

Run safety tests:

```bash
# Test dangerous message detection
python -c "
from src.aws_devops_agent.main import AWSDevOpsAgentV2
agent = AWSDevOpsAgentV2()
print(agent._check_message_safety('create a pull request'))
"

# Test function safety
python -c "
from src.aws_devops_agent.tools.github.integration import create_optimization_pull_request
result = create_optimization_pull_request('test/repo', 'cost', {}, user_consent=False)
print(result)
"
```

## 📞 Support

If you encounter any safety issues:

1. **Check the safety configuration**
2. **Verify user consent is properly provided**
3. **Review function documentation**
4. **Test with explicit consent parameters**

## 🎯 Summary

The AWS DevOps Agent now implements comprehensive safety measures:

- ✅ **No automatic PR creation**
- ✅ **No automatic infrastructure changes**
- ✅ **No automatic code modifications**
- ✅ **Explicit consent required for all dangerous operations**
- ✅ **Clear safety warnings and recommendations**
- ✅ **Message-level safety checking**
- ✅ **Function-level safety validation**

**Remember: Safety first! Always ask for explicit user consent before performing any potentially dangerous operations.**
