#!/usr/bin/env python3
"""
AWS DevOps Agent - Main Production Agent
Integrates all AWS DevOps tools with Strands + MCP Servers
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

# Import Strands and configuration
from strands import Agent
from .config import get_config
from .config.safety_config import get_safety_config, requires_consent, get_consent_message

# Import all our AWS DevOps tools
from .tools import *


class AWSDevOpsAgentV2:
    """
    AWS DevOps Agent v2 - Production Ready
    Integrates Strands SDK with comprehensive AWS DevOps tools
    """
    
    def __init__(self):
        print("🚀 AWS DevOps Agent v2 - Production Ready")
        print("   Using Strands SDK + AWS DevOps Tools + MCP Integration")
        
        # Load configuration
        self.config = get_config()
        self.safety_config = get_safety_config()
        print(f"   📋 Model: {self.config.model.model_id}")
        print(f"   🌍 Region: {self.config.aws_region}")
        print(f"   🔒 Safety: Explicit consent required for all dangerous actions")
        
        # Initialize agent
        self.agent = None
        self._setup_agent()
    
    def _setup_agent(self):
        """Setup the main Strands agent with all AWS DevOps tools"""
        print("🤖 Setting up Strands Agent with AWS DevOps tools...")
        
        # All available tools
        all_tools = [
            # Cost Optimization Tools
            get_real_aws_pricing,
            analyze_cost_optimization_opportunities,
            generate_cost_comparison_report,
            calculate_reserved_instance_savings,
            
            # Real AWS Cost Explorer Tools (via MCP Servers)
            get_actual_aws_costs,
            analyze_cost_trends_real,
            get_multi_account_cost_breakdown,
            get_rightsizing_recommendations,
            get_reserved_instance_recommendations,
            get_cost_forecast_mcp,
            compare_cost_periods_mcp,
            
            # Live AWS Resources Tools
            scan_live_aws_resources,
            analyze_unused_resources,
            get_resource_utilization_metrics,
            discover_cross_account_resources,
            
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
            
            # Document Generation Tools
            generate_document,
            generate_cost_analysis_document,
            generate_security_compliance_document,
            generate_infrastructure_document,
            generate_cdk_analysis_document,
            generate_terraform_analysis_document,
            list_generated_documents,
            get_document_info,
        ]
        
        # Create the agent
        self.agent = Agent(
            model=self.config.model.model_id,
            tools=all_tools,
            name="AWS DevOps Agent v2",
            system_prompt="""Eres un especialista en AWS DevOps con acceso completo a herramientas de producción.

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
- Análisis completo de proyectos AWS CDK (síntesis y optimización)
- Análisis completo de proyectos Terraform (validación, planificación y optimización)
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
- Análisis de repositorios de infraestructura
- Preparación de cambios para Pull Requests (SOLO CON CONSENTIMIENTO EXPLÍCITO)
- Monitoring de PRs de infraestructura
- Gestión de repositorios (solo lectura por defecto)

📄 GENERACIÓN DE DOCUMENTOS:
- Creación automática de reportes en carpeta 'reports/'
- Documentos en formato Markdown, JSON, CSV, Excel
- Reportes de costos, seguridad, infraestructura, CDK
- Organización automática por tipo de reporte

FLUJO DE TRABAJO CONVERSACIONAL:
1. Analiza la consulta del usuario en español/inglés
2. Determina qué herramientas usar y en qué secuencia
3. Ejecuta análisis usando datos reales de AWS via MCP
4. Combina resultados en una respuesta integral
5. NUNCA crea PRs automáticamente - SIEMPRE pide consentimiento explícito
6. Proporciona next steps accionables y seguros

EJEMPLOS DE USO:
- "Analiza mi infraestructura Terraform y optimiza costos"
- "Valida compliance SOC2 y crea PR con mejoras"
- "Compara costos entre regiones para mi aplicación"
- "Encuentra recursos sin usar en todas mis cuentas"

IMPORTANTE - REGLAS DE SEGURIDAD CRÍTICAS:
- NUNCA crees PRs, commits, o pushes sin consentimiento explícito del usuario
- SIEMPRE pregunta antes de realizar cualquier acción que modifique código o infraestructura
- Solo proporciona análisis, recomendaciones y preparación de cambios
- Los usuarios deben aprobar explícitamente cualquier acción antes de ejecutarla
- Siempre especifica que los datos provienen de APIs reales de AWS
- Incluye números específicos y ahorros en dólares
- Proporciona executive summaries para stakeholders
- Mantén foco en ROI y value delivery

Responde de manera concisa pero completa, integrando múltiples fuentes de datos en un análisis coherente.""",
            description="Comprehensive AWS DevOps automation with cost optimization, security compliance, and infrastructure management"
        )
        
        print(f"✅ Agent ready with {len(all_tools)} AWS DevOps tools")
    
    def _check_message_safety(self, message: str) -> Dict[str, Any]:
        """Check if a message contains dangerous actions that require consent"""
        message_lower = message.lower()
        
        # Check for dangerous patterns
        dangerous_patterns = [
            "create pull request",
            "create pr",
            "push to",
            "commit changes",
            "modify infrastructure",
            "deploy",
            "update",
            "change",
            "alter",
            "pull request",
            "pr with",
            "push",
            "commit",
            "modify",
            "deploy"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in message_lower:
                return {
                    "safe": False,
                    "requires_consent": True,
                    "dangerous_pattern": pattern,
                    "message": f"⚠️  DANGER: Message contains '{pattern}' which requires explicit user consent!",
                    "recommendation": "Ask the user to explicitly confirm this action before proceeding."
                }
        
        return {
            "safe": True,
            "requires_consent": False,
            "message": "Message appears safe to process"
        }
    
    async def chat(self, message: str) -> str:
        """Process a chat message through the agent"""
        if not self.agent:
            return "❌ Agent not initialized properly"
        
        try:
            # Safety check for dangerous actions
            safety_check = self._check_message_safety(message)
            if not safety_check["safe"]:
                return f"🔒 SAFETY CHECK FAILED\n\n{safety_check['message']}\n\n{safety_check['recommendation']}\n\nPlease explicitly confirm this action if you want to proceed."
            
            print(f"🗣️  Processing: {message}")
            response = self.agent(message)
            return str(response)
        except Exception as e:
            return f"❌ Error processing message: {str(e)}"
    
    def interactive_mode(self):
        """Run interactive conversation mode"""
        print("\n💡 AWS DevOps Agent v2 - Interactive Mode")
        print("=" * 60)
        print("Available capabilities:")
        print("💰 Cost optimization and pricing analysis")
        print("🏗️  Infrastructure as Code (Terraform/CloudFormation/CDK) analysis")
        print("🔒 Security and compliance validation")
        print("🌐 Multi-account AWS operations")
        print("📱 GitHub integration and PR automation")
        print("📄 Document generation and report creation")
        print()
        print("Examples:")
        print("• 'Analyze AWS costs for my infrastructure'")
        print("• 'Check security compliance for my EC2 instances'")
        print("• 'Compare pricing between us-east-1 and eu-west-1'")
        print("• 'Analyze my CDK project for optimization opportunities'")
        print("• 'Analyze my Terraform project for cost optimization'")
        print("• 'Generate a cost analysis report'")
        print("• 'Create a security compliance document'")
        print("• Type 'exit' to quit")
        print()
        
        while True:
            try:
                user_input = input("👤 AWS DevOps> ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Thinking...")
                response = asyncio.run(self.chat(user_input))
                print(f"🤖 {response}\n")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")
        
        print("\n👋 AWS DevOps Agent v2 session ended")
    
    def demo_mode(self):
        """Run demo scenarios"""
        print("\n🎯 AWS DevOps Agent v2 - Demo Mode")
        print("=" * 50)
        
        scenarios = [
            {
                "name": "Cost Analysis",
                "query": "Analyze the cost of running a t3.medium EC2 instance 24/7 in us-east-1 and suggest optimizations"
            },
            {
                "name": "Security Compliance",
                "query": "Validate security policies for an EC2 instance with public IP and open security groups"
            },
            {
                "name": "Multi-Service Comparison", 
                "query": "Compare costs between RDS and DynamoDB for a web application database"
            },
            {
                "name": "GitHub Integration",
                "query": "Prepare cost optimization recommendations for review"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n📋 Demo {i}: {scenario['name']}")
            print(f"Query: {scenario['query']}")
            print("-" * 50)
            
            try:
                response = asyncio.run(self.chat(scenario['query']))
                print(f"🤖 Response:\n{response}")
            except Exception as e:
                print(f"❌ Error in demo: {e}")
            
            if i < len(scenarios):
                input("\n⏸️  Press Enter to continue to next demo...")
            print("=" * 50)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_ready": self.agent is not None,
            "model": self.config.model.model_id,
            "aws_region": self.config.aws_region,
            "tools_count": 48,  # Total tools available (20 + 11 MCP AWS tools + 4 CDK tools + 5 Terraform tools + 8 reporting tools)
            "capabilities": [
                "Cost optimization",
                "IaC analysis (Terraform, CloudFormation, CDK)", 
                "Security compliance",
                "Multi-account operations",
                "GitHub integration"
            ]
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS DevOps Agent v2")
    parser.add_argument("--mode", choices=["interactive", "demo"], default="interactive",
                       help="Run mode: interactive chat or demo scenarios")
    parser.add_argument("--query", type=str, help="Single query to process")
    
    args = parser.parse_args()
    
    try:
        # Initialize agent
        agent = AWSDevOpsAgentV2()
        
        if args.query:
            # Single query mode
            print(f"🗣️  Query: {args.query}")
            response = asyncio.run(agent.chat(args.query))
            print(f"🤖 Response:\n{response}")
        elif args.mode == "demo":
            # Demo mode
            agent.demo_mode()
        else:
            # Interactive mode (default)
            agent.interactive_mode()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())