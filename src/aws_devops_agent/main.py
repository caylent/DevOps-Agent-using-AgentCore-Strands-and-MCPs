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
from .config.aws_account_manager import get_aws_account_manager

# Import all our AWS DevOps tools
from .tools import *

# Import security tools specifically
from .tools.aws_security import (
    analyze_security_hub_findings,
    get_security_insights,
    analyze_security_posture,
    analyze_config_compliance,
    get_compliance_details,
    check_resource_compliance,
    analyze_inspector_findings,
    get_vulnerability_assessment,
    check_security_vulnerabilities,
    get_trusted_advisor_checks,
    analyze_trusted_advisor_recommendations,
    get_security_recommendations,
    perform_comprehensive_security_analysis,
    generate_security_report
)


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
    
    def __init__(self, session_id=None, interactive_account_selection=True):
        print("🚀 AWS DevOps Agent v2 - Production Ready")
        print("   Using Strands SDK + AWS DevOps Tools + MCP Integration")
        
        # Load configuration
        self.config = get_config()
        
        # Setup AWS account management
        self.account_manager = get_aws_account_manager(
            region=self.config.aws_region, 
            profile=self.config.aws_profile
        )
        
        # Handle account selection
        if interactive_account_selection:
            self.selected_account = self.account_manager.interactive_account_selection()
        else:
            # Use environment variables or detect current account
            if self.config.aws_account_id:
                self.selected_account = self.account_manager.add_account(
                    self.config.aws_account_id,
                    self.config.aws_account_name,
                    self.config.aws_role_arn
                )
            else:
                self.selected_account = self.account_manager.detect_current_account()
        
        # Setup session management
        self.session_id = self._setup_session(session_id)
        self.safety_config = get_safety_config()
        
        print(f"   📋 Model: {self.config.model.model_id}")
        print(f"   🌍 Region: {self.config.aws_region}")
        if self.selected_account:
            print(f"   🏢 Account: {self.selected_account.account_id} ({self.selected_account.account_name or 'No name'})")
        else:
            print(f"   🏢 Account: Using environment variables")
        print(f"   🔒 Safety: Explicit consent required for all dangerous actions")
        
        # Initialize agent
        self.agent = None
        self._setup_agent()
    
    def _get_project_sessions_dir(self):
        """Get the project-local sessions directory"""
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(project_root, ".sessions")
    
    def _show_accounts(self):
        """Show all managed AWS accounts"""
        print("\n🏢 Managed AWS Accounts")
        print("=" * 40)
        
        accounts = self.account_manager.list_accounts()
        if not accounts:
            print("No accounts managed yet")
            return
        
        for i, account in enumerate(accounts, 1):
            status_icon = "✅" if account.status == "active" else "❌"
            current_marker = " (CURRENT)" if account.is_current else ""
            print(f"{i}. {status_icon} {account.account_id} ({account.account_name or 'No name'}){current_marker}")
            print(f"   Region: {account.region}")
            print(f"   Status: {account.status}")
            if account.permissions:
                print(f"   Permissions: {', '.join(account.permissions)}")
            print()
    
    def _switch_account(self):
        """Switch to a different AWS account"""
        print("\n🔄 Switch AWS Account")
        print("=" * 30)
        
        accounts = self.account_manager.list_accounts()
        if not accounts:
            print("No accounts managed yet. Use the startup account selection to add accounts.")
            return
        
        print("Available accounts:")
        for i, account in enumerate(accounts, 1):
            status_icon = "✅" if account.status == "active" else "❌"
            current_marker = " (CURRENT)" if account.is_current else ""
            print(f"{i}. {status_icon} {account.account_id} ({account.account_name or 'No name'}){current_marker}")
        
        try:
            choice = input("\nEnter account number to switch to (or 'cancel'): ").strip()
            if choice.lower() == 'cancel':
                return
            
            account_index = int(choice) - 1
            if 0 <= account_index < len(accounts):
                selected_account = accounts[account_index]
                
                # Validate access
                success, message = self.account_manager.validate_account_access(selected_account.account_id)
                if success:
                    self.selected_account = selected_account
                    print(f"✅ Switched to account: {selected_account.account_id} ({selected_account.account_name or 'No name'})")
                else:
                    print(f"❌ Could not switch to account: {message}")
            else:
                print("❌ Invalid account number")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Cancelled")
    
    def _show_account_status(self):
        """Show current account status and information"""
        print("\n📊 Current Account Status")
        print("=" * 30)
        
        if self.selected_account:
            print(f"Account ID: {self.selected_account.account_id}")
            print(f"Account Name: {self.selected_account.account_name or 'No name'}")
            print(f"Region: {self.selected_account.region}")
            print(f"Status: {self.selected_account.status}")
            print(f"Is Current: {self.selected_account.is_current}")
            if self.selected_account.permissions:
                print(f"Permissions: {', '.join(self.selected_account.permissions)}")
            if self.selected_account.last_accessed:
                print(f"Last Accessed: {self.selected_account.last_accessed}")
        else:
            print("No account selected - using environment variables")
        
        print(f"\nAccount Manager Summary:")
        summary = self.account_manager.get_account_summary()
        print(f"Total Accounts: {summary['total_accounts']}")
        print(f"Current Account: {summary['current_account'] or 'None'}")
    
    def _show_help(self):
        """Show help information and available commands"""
        print("\n🤖 AWS DevOps Agent v2 - Help")
        print("=" * 40)
        print("Available Commands:")
        print("  accounts        - Show all managed AWS accounts")
        print("  switch-account  - Switch to a different AWS account")
        print("  account-status  - Show current account status")
        print("  help, ?         - Show this help message")
        print("  exit, quit, q   - Exit the application")
        print()
        print("Multi-line Input:")
        print("  Type \"'''\" to enter multi-line mode for complex queries")
        print()
        print("AWS DevOps Capabilities:")
        print("  💰 Cost optimization and analysis")
        print("  🏗️  Infrastructure as Code (Terraform, CloudFormation, CDK)")
        print("  🔒 Security and compliance analysis")
        print("  🌐 Multi-account operations")
        print("  📊 Real-time AWS resource monitoring")
        print("  📄 Automated report generation")
        print()
        print("Example Queries:")
        print("  'Analyze costs for the last 30 days'")
        print("  'Review security findings in this account'")
        print("  'Optimize EC2 instances for cost savings'")
        print("  'Generate a compliance report for SOC2'")
        print()
    
    def _setup_agent(self):
        """Setup the main Strands agent with all AWS DevOps tools and session management"""
        print("🤖 Setting up Strands Agent with AWS DevOps tools...")
        
        # Setup Strands session manager with custom directory
        sessions_dir = self._get_project_sessions_dir()
        os.makedirs(sessions_dir, exist_ok=True)
        
        # Check if FileSessionManager supports custom base directory
        try:
            # Try with base_dir parameter first
            session_manager = FileSessionManager(session_id=self.session_id, base_dir=sessions_dir)
        except TypeError:
            # Fall back to default behavior if base_dir is not supported
            session_manager = FileSessionManager(session_id=self.session_id)
            
        print(f"   📝 Session: {self.session_id}")
        print(f"   📂 Session dir: {os.path.join(sessions_dir, self.session_id)}")
        
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
            
            # Real AWS Security Analysis Tools
            analyze_security_hub_findings,
            get_security_insights,
            analyze_security_posture,
            analyze_config_compliance,
            get_compliance_details,
            check_resource_compliance,
            analyze_inspector_findings,
            get_vulnerability_assessment,
            check_security_vulnerabilities,
            get_trusted_advisor_checks,
            analyze_trusted_advisor_recommendations,
            get_security_recommendations,
            perform_comprehensive_security_analysis,
            generate_security_report,
            
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

⚠️ CRÍTICO - MOSTRAR TABLA DE RECURSOS:
- Cuando uses analyze_terraform_project, muestra la tabla ASCII completa tal como viene en el resultado de "resource_summary_display" 
- Debe ser lo PRIMERO que muestres al usuario


🏗️ ANÁLISIS DE INFRAESTRUCTURA COMO CÓDIGO (IaC):
- Validación de configuraciones Terraform y CloudFormation
- Análisis completo de proyectos AWS CDK (síntesis y optimización)
- Análisis completo de proyectos Terraform (validación, planificación y optimización)
- Detección de drift entre código y estado real
- Best practices y recomendaciones de seguridad
- Análisis de cumplimiento de estándares

🔒 SEGURIDAD Y COMPLIANCE (REAL AWS APIs):
- Análisis REAL de Security Hub con findings de seguridad en tiempo real
- Compliance REAL con AWS Config y reglas de configuración
- Vulnerabilidades REALES con Amazon Inspector
- Recomendaciones REALES de AWS Trusted Advisor
- Análisis integral de postura de seguridad combinando todos los servicios
- Validación contra estándares SOC2, HIPAA, PCI-DSS, ISO27001
- Reportes de compliance ejecutivos con datos reales de AWS

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
    
    def _get_multiline_input(self) -> str:
        """Get multi-line input from user"""
        print("📝 Multi-line input mode activated. Type your text, then type \"'''\" on a new line to finish:")
        lines = []
        while True:
            try:
                line = input("... ")
                if line.strip() == "'''":
                    break
                lines.append(line)
            except KeyboardInterrupt:
                print("\n❌ Multi-line input cancelled")
                return ""
            except EOFError:
                break
        
        return "\n".join(lines)
    
    def _handle_input_with_fallback(self) -> str:
        """Enhanced input handling with multi-line support fallback"""
        try:
            user_input = input("👤 AWS DevOps> ").strip()
            
            # If input contains literal \n characters (from paste), convert them
            if "\\n" in user_input:
                print("📝 Converting escaped newlines to multi-line format...")
                user_input = user_input.replace("\\n", "\n")
            
            return user_input
            
        except KeyboardInterrupt:
            raise  # Let the main handler deal with this
        except EOFError:
            raise  # Let the main handler deal with this
    
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
        print("💡 Multi-line input options:")
        print("  - Type \"'''\" to enter multi-line mode")
        print("  - Or paste text with literal \\n characters (they'll be converted)")
        print()
        
        while True:
            try:
                user_input = self._handle_input_with_fallback()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                # Handle special commands
                if user_input.lower() == 'accounts':
                    self._show_accounts()
                    continue
                elif user_input.lower() == 'switch-account':
                    self._switch_account()
                    continue
                elif user_input.lower() == 'account-status':
                    self._show_account_status()
                    continue
                elif user_input.lower() in ['help', '?']:
                    self._show_help()
                    continue
                
                # Check for multi-line input trigger
                if user_input == "'''":
                    user_input = self._get_multiline_input()
                    if not user_input:  # User cancelled
                        continue
                
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
    
    def _validate_or_create_session(self, session_id: str) -> str:
        """Validate if session exists, create if it doesn't"""
        try:
            # Use project-local session directory
            sessions_base_dir = self._get_project_sessions_dir()
            session_dir = os.path.join(sessions_base_dir, session_id)
            marker_file = os.path.join(session_dir, ".session_initialized")
            
            session_exists = False
            if os.path.exists(session_dir):
                session_exists = os.path.exists(marker_file) or len([f for f in os.listdir(session_dir) if f.endswith('.json')]) > 0
            
            if session_exists:
                print(f"✅ Using existing session: {session_id}")
                print(f"   📂 Session data found at: {session_dir}")
                # Count conversation files to show session activity
                try:
                    files = [f for f in os.listdir(session_dir) if f.endswith('.json')]
                    if files:
                        print(f"   💬 Found {len(files)} conversation files")
                except:
                    pass
            else:
                print(f"🆕 Creating NEW session: {session_id}")
                print(f"   📂 Session will be saved at: {session_dir}")
                print(f"   💡 This is a fresh start - no previous conversation history")
                
                # Create the directory structure to ensure it exists
                os.makedirs(session_dir, exist_ok=True)
                print(f"   ✅ Session directory created")
                
            # Try to create FileSessionManager with the session_id
            # This will work whether the session exists or not
            session_manager = FileSessionManager(session_id=session_id)
            
            # Test session manager by creating a small marker file
            marker_file = os.path.join(session_dir, ".session_initialized")
            if not os.path.exists(marker_file):
                with open(marker_file, 'w') as f:
                    import json
                    json.dump({
                        "session_id": session_id,
                        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "agent_version": "v2"
                    }, f, indent=2)
                print(f"   ✅ Session initialized and marked")
            
            return session_id
            
        except Exception as e:
            # If there's any issue, create a new session
            new_id = str(uuid.uuid4())[:8]
            print(f"⚠️  Issue with session '{session_id}': {e}")
            print(f"🆕 Created fallback session: {new_id}")
            sessions_base_dir = self._get_project_sessions_dir()
            fallback_dir = os.path.join(sessions_base_dir, new_id)
            print(f"   📂 Session will be saved at: {fallback_dir}")
            try:
                os.makedirs(fallback_dir, exist_ok=True)
            except:
                pass
            return new_id

    def _setup_session(self, session_id=None):
        """Setup session management with interactive prompt if needed"""
        if session_id is not None:
            if session_id == "new":
                # Generate new session ID
                new_id = str(uuid.uuid4())[:8]
                print(f"✅ Created new session: {new_id}")
                return new_id
            else:
                # Validate or create the session
                return self._validate_or_create_session(session_id)
        
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
                    return self._validate_or_create_session(user_input)
                    
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
            # Set history file path with session ID in project sessions directory
            sessions_base_dir = self._get_project_sessions_dir()
            history_file = os.path.join(sessions_base_dir, f"{self.session_id}.history")
            
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
            "tools_count": 65,  # Total tools available (20 + 11 MCP AWS tools + 4 CDK tools + 5 Terraform tools + 8 reporting tools + 17 security tools)
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
    parser.add_argument("--no-account-selection", action="store_true",
                       help="Skip interactive account selection (use environment variables only)")
    
    args = parser.parse_args()
    
    try:
        # Initialize agent with session management
        interactive_account_selection = not args.no_account_selection
        agent = AWSDevOpsAgentV2(
            session_id=args.session_id, 
            interactive_account_selection=interactive_account_selection
        )
        
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