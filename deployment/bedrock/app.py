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

try:
    config = get_config()
    model_id = config.model.model_id
except ImportError:
    # Fallback for testing - using inference profile
    model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

# Create the Strands agent
agent = Agent(
    model=model_id,
    tools=[
        # Cost Optimization Tools
        get_real_aws_pricing,
        analyze_cost_optimization_opportunities,
        generate_cost_comparison_report,
        calculate_reserved_instance_savings,
        
        # Cost Explorer Tools (Real AWS Data)
        get_actual_aws_costs,
        analyze_cost_trends_real,
        get_multi_account_cost_breakdown,
        get_rightsizing_recommendations,
        get_reserved_instance_recommendations,
        get_cost_forecast_mcp,
        compare_cost_periods_mcp,
        
        # Live Resources Tools
        scan_live_aws_resources,
        analyze_unused_resources,
        get_resource_utilization_metrics,
        discover_cross_account_resources,
        
        # Infrastructure as Code Tools
        analyze_terraform_configuration,
        validate_cloudformation_template,
        scan_infrastructure_drift,
        generate_iac_best_practices_report,
        
        # Compliance and Security Tools
        validate_security_policies,
        check_compliance_standards,
        generate_compliance_report,
        scan_security_vulnerabilities,
        
        # Multi-Account Management Tools
        list_cross_account_resources,
        execute_cross_account_operation,
        generate_multi_account_report,
        monitor_cross_account_compliance,
        
        # GitHub Integration Tools
        create_optimization_pull_request,
        update_iac_via_github,
        list_infrastructure_repositories,
        monitor_infrastructure_prs,
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

🏗️ ANÁLISIS DE INFRAESTRUCTURA COMO CÓDIGO (IaC):
- Validación de configuraciones Terraform y CloudFormation
- Detección de drift entre código y estado real
- Best practices y recomendaciones de seguridad
- Análisis de cumplimiento de estándares

🔒 SEGURIDAD Y COMPLIANCE:
- Validación contra estándares SOC2, HIPAA, PCI-DSS, ISO27001
- Escaneo de vulnerabilidades de seguridad
- Análisis de políticas y configuraciones
- Reportes de compliance ejecutivos

🌐 GESTIÓN MULTI-CUENTA:
- Operaciones cross-account en organizaciones AWS
- Inventario de recursos en múltiples cuentas y regiones
- Análisis de costos organizacional
- Monitoreo de compliance centralizado

📱 INTEGRACIÓN GITHUB:
- Generación automática de Pull Requests con optimizaciones
- Gestión de repositorios de infraestructura
- Automatización de CI/CD para IaC
- Monitoring de PRs de infraestructura

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

# Create the Bedrock Agent Core app
app = BedrockAgentCoreApp()


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
    print("🔧 Modern Structure: src/ layout with domain-organized tools")
    print("💰 Tools: Cost optimization, IaC analysis, compliance validation, multi-account operations")
    print("🔌 MCP Integration: Real AWS APIs via official MCP servers")
    print("🌐 Starting Bedrock Agent Core app...")
    app.run()