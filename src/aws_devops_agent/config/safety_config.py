"""
Safety Configuration for AWS DevOps Agent
Critical safety settings to prevent unauthorized actions
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class SafetyConfig:
    """Safety configuration settings"""
    
    # Critical safety settings
    require_explicit_consent_for_prs: bool = True
    require_explicit_consent_for_commits: bool = True
    require_explicit_consent_for_pushes: bool = True
    require_explicit_consent_for_infrastructure_changes: bool = True
    
    # Allowed actions without explicit consent (read-only)
    allowed_readonly_actions: List[str] = None
    
    # Dangerous actions that require explicit consent
    dangerous_actions: List[str] = None
    
    # Safety messages
    consent_required_message: str = "⚠️  CRITICAL: This action requires explicit user consent!"
    safety_warning_message: str = "🔒 SAFETY: This action could modify your infrastructure or code."
    
    def __post_init__(self):
        if self.allowed_readonly_actions is None:
            self.allowed_readonly_actions = [
                "analyze",
                "scan", 
                "check",
                "validate",
                "review",
                "monitor",
                "list",
                "get",
                "read",
                "describe",
                "inspect",
                "examine",
                "assess",
                "evaluate",
                "report",
                "generate_report",
                "prepare_recommendations"
            ]
        
        if self.dangerous_actions is None:
            self.dangerous_actions = [
                "create",
                "update", 
                "modify",
                "delete",
                "deploy",
                "push",
                "commit",
                "merge",
                "publish",
                "execute",
                "run",
                "apply",
                "provision",
                "destroy",
                "terminate",
                "shutdown",
                "restart",
                "scale",
                "migrate",
                "sync",
                "backup",
                "restore"
            ]


def get_safety_config() -> SafetyConfig:
    """Get safety configuration"""
    return SafetyConfig()


def is_dangerous_action(action: str) -> bool:
    """Check if an action is considered dangerous and requires consent"""
    config = get_safety_config()
    action_lower = action.lower()
    
    # Check if action contains dangerous keywords
    for dangerous in config.dangerous_actions:
        if dangerous in action_lower:
            return True
    
    return False


def requires_consent(action: str) -> bool:
    """Check if an action requires explicit user consent"""
    config = get_safety_config()
    action_lower = action.lower()
    
    # Check for dangerous actions
    if is_dangerous_action(action):
        return True
    
    # Check for specific dangerous patterns
    dangerous_patterns = [
        "pull_request",
        "create_pr",
        "push_to",
        "commit_changes",
        "modify_infrastructure",
        "deploy_",
        "update_",
        "change_",
        "alter_"
    ]
    
    for pattern in dangerous_patterns:
        if pattern in action_lower:
            return True
    
    return False


def get_consent_message(action: str) -> str:
    """Get appropriate consent message for an action"""
    config = get_safety_config()
    
    if requires_consent(action):
        return f"{config.consent_required_message}\n{config.safety_warning_message}\n\nAction: {action}\n\nPlease confirm with explicit approval before proceeding."
    
    return ""


def validate_action_safety(action: str, user_consent: bool = False) -> Dict[str, Any]:
    """Validate if an action is safe to proceed"""
    
    if not requires_consent(action):
        return {
            "safe": True,
            "requires_consent": False,
            "message": "Action is safe to proceed (read-only)"
        }
    
    if user_consent:
        return {
            "safe": True,
            "requires_consent": True,
            "consent_given": True,
            "message": "Action approved by user"
        }
    
    return {
        "safe": False,
        "requires_consent": True,
        "consent_given": False,
        "error": "CRITICAL: User consent required!",
        "message": get_consent_message(action),
        "recommendation": "Ask the user for explicit approval before proceeding with this action."
    }


# Safety decorator for functions
def require_consent(func):
    """Decorator to require explicit consent for dangerous functions"""
    def wrapper(*args, **kwargs):
        # Check if user_consent is provided and True
        user_consent = kwargs.get('user_consent', False)
        
        if not user_consent:
            return {
                "status": "error",
                "error": "CRITICAL: User consent required!",
                "safety_message": f"This function ({func.__name__}) requires explicit user approval.",
                "recommendation": "Ask the user for explicit approval before calling this function."
            }
        
        return func(*args, **kwargs)
    
    return wrapper
