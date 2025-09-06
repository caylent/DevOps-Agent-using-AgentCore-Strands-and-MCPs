"""
AWS CDK Analysis Tools
CDK project analysis, synthesis, and optimization recommendations
"""

import json
import os
import subprocess
import tempfile
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from strands import tool


@tool
def analyze_cdk_project(project_path: str, environment: str = "production") -> Dict[str, Any]:
    """
    Analyze a CDK project for best practices, cost optimization, and security
    
    Args:
        project_path: Path to CDK project directory
        environment: Environment type (production, staging, development)
    
    Returns:
        Dict containing CDK project analysis results and recommendations
    """
    try:
        # Validate project path
        if not os.path.exists(project_path):
            return {"status": "error", "error": f"Project path not found: {project_path}"}
        
        # Check if it's a valid CDK project
        cdk_json_path = os.path.join(project_path, "cdk.json")
        if not os.path.exists(cdk_json_path):
            return {"status": "error", "error": "Not a valid CDK project - cdk.json not found"}
        
        analysis_results = {
            "status": "success",
            "project_path": project_path,
            "environment": environment,
            "analysis_timestamp": datetime.now().isoformat(),
            "project_info": {},
            "findings": [],
            "recommendations": [],
            "cost_optimization_opportunities": [],
            "security_issues": [],
            "best_practices_violations": []
        }
        
        # Analyze CDK project structure
        project_info = _analyze_cdk_project_structure(project_path)
        analysis_results["project_info"] = project_info
        
        # Find and analyze CDK source files
        cdk_files = _find_cdk_source_files(project_path)
        
        for cdk_file in cdk_files:
            file_analysis = _analyze_cdk_file(cdk_file, environment)
            analysis_results["findings"].extend(file_analysis.get("findings", []))
            analysis_results["recommendations"].extend(file_analysis.get("recommendations", []))
            analysis_results["cost_optimization_opportunities"].extend(file_analysis.get("cost_optimizations", []))
            analysis_results["security_issues"].extend(file_analysis.get("security_issues", []))
            analysis_results["best_practices_violations"].extend(file_analysis.get("best_practices", []))
        
        # Generate summary
        analysis_results["summary"] = {
            "total_files_analyzed": len(cdk_files),
            "total_findings": len(analysis_results["findings"]),
            "total_recommendations": len(analysis_results["recommendations"]),
            "critical_security_issues": len([i for i in analysis_results["security_issues"] if i.get("severity") == "critical"]),
            "potential_monthly_savings": sum([opp.get("monthly_savings", 0) for opp in analysis_results["cost_optimization_opportunities"]])
        }
        
        return analysis_results
        
    except Exception as e:
        return {"status": "error", "error": f"CDK project analysis failed: {str(e)}"}


@tool
def synthesize_cdk_project(project_path: str, context: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Synthesize a CDK project to generate CloudFormation templates
    
    Args:
        project_path: Path to CDK project directory
        context: CDK context variables (optional)
    
    Returns:
        Dict containing synthesis results and generated templates
    """
    try:
        if not os.path.exists(project_path):
            return {"status": "error", "error": f"Project path not found: {project_path}"}
        
        # Change to project directory
        original_cwd = os.getcwd()
        os.chdir(project_path)
        
        try:
            # Prepare CDK synth command
            cmd = ["cdk", "synth", "--quiet", "--output", "cdk.out"]
            
            # Add context variables if provided
            if context:
                for key, value in context.items():
                    cmd.extend(["--context", f"{key}={value}"])
            
            # Run CDK synth
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                return {
                    "status": "error", 
                    "error": f"CDK synthesis failed: {result.stderr}",
                    "stdout": result.stdout
                }
            
            # Analyze generated templates
            cdk_out_path = os.path.join(project_path, "cdk.out")
            synthesis_results = {
                "status": "success",
                "project_path": project_path,
                "synthesis_timestamp": datetime.now().isoformat(),
                "cdk_output_path": cdk_out_path,
                "generated_templates": [],
                "stack_summary": {},
                "synthesis_logs": result.stdout
            }
            
            if os.path.exists(cdk_out_path):
                templates = _analyze_synthesized_templates(cdk_out_path)
                synthesis_results["generated_templates"] = templates
                synthesis_results["stack_summary"] = _generate_stack_summary(templates)
            
            return synthesis_results
            
        finally:
            os.chdir(original_cwd)
            
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "CDK synthesis timed out after 5 minutes"}
    except Exception as e:
        return {"status": "error", "error": f"CDK synthesis failed: {str(e)}"}


@tool
def analyze_cdk_synthesized_output(cdk_output_path: str) -> Dict[str, Any]:
    """
    Analyze synthesized CDK output for cost optimization and security
    
    Args:
        cdk_output_path: Path to CDK output directory (usually cdk.out)
    
    Returns:
        Dict containing analysis of synthesized CloudFormation templates
    """
    try:
        if not os.path.exists(cdk_output_path):
            return {"status": "error", "error": f"CDK output path not found: {cdk_output_path}"}
        
        analysis_results = {
            "status": "success",
            "cdk_output_path": cdk_output_path,
            "analysis_timestamp": datetime.now().isoformat(),
            "templates_analyzed": [],
            "cost_analysis": {},
            "security_analysis": {},
            "recommendations": []
        }
        
        # Find all CloudFormation templates
        template_files = list(Path(cdk_output_path).rglob("*.template.json"))
        
        for template_file in template_files:
            template_analysis = _analyze_cloudformation_template_file(template_file)
            analysis_results["templates_analyzed"].append(template_analysis)
        
        # Generate overall analysis
        analysis_results["cost_analysis"] = _generate_cost_analysis(analysis_results["templates_analyzed"])
        analysis_results["security_analysis"] = _generate_security_analysis(analysis_results["templates_analyzed"])
        analysis_results["recommendations"] = _generate_cdk_recommendations(analysis_results["templates_analyzed"])
        
        return analysis_results
        
    except Exception as e:
        return {"status": "error", "error": f"CDK synthesized output analysis failed: {str(e)}"}


@tool
def generate_cdk_optimization_report(project_path: str, environment: str = "production") -> Dict[str, Any]:
    """
    Generate comprehensive CDK optimization report with cost and security recommendations
    
    Args:
        project_path: Path to CDK project directory
        environment: Environment type (production, staging, development)
    
    Returns:
        Dict containing comprehensive optimization report
    """
    try:
        # First synthesize the project
        synth_result = synthesize_cdk_project(project_path)
        if synth_result["status"] != "success":
            return synth_result
        
        # Analyze the synthesized output
        cdk_out_path = synth_result["cdk_output_path"]
        analysis_result = analyze_cdk_synthesized_output(cdk_out_path)
        if analysis_result["status"] != "success":
            return analysis_result
        
        # Generate comprehensive report
        report = {
            "status": "success",
            "project_path": project_path,
            "environment": environment,
            "report_timestamp": datetime.now().isoformat(),
            "executive_summary": {},
            "cost_optimization": {},
            "security_recommendations": {},
            "architecture_improvements": {},
            "implementation_roadmap": []
        }
        
        # Generate executive summary
        report["executive_summary"] = _generate_executive_summary(synth_result, analysis_result)
        
        # Generate cost optimization section
        report["cost_optimization"] = _generate_cost_optimization_section(analysis_result)
        
        # Generate security recommendations
        report["security_recommendations"] = _generate_security_recommendations_section(analysis_result)
        
        # Generate architecture improvements
        report["architecture_improvements"] = _generate_architecture_improvements(analysis_result)
        
        # Generate implementation roadmap
        report["implementation_roadmap"] = _generate_implementation_roadmap(analysis_result)
        
        return report
        
    except Exception as e:
        return {"status": "error", "error": f"CDK optimization report generation failed: {str(e)}"}


# Helper functions
def _analyze_cdk_project_structure(project_path: str) -> Dict[str, Any]:
    """Analyze CDK project structure and configuration"""
    project_info = {
        "cdk_version": "unknown",
        "language": "unknown",
        "stacks_count": 0,
        "constructs_count": 0,
        "dependencies": []
    }
    
    # Read cdk.json
    cdk_json_path = os.path.join(project_path, "cdk.json")
    try:
        with open(cdk_json_path, 'r') as f:
            cdk_config = json.load(f)
            project_info["cdk_version"] = cdk_config.get("version", "unknown")
            project_info["language"] = cdk_config.get("language", "unknown")
    except Exception:
        pass
    
    # Count TypeScript/JavaScript files
    ts_files = list(Path(project_path).rglob("*.ts"))
    js_files = list(Path(project_path).rglob("*.js"))
    py_files = list(Path(project_path).rglob("*.py"))
    java_files = list(Path(project_path).rglob("*.java"))
    
    if ts_files:
        project_info["language"] = "typescript"
    elif js_files:
        project_info["language"] = "javascript"
    elif py_files:
        project_info["language"] = "python"
    elif java_files:
        project_info["language"] = "java"
    
    return project_info


def _find_cdk_source_files(project_path: str) -> List[str]:
    """Find CDK source files in the project"""
    cdk_files = []
    
    # Look for common CDK file patterns
    patterns = ["*.ts", "*.js", "*.py", "*.java"]
    
    for pattern in patterns:
        files = list(Path(project_path).rglob(pattern))
        for file_path in files:
            # Skip node_modules, .git, and other common directories
            if any(skip in str(file_path) for skip in ["node_modules", ".git", "cdk.out", "dist", "build"]):
                continue
            cdk_files.append(str(file_path))
    
    return cdk_files


def _analyze_cdk_file(file_path: str, environment: str) -> Dict[str, Any]:
    """Analyze individual CDK file for patterns and issues"""
    analysis = {
        "findings": [],
        "recommendations": [],
        "cost_optimizations": [],
        "security_issues": [],
        "best_practices": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for common CDK patterns and issues
        if "new ec2.Instance" in content or "ec2.Instance" in content:
            # Check for instance type optimization
            if "t3.large" in content or "m5.large" in content:
                analysis["cost_optimizations"].append({
                    "file": os.path.basename(file_path),
                    "resource_type": "EC2 Instance",
                    "issue": "Large instance type detected",
                    "recommendation": "Consider using smaller instance types if workload permits",
                    "monthly_savings": 50.0,
                    "priority": "medium"
                })
        
        # Check for security group configurations
        if "SecurityGroup" in content and "0.0.0.0/0" in content:
            analysis["security_issues"].append({
                "file": os.path.basename(file_path),
                "resource_type": "Security Group",
                "issue": "Overly permissive security group rule",
                "recommendation": "Restrict source IP ranges to minimum required",
                "severity": "high",
                "priority": "critical"
            })
        
        # Check for missing tags
        if "new " in content and "tags" not in content.lower():
            analysis["best_practices"].append({
                "file": os.path.basename(file_path),
                "issue": "Missing resource tags",
                "recommendation": "Add consistent tagging for resource management and cost allocation",
                "priority": "medium"
            })
            
    except Exception as e:
        analysis["findings"].append({
            "file": os.path.basename(file_path),
            "type": "error",
            "message": f"Failed to analyze file: {str(e)}"
        })
    
    return analysis


def _analyze_synthesized_templates(cdk_out_path: str) -> List[Dict[str, Any]]:
    """Analyze synthesized CloudFormation templates"""
    templates = []
    
    for template_file in Path(cdk_out_path).rglob("*.template.json"):
        try:
            with open(template_file, 'r') as f:
                template = json.load(f)
                
            template_info = {
                "file_name": template_file.name,
                "file_path": str(template_file),
                "resources_count": len(template.get("Resources", {})),
                "parameters_count": len(template.get("Parameters", {})),
                "outputs_count": len(template.get("Outputs", {})),
                "template_size_kb": template_file.stat().st_size / 1024
            }
            
            templates.append(template_info)
            
        except Exception as e:
            templates.append({
                "file_name": template_file.name,
                "error": f"Failed to parse template: {str(e)}"
            })
    
    return templates


def _generate_stack_summary(templates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary of all stacks"""
    total_resources = sum(t.get("resources_count", 0) for t in templates)
    total_parameters = sum(t.get("parameters_count", 0) for t in templates)
    total_outputs = sum(t.get("outputs_count", 0) for t in templates)
    
    return {
        "total_stacks": len(templates),
        "total_resources": total_resources,
        "total_parameters": total_parameters,
        "total_outputs": total_outputs,
        "average_resources_per_stack": total_resources / len(templates) if templates else 0
    }


def _analyze_cloudformation_template_file(template_file: Path) -> Dict[str, Any]:
    """Analyze individual CloudFormation template file"""
    try:
        with open(template_file, 'r') as f:
            template = json.load(f)
        
        analysis = {
            "file_name": template_file.name,
            "resources": {},
            "cost_estimates": {},
            "security_findings": [],
            "best_practices": []
        }
        
        resources = template.get("Resources", {})
        
        # Analyze each resource
        for resource_name, resource_config in resources.items():
            resource_type = resource_config.get("Type", "")
            properties = resource_config.get("Properties", {})
            
            # EC2 Instance analysis
            if resource_type == "AWS::EC2::Instance":
                instance_type = properties.get("InstanceType", "")
                analysis["resources"][resource_name] = {
                    "type": resource_type,
                    "instance_type": instance_type,
                    "estimated_monthly_cost": _estimate_ec2_cost(instance_type)
                }
            
            # Security Group analysis
            elif resource_type == "AWS::EC2::SecurityGroup":
                analysis["security_findings"].extend(_analyze_security_group(resource_name, properties))
        
        return analysis
        
    except Exception as e:
        return {
            "file_name": template_file.name,
            "error": f"Failed to analyze template: {str(e)}"
        }


def _estimate_ec2_cost(instance_type: str) -> float:
    """Estimate monthly cost for EC2 instance type"""
    # Simplified cost estimation (in reality, this would use AWS Pricing API)
    cost_map = {
        "t3.micro": 8.0,
        "t3.small": 16.0,
        "t3.medium": 32.0,
        "t3.large": 64.0,
        "m5.large": 80.0,
        "m5.xlarge": 160.0
    }
    return cost_map.get(instance_type, 50.0)  # Default estimate


def _analyze_security_group(resource_name: str, properties: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyze security group for security issues"""
    findings = []
    
    ingress_rules = properties.get("SecurityGroupIngress", [])
    for rule in ingress_rules:
        if rule.get("CidrIp") == "0.0.0.0/0":
            findings.append({
                "resource": resource_name,
                "issue": "Overly permissive inbound rule",
                "severity": "high",
                "recommendation": "Restrict source IP range"
            })
    
    return findings


def _generate_cost_analysis(templates_analyzed: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate cost analysis from templates"""
    total_estimated_cost = 0
    resource_costs = []
    
    for template in templates_analyzed:
        if "error" in template:
            continue
            
        for resource_name, resource_info in template.get("resources", {}).items():
            if "estimated_monthly_cost" in resource_info:
                cost = resource_info["estimated_monthly_cost"]
                total_estimated_cost += cost
                resource_costs.append({
                    "resource": resource_name,
                    "type": resource_info.get("type", "Unknown"),
                    "monthly_cost": cost
                })
    
    return {
        "total_estimated_monthly_cost": total_estimated_cost,
        "resource_costs": resource_costs,
        "cost_optimization_opportunities": _identify_cost_optimization_opportunities(resource_costs)
    }


def _generate_security_analysis(templates_analyzed: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate security analysis from templates"""
    all_security_findings = []
    
    for template in templates_analyzed:
        if "error" in template:
            continue
        all_security_findings.extend(template.get("security_findings", []))
    
    return {
        "total_security_findings": len(all_security_findings),
        "critical_findings": [f for f in all_security_findings if f.get("severity") == "high"],
        "security_findings": all_security_findings
    }


def _generate_cdk_recommendations(templates_analyzed: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate CDK-specific recommendations"""
    recommendations = []
    
    # Cost optimization recommendations
    recommendations.append({
        "category": "cost_optimization",
        "priority": "high",
        "title": "Consider using smaller instance types",
        "description": "Review instance types and consider downsizing if workload permits",
        "potential_savings": "$100-500/month"
    })
    
    # Security recommendations
    recommendations.append({
        "category": "security",
        "priority": "critical",
        "title": "Review security group rules",
        "description": "Ensure security groups follow least privilege principle",
        "action_required": "Immediate review needed"
    })
    
    return recommendations


def _identify_cost_optimization_opportunities(resource_costs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identify cost optimization opportunities"""
    opportunities = []
    
    for resource in resource_costs:
        if resource["monthly_cost"] > 100:  # High cost resources
            opportunities.append({
                "resource": resource["resource"],
                "current_cost": resource["monthly_cost"],
                "optimization": "Consider right-sizing or using reserved instances",
                "potential_savings": resource["monthly_cost"] * 0.3  # 30% savings estimate
            })
    
    return opportunities


def _generate_executive_summary(synth_result: Dict[str, Any], analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate executive summary"""
    return {
        "total_stacks": len(synth_result.get("generated_templates", [])),
        "total_resources": sum(t.get("resources_count", 0) for t in synth_result.get("generated_templates", [])),
        "estimated_monthly_cost": analysis_result.get("cost_analysis", {}).get("total_estimated_monthly_cost", 0),
        "security_findings": analysis_result.get("security_analysis", {}).get("total_security_findings", 0),
        "key_recommendations": len(analysis_result.get("recommendations", []))
    }


def _generate_cost_optimization_section(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate cost optimization section"""
    cost_analysis = analysis_result.get("cost_analysis", {})
    return {
        "current_estimated_cost": cost_analysis.get("total_estimated_monthly_cost", 0),
        "optimization_opportunities": cost_analysis.get("cost_optimization_opportunities", []),
        "potential_savings": sum(opp.get("potential_savings", 0) for opp in cost_analysis.get("cost_optimization_opportunities", []))
    }


def _generate_security_recommendations_section(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate security recommendations section"""
    security_analysis = analysis_result.get("security_analysis", {})
    return {
        "total_findings": security_analysis.get("total_security_findings", 0),
        "critical_findings": security_analysis.get("critical_findings", []),
        "recommendations": [
            "Implement least privilege security group rules",
            "Enable VPC Flow Logs for monitoring",
            "Use AWS Config for compliance monitoring"
        ]
    }


def _generate_architecture_improvements(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """Generate architecture improvements"""
    return {
        "modularity": "Consider breaking down large stacks into smaller, focused stacks",
        "reusability": "Extract common patterns into CDK constructs",
        "testing": "Implement CDK unit tests for critical infrastructure",
        "documentation": "Add comprehensive documentation for all stacks and constructs"
    }


def _generate_implementation_roadmap(analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate implementation roadmap"""
    return [
        {
            "phase": 1,
            "title": "Security Hardening",
            "duration": "1-2 weeks",
            "priority": "critical",
            "tasks": ["Review and fix security group rules", "Implement least privilege access"]
        },
        {
            "phase": 2,
            "title": "Cost Optimization",
            "duration": "2-3 weeks", 
            "priority": "high",
            "tasks": ["Right-size instances", "Implement reserved instances", "Review storage costs"]
        },
        {
            "phase": 3,
            "title": "Architecture Improvements",
            "duration": "3-4 weeks",
            "priority": "medium",
            "tasks": ["Modularize stacks", "Add comprehensive testing", "Improve documentation"]
        }
    ]
