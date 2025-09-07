#!/usr/bin/env python3
"""
AWS DevOps Agent - Main Production Agent
Integrates all AWS DevOps tools with Strands + MCP Servers
"""

import asyncio
import os
import sys
import readline
import atexit
import uuid
import time
import signal
from pathlib import Path
from typing import Dict, List, Any

# Import Strands and configuration
from strands import Agent
from strands.session.file_session_manager import FileSessionManager
from .config import get_config
from .config.safety_config import get_safety_config, requires_consent, get_consent_message

# Import all our AWS DevOps tools
from .tools import *


class KeyboardInterruptHandler:
    """Handle double Ctrl+C to exit, single Ctrl+C to clear line"""
    
    def __init__(self, timeout=1.0):
        self.last_interrupt_time = 0
        self.timeout = timeout
        self.interrupt_count = 0
    
    def handle_interrupt(self):
        """Handle keyboard interrupt - return True if should exit"""
        current_time = time.time()
        
        if current_time - self.last_interrupt_time < self.timeout:
            # Second Ctrl+C within timeout - exit
            print("\n👋 Goodbye!")
            return True
        else:
            # First Ctrl+C or after timeout - just clear line
            print("\n💡 Press Ctrl+C again within 1 second to exit, or continue typing...")
            self.last_interrupt_time = current_time
            return False


class AWSDevOpsAgentV2:
    """
    AWS DevOps Agent v2 - Production Ready
    Integrates Strands SDK with comprehensive AWS DevOps tools
    """
    
    def __init__(self, session_id=None):
        print("🚀 AWS DevOps Agent v2 - Production Ready")
        print("   Using Strands SDK + AWS DevOps Tools + MCP Integration")
        
        # Load configuration
        self.config = get_config()
        
        # Setup session management
        self.session_id = self._setup_session(session_id)
        self.safety_config = get_safety_config()
        print(f"   📋 Model: {self.config.model.model_id}")
        print(f"   🌍 Region: {self.config.aws_region}")
        print(f"   🔒 Safety: Explicit consent required for all dangerous actions")
        
        # Initialize agent
        self.agent = None
        self._setup_agent()
    
    def _setup_agent(self):
        """Setup the main Strands agent with all AWS DevOps tools and session management"""
        print("🤖 Setting up Strands Agent with AWS DevOps tools...")
        
        # Setup Strands session manager
        session_manager = FileSessionManager(session_id=self.session_id)
        print(f"   📝 Session: {self.session_id}")
        
        # All available tools
        all_tools = [
            # Cost Optimization Tools
            get_real_aws_pricing,
            analyze_price_optimization_opportunities,
            generate_cost_comparison_report,
            calculate_reserved_instance_savings,
            
            # Real AWS Cost Explorer Tools (via MCP Servers)
            get_actual_aws_costs,
            get_cost_trends,
            get_organization_costs,
            get_rightsizing_recommendations,
            get_reserved_instance_recommendations,
            analyze_cost_anomalies,
            analyze_usage_based_optimization,
            
            # Live AWS Resources Tools  
            get_unused_resources,
            calculate_resource_utilization,
            analyze_resource_costs,
            
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
            generate_multi_account_report,
            
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
        
        # Create the agent with session management
        self.agent = Agent(
            model=self.config.model.model_id,
            tools=all_tools,
            name="AWS DevOps Agent v2",
            session_manager=session_manager,
            system_prompt="""Eres un especialista en AWS DevOps con acceso completo a herramientas de producción.

TUS CAPACIDADES PRINCIPALES:
💰 OPTIMIZACIÓN DE COSTOS:
- Análisis de precios en tiempo real via AWS Pricing API
- Acceso REAL a AWS Cost Explorer con datos de facturación actuales
- Análisis de tendencias y breakdowns multi-cuenta via Cost Explorer API
- Recomendaciones de rightsizing y Reserved Instances basadas en datos reales

🎯 ANÁLISIS INTELIGENTE DE TERRAFORM:
Cuando analices proyectos Terraform, usa toda la información disponible del plan real:
- Lee TODOS los recursos específicos del terraform_resources_detail
- Considera las preferencias del usuario (ej: "no T-family instances", "production environment", "use reserved instances")
- Calcula ahorros específicos con precios reales de AWS
- Sugiere alternativas técnicas concretas (ej: "t3.large → m5.large")
- Considera restricciones de producción vs desarrollo
- Analiza configuraciones reales (instance types, storage, networking)

EJEMPLOS DE CONTEXTO DEL USUARIO:
- "No T-family EC2 instances" → Recomienda M5, C5, R5 según uso
- "Production environment" → Multi-AZ, Reserved Instances, no Spot
- "Use gp3 storage" → Migra de gp2 a gp3 con IOPS específicos  
- "Reserved instances preferred" → Calcula savings exactos RI vs On-Demand
- "Use Graviton when possible" → Sugiere instances ARM64 cuando aplicable
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
        """Run interactive conversation mode with command history and smart Ctrl+C handling"""
        # Setup readline for command history and arrow key navigation
        self._setup_readline_history()
        
        # Setup double Ctrl+C handler
        interrupt_handler = KeyboardInterruptHandler()
        
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
        print("\n💡 Use ↑/↓ arrow keys to navigate command history")
        print("💡 Single Ctrl+C clears line, double Ctrl+C exits")
        print()
        
        while True:
            try:
                user_input = input("👤 AWS DevOps> ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Thinking...")
                response = asyncio.run(self.chat(user_input))
                print(f"🤖 {response}\n")
                
            except KeyboardInterrupt:
                # Handle smart Ctrl+C logic
                should_exit = interrupt_handler.handle_interrupt()
                if should_exit:
                    break
                # Continue the loop for single Ctrl+C
                continue
                
            except EOFError:
                print("\n👋 Goodbye!")  
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
    
    def _setup_session(self, session_id=None):
        """Setup session management with interactive prompt if needed"""
        if session_id is not None:
            if session_id == "new":
                # Generate new session ID
                new_id = str(uuid.uuid4())[:8]
                print(f"✅ Created new session: {new_id}")
                return new_id
            else:
                # Use provided session ID
                print(f"✅ Using session: {session_id}")
                return session_id
        
        # Interactive session prompt
        interrupt_handler = KeyboardInterruptHandler()
        print("\n🔐 AWS DevOps Agent v2 - Session Setup")
        print("=" * 50)
        print("💡 Single Ctrl+C clears line, double Ctrl+C creates new session")
        
        while True:
            try:
                user_input = input("Enter session ID (or 'new' for new session): ").strip()
                
                if not user_input:
                    print("⚠️  Please enter a session ID or 'new'")
                    continue
                
                if user_input.lower() == "new":
                    new_id = str(uuid.uuid4())[:8]
                    print(f"✅ Created new session: {new_id}")
                    return new_id
                else:
                    print(f"✅ Using session: {user_input}")
                    return user_input
                    
            except KeyboardInterrupt:
                should_exit = interrupt_handler.handle_interrupt()
                if should_exit:
                    # Create new session and continue
                    new_id = str(uuid.uuid4())[:8]
                    print(f"✅ Using default new session: {new_id}")
                    return new_id
                continue
                
            except EOFError:
                # Default to new session if user cancels with Ctrl+D
                new_id = str(uuid.uuid4())[:8] 
                print(f"\n✅ Using default new session: {new_id}")
                return new_id

    def _setup_readline_history(self):
        """Setup readline for command history and arrow key navigation"""
        try:
            # Set history file path with session ID
            history_file = os.path.expanduser(f"~/.aws_devops_agent_history_{self.session_id}")
            
            # Configure readline
            readline.set_startup_hook(None)
            readline.set_completer(None)
            
            # Enable arrow key navigation
            readline.parse_and_bind("\\e[A: history-search-backward")  # Up arrow
            readline.parse_and_bind("\\e[B: history-search-forward")   # Down arrow
            readline.parse_and_bind("\\e[C: forward-char")             # Right arrow
            readline.parse_and_bind("\\e[D: backward-char")            # Left arrow
            
            # Enable common shortcuts
            readline.parse_and_bind("\\C-a: beginning-of-line")        # Ctrl+A
            readline.parse_and_bind("\\C-e: end-of-line")              # Ctrl+E
            readline.parse_and_bind("\\C-k: kill-line")                # Ctrl+K
            readline.parse_and_bind("\\C-u: unix-line-discard")        # Ctrl+U
            
            # Set maximum history length
            readline.set_history_length(1000)
            
            # Load existing history if it exists
            if os.path.exists(history_file):
                readline.read_history_file(history_file)
            
            # Setup auto-save on exit
            atexit.register(lambda: self._save_history(history_file))
            
        except Exception as e:
            # If readline setup fails, continue without history
            print(f"⚠️  Command history unavailable: {e}")
    
    def _save_history(self, history_file: str):
        """Save command history to file"""
        try:
            readline.write_history_file(history_file)
        except Exception:
            # Silently ignore history save errors
            pass

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
    parser.add_argument("--session-id", type=str, help="Session ID ('new' for new session)")
    
    args = parser.parse_args()
    
    try:
        # Initialize agent with session management
        agent = AWSDevOpsAgentV2(session_id=args.session_id)
        
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