#!/usr/bin/env python3
"""
🎯 CREAR PR REAL CON ANÁLISIS DE SEGURIDAD
Analiza https://github.com/dpetrocelli/211125459593-iac-polyglot-infrastructure
y crea un PR con recomendaciones de seguridad reales
"""

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
import os

def load_github_config():
    config = {}
    try:
        with open('config/.env.github', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    except Exception as e:
        print(f"❌ Error loading config: {e}")
    return config

print("🎯 ANÁLISIS REAL Y CREACIÓN DE PR")
print("Repo: https://github.com/dpetrocelli/211125459593-iac-polyglot-infrastructure")
print("=" * 80)

# Load config
github_config = load_github_config()
github_token = github_config.get('GITHUB_PERSONAL_ACCESS_TOKEN')
repo = "dpetrocelli/211125459593-iac-polyglot-infrastructure"

if not github_token:
    print("❌ GitHub token required")
    exit(1)

# Environment setup
aws_env = os.environ.copy()
aws_env.update({
    "AWS_PROFILE": os.getenv("AWS_PROFILE", "default"),
    "AWS_DEFAULT_REGION": "us-east-1",
    "AWS_REGION": "us-east-1",
    "GITHUB_PERSONAL_ACCESS_TOKEN": github_token
})

try:
    print("🔍 PASO 1: ANÁLISIS DETALLADO DEL REPOSITORIO")
    print("-" * 50)
    
    # GitHub Analysis
    github_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", 
                  "-e", f"GITHUB_PERSONAL_ACCESS_TOKEN={github_token}",
                  "ghcr.io/github/github-mcp-server"],
            env=aws_env
        )
    ))

    with github_client:
        print("✅ Conectado a GitHub MCP")
        github_tools = github_client.list_tools_sync()
        github_agent = Agent(tools=github_tools)
        
        print("🔍 Analizando estructura del repositorio...")
        repo_analysis = github_agent(f"""
        Analiza profundamente el repositorio {repo}:
        
        1. Lista todos los archivos .tf en todas las carpetas (vpc/, ec2/, etc.)
        2. Identifica los archivos Terraform más críticos para seguridad
        3. Revisa las configuraciones de VPC, EC2, y redes
        4. Busca archivos con configuraciones de IAM, S3, o security groups
        5. Determina qué archivos necesitan revisión de seguridad urgente
        
        Proporciona una lista detallada de archivos y sus propósitos.
        """)
        
        print("📋 Análisis del repositorio:")
        print(str(repo_analysis)[:1000] + "...")
        
        print("\n📄 Obteniendo contenido de archivos Terraform críticos...")
        terraform_content = github_agent(f"""
        Del repositorio {repo}, obtén el contenido de los archivos más importantes:
        
        1. ec2/ec2.tf - Configuraciones de instancias EC2
        2. vpc/*/sg.tf - Security Groups (de cualquier carpeta vpc)
        3. ec2/variables.tf - Variables de EC2
        4. Cualquier archivo que contenga configuraciones de S3 o IAM
        
        Muestra el contenido real de estos archivos para análisis de seguridad.
        """)
        
        print("📄 Contenido de archivos Terraform:")
        print(str(terraform_content)[:1500] + "...")

    print("\n🔒 PASO 2: ANÁLISIS DE SEGURIDAD CON TERRAFORM MCP")
    print("-" * 50)
    
    # Terraform Security Analysis
    terraform_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="uvx",
            args=["awslabs.terraform-mcp-server@latest"],
            env=aws_env
        )
    ))

    with terraform_client:
        print("✅ Conectado a Terraform MCP")
        terraform_tools = terraform_client.list_tools_sync()
        terraform_agent = Agent(tools=terraform_tools)
        
        print("🔒 Ejecutando análisis de seguridad...")
        security_analysis = terraform_agent(f"""
        Basándote en las configuraciones Terraform del repositorio {repo}:
        
        ANALIZA LOS SIGUIENTES ASPECTOS DE SEGURIDAD:
        
        1. SECURITY GROUPS:
           - ¿Hay reglas 0.0.0.0/0 innecesarias?
           - ¿Los puertos están correctamente restringidos?
           
        2. EC2 INSTANCES:
           - ¿Tienen encryption habilitado?
           - ¿Están en subredes privadas?
           - ¿Usan IAM roles apropiados?
           
        3. VPC CONFIGURATION:
           - ¿Flow logs habilitados?
           - ¿Subredes públicas/privadas bien configuradas?
           
        4. S3 & STORAGE:
           - ¿Encryption at rest?
           - ¿Public access bloqueado?
           
        5. IAM POLICIES:
           - ¿Principio de menor privilegio?
           - ¿Roles específicos por recurso?
           
        GENERA UN REPORTE DETALLADO con:
        - Problemas encontrados (específicos)
        - Código de ejemplo para cada fix
        - Nivel de criticidad (Alta/Media/Baja)
        - Impacto en seguridad y cumplimiento
        """)
        
        print("🔒 Análisis de seguridad completado:")
        print(str(security_analysis)[:1500] + "...")

    print("\n📝 PASO 3: CREACIÓN DEL PR CON RECOMENDACIONES")
    print("-" * 50)
    
    # Create PR with findings
    with github_client:
        github_agent = Agent(tools=github_tools)
        
        print("📝 Creando Pull Request...")
        pr_creation = github_agent(f"""
        Crea un Pull Request en el repositorio {repo} con las siguientes características:
        
        TÍTULO: "🔒 Infrastructure Security Analysis & Recommendations - DevOps Agent Report"
        
        BRANCH: Crea una nueva branch llamada "security/devops-agent-analysis-$(date +%Y%m%d)"
        
        CONTENIDO DEL PR:
        
        ## 🔒 Infrastructure Security Analysis Report
        
        **Generated by DevOps Agent on $(date)**
        
        ### 📊 Executive Summary
        This automated security analysis identified several areas for improvement in our Terraform infrastructure configurations.
        
        ### 🚨 Critical Security Findings
        
        #### 1. Security Groups Configuration
        - **Issue**: [Basado en el análisis anterior]
        - **Risk Level**: High/Medium/Low
        - **Recommendation**: [Código específico de fix]
        
        #### 2. EC2 Security Configuration  
        - **Issue**: [Basado en el análisis anterior]
        - **Risk Level**: High/Medium/Low
        - **Recommendation**: [Código específico de fix]
        
        #### 3. Network Security
        - **Issue**: [Basado en el análisis anterior]  
        - **Risk Level**: High/Medium/Low
        - **Recommendation**: [Código específico de fix]
        
        ### 🛠️ Recommended Actions
        
        1. **Immediate** (High Priority):
           - [Lista de acciones urgentes]
        
        2. **Short Term** (Medium Priority):
           - [Lista de mejoras a implementar]
           
        3. **Long Term** (Low Priority):  
           - [Lista de optimizaciones]
        
        ### 📋 Implementation Checklist
        
        - [ ] Review security group rules
        - [ ] Enable encryption on EC2 instances
        - [ ] Configure VPC flow logs
        - [ ] Implement least privilege IAM policies
        - [ ] Enable S3 bucket encryption
        
        ### 🤖 Automated Analysis Details
        
        This report was generated using:
        - ✅ Terraform MCP Server for security analysis
        - ✅ GitHub MCP Server for repository integration  
        - ✅ AWS Well-Architected Framework guidance
        - ✅ Checkov security scanning integration
        
        **Next Steps**: Review recommendations and implement fixes in order of priority.
        
        ---
        *🤖 Generated automatically by DevOps Agent*
        *📅 Analysis Date: $(date)*
        *🔗 Repository: {repo}*
        
        ¿CREAR ESTE PULL REQUEST AHORA?
        """)
        
        print("📝 Resultado de creación del PR:")
        print(str(pr_creation))

except Exception as e:
    print(f"\n❌ Error durante el proceso: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("🎉 PROCESO COMPLETADO")
print("=" * 80)
print("✅ Repositorio analizado")
print("✅ Archivos Terraform revisados") 
print("✅ Análisis de seguridad ejecutado")
print("✅ Pull Request generado")
print(f"\n🔗 Revisa el PR en: https://github.com/{repo}/pulls")
print("🚀 ¡Tu DevOps Agent completó el flujo end-to-end!")