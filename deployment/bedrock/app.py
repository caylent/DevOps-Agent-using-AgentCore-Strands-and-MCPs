#!/usr/bin/env python3
"""
AWS DevOps Agent using Strands + Bedrock Agent Core
Production-ready agent for cost optimization, IaC analysis, and compliance validation
"""

import sys
import os
from pathlib import Path

# Add project paths for modern src/ layout
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Import our AWS DevOps tools from new structure
from aws_devops_agent.tools import *
from aws_devops_agent.config import get_config

# Import specific tools that might not be in __init__.py
from aws_devops_agent.tools.aws_cost.optimization import get_cost_forecast_mcp, compare_cost_periods_mcp
from aws_devops_agent.tools.aws_cost.resources import scan_live_aws_resources, analyze_unused_resources, get_resource_utilization_metrics, discover_cross_account_resources
from aws_devops_agent.tools.aws_cost.multi_account import list_cross_account_resources, execute_cross_account_operation, monitor_cross_account_compliance
from aws_devops_agent.tools.github.integration import update_iac_via_github, list_infrastructure_repositories, monitor_infrastructure_prs

# Load configuration from environment variables
import os
from pathlib import Path

# Import centralized environment configuration
from aws_devops_agent.config.env_config import load_env_file, get_env_config

# Load .env file
load_env_file()

# Get environment configuration with strict validation for production
try:
    env_config = get_env_config(strict_validation=True)
    print("✅ Environment configuration loaded successfully")
    print(f"   AWS Region: {env_config.aws_region}")
    print(f"   Model ID: {env_config.bedrock_model_id}")
    print(f"   Server: {env_config.host}:{env_config.port}")
    
    # Show any configuration warnings
    warnings = env_config.validate_configuration()
    if warnings:
        print("\n⚠️  Configuration warnings:")
        for warning in warnings:
            print(f"   - {warning}")
    
except EnvironmentError as e:
    print("🚨 CRITICAL: Environment configuration failed")
    print("=" * 60)
    print(str(e))
    print("\n🔒 DEPLOYMENT BLOCKED - No defaults will be used for safety")
    print("\n💡 Required Actions:")
    print("  1. Set system environment variables:")
    print("     export AWS_REGION=us-east-1")
    print("     export BEDROCK_MODEL_ID=claude-3.5-sonnet")
    print("     export PORT=8080")
    print("     export HOST=0.0.0.0")
    print("\n  2. Or create a .env file in deployment/bedrock/")
    print("     make agentcore-env-dev    # for development")
    print("     make agentcore-env-prod   # for production")
    print("\n  3. Verify configuration before deployment:")
    print("     make agentcore-configure")
    print("\n⚠️  This prevents accidental deployments with wrong settings!")
    exit(1)

# Get model ID from centralized config
model_id = env_config.get_model_id()

# Create the Strands agent
agent = Agent(
    model=model_id,
    tools=[
        # Cost Optimization Tools (AWS Pricing API)
        get_real_aws_pricing,
        analyze_price_optimization_opportunities,
        generate_cost_comparison_report,
        calculate_reserved_instance_savings,
        compare_instance_types,
        compare_pricing_models,
        compare_regions_pricing,
        suggest_cost_effective_alternatives,
        calculate_savings_potential,
        
        # Cost Explorer Tools (Real AWS Data via MCP)
        get_actual_aws_costs,
        get_cost_by_service,
        get_cost_trends,
        get_rightsizing_recommendations,
        get_reserved_instance_recommendations,
        analyze_cost_anomalies,
        analyze_usage_based_optimization,
        get_underutilized_resources,
        calculate_wasted_spend,
        generate_cost_optimization_report,
        get_cost_forecast_mcp,
        compare_cost_periods_mcp,
        
        # Live AWS Resources Tools
        scan_live_aws_resources,
        analyze_unused_resources,
        get_resource_utilization_metrics,
        discover_cross_account_resources,
        analyze_resource_costs,
        get_unused_resources,
        calculate_resource_utilization,
        
        # Infrastructure as Code Tools
        analyze_terraform_configuration,
        validate_cloudformation_template,
        scan_infrastructure_drift,
        generate_iac_best_practices_report,
        
        # CDK Analysis Tools
        analyze_cdk_project,
        synthesize_cdk_project,
        analyze_cdk_synthesized_output,
        generate_cdk_optimization_report,
        
        # Terraform Analysis Tools
        analyze_terraform_project,
        validate_terraform_configuration,
        plan_terraform_changes,
        analyze_terraform_state,
        generate_terraform_optimization_report,
        
        # Compliance and Security Tools
        validate_security_policies,
        check_compliance_standards,
        generate_compliance_report,
        scan_security_vulnerabilities,
        analyze_security_hub_findings,
        get_security_insights,
        analyze_security_posture,
        analyze_config_compliance,
        get_compliance_details,
        check_resource_compliance,
        analyze_inspector_findings,
        
        # Multi-Account Management Tools
        get_organization_costs,
        analyze_account_costs,
        generate_multi_account_report,
        list_cross_account_resources,
        execute_cross_account_operation,
        monitor_cross_account_compliance,
        
        # GitHub Integration Tools
        create_optimization_pull_request,
        update_iac_via_github,
        list_infrastructure_repositories,
        monitor_infrastructure_prs,
        
        # Document Generation Tools
        generate_document,
        generate_cost_analysis_document,
        generate_security_compliance_document,
        generate_infrastructure_document,
        generate_cdk_analysis_document,
        generate_terraform_analysis_document,
        list_generated_documents,
        get_document_info,
    ],
    system_prompt="""Eres un especialista en AWS DevOps desplegado en Bedrock Agent Core con acceso completo a APIs reales de AWS via servidores MCP.

TUS CAPACIDADES PRINCIPALES:
💰 OPTIMIZACIÓN DE COSTOS:
- Análisis de precios en tiempo real via AWS Pricing API
- Acceso REAL a AWS Cost Explorer con datos de facturación actuales
- Análisis de tendencias y breakdowns multi-cuenta via Cost Explorer API
- Recomendaciones de rightsizing y Reserved Instances basadas en datos reales
- Escaneo de recursos vivos para identificar recursos sin usar
- Métricas de utilización en tiempo real de todos los servicios AWS
- Análisis de anomalías de costos y optimización basada en uso
- Comparación de modelos de precios y regiones

🏗️ ANÁLISIS DE INFRAESTRUCTURA COMO CÓDIGO (IaC):
- Validación de configuraciones Terraform y CloudFormation
- Análisis completo de proyectos CDK con síntesis y optimización
- Detección de drift entre código y estado real
- Best practices y recomendaciones de seguridad
- Análisis de cumplimiento de estándares
- Planificación y análisis de cambios de Terraform

🔒 SEGURIDAD Y COMPLIANCE:
- Validación contra estándares SOC2, HIPAA, PCI-DSS, ISO27001
- Escaneo de vulnerabilidades de seguridad via Security Hub
- Análisis de políticas y configuraciones
- Reportes de compliance ejecutivos
- Análisis de Inspector y Config Compliance
- Insights de seguridad y postura de seguridad

🌐 GESTIÓN MULTI-CUENTA:
- Operaciones cross-account en organizaciones AWS
- Inventario de recursos en múltiples cuentas y regiones
- Análisis de costos organizacional
- Monitoreo de compliance centralizado
- Ejecución de operaciones en múltiples cuentas

📱 INTEGRACIÓN GITHUB:
- Generación automática de Pull Requests con optimizaciones
- Gestión de repositorios de infraestructura
- Automatización de CI/CD para IaC
- Monitoring de PRs de infraestructura

📄 GENERACIÓN DE DOCUMENTOS:
- Reportes ejecutivos de análisis de costos
- Documentos de compliance y seguridad
- Análisis de infraestructura y CDK
- Documentación de optimizaciones de Terraform

FLUJO DE TRABAJO CONVERSACIONAL:
1. Analiza la consulta del usuario en español/inglés
2. Determina qué herramientas usar y en qué secuencia
3. Ejecuta análisis usando datos reales de AWS via MCP
4. Combina resultados en una respuesta integral
5. Genera PRs automáticos cuando sea apropiado
6. Proporciona next steps accionables

IMPORTANTE:
- Siempre especifica que los datos provienen de APIs reales de AWS via MCP servers
- Incluye números específicos y ahorros en dólares
- Genera PRs automáticamente para cambios seguros
- Proporciona executive summaries para stakeholders
- Mantén foco en ROI y value delivery

Responde de manera concisa pero completa, integrando múltiples fuentes de datos en un análisis coherente.""",
    name="AWS DevOps Agent",
    description="Production AWS DevOps agent for cost optimization, IaC analysis, compliance validation, and automated infrastructure improvements",
)

# Create the Bedrock Agent Core app with environment configuration
app = BedrockAgentCoreApp(debug=env_config.debug_mode)


@app.entrypoint
def invoke(payload):
    """Process user input and return a response"""
    print(f"📥 Received AWS DevOps payload: {payload}")

    # Extract user message
    user_message = payload.get("prompt", "")
    if not user_message:
        user_message = payload.get("inputText", "")
    if not user_message:
        user_message = payload.get("query", "Analyze AWS infrastructure and provide optimization recommendations")

    print(f"💬 AWS DevOps query: {user_message}")

    try:
        # Process with Strands agent
        response = agent(user_message)
        print(f"🤖 AWS DevOps Agent response: {response}")

        # Return JSON serializable response
        if isinstance(response, str):
            return {
                "response": response,
                "status": "success",
                "agent": "AWS DevOps Agent",
                "capabilities": [
                    "Real-time AWS cost analysis",
                    "IaC analysis (Terraform/CloudFormation)",
                    "Security compliance validation",
                    "Multi-account operations",
                    "Automated PR generation"
                ]
            }
        else:
            return {
                "response": str(response),
                "status": "success",
                "agent": "AWS DevOps Agent",
                "data_source": "Real AWS APIs via MCP servers"
            }

    except Exception as e:
        print(f"❌ AWS DevOps Agent Error: {e}")
        return {
            "response": f"Error processing AWS DevOps request: {str(e)}",
            "status": "error",
            "error": str(e),
            "suggestion": "Check AWS credentials and MCP server connectivity"
        }


if __name__ == "__main__":
    print("🚀 Starting AWS DevOps Agent")
    print(f"🤖 Agent: {agent.name}")
    print(f"🧠 Model: {model_id}")
    print(f"🔧 Debug Mode: {env_config.debug_mode}")
    print(f"🌐 Server: {env_config.host}:{env_config.port}")
    print("🔧 Modern Structure: src/ layout with domain-organized tools")
    print("💰 Tools: Cost optimization, IaC analysis, compliance validation, multi-account operations")
    print("🔌 MCP Integration: Real AWS APIs via official MCP servers")
    print("🌐 Starting Bedrock Agent Core app...")
    
    app.run(port=env_config.port, host=env_config.host)