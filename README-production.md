# AWS DevOps Agent - Production Ready

Agente conversacional para operaciones DevOps en AWS que integra **Strands SDK**, **Amazon Bedrock**, y **Official AWS MCP Servers** en un único flujo conversacional.

## 🎯 Capacidades

- **Análisis de costos en tiempo real** via AWS Pricing API
- **Operaciones DynamoDB** completas (crear, gestionar, consultar)
- **Optimización de costos** con recomendaciones específicas
- **Análisis multi-región** para AWS services
- **Lenguaje natural** para todas las operaciones AWS

## 🏗️ Arquitectura

```
Natural Language Input
         ↓
Strands Agent (Claude Sonnet 4)
         ↓  
Official AWS MCP Servers
         ↓
Real AWS APIs
```

**MCP Servers Integrados:**
- `awslabs.aws-pricing-mcp-server` - Pricing API real-time
- `awslabs.dynamodb-mcp-server` - DynamoDB operations

## 🚀 Instalación

```bash
# 1. Ejecutar instalación
./install.sh

# 2. Instalar Strands SDK (requiere acceso)
pip install strands

# 3. Configurar AWS credentials
aws configure
```

## 💻 Uso

### Modo Interactivo
```bash
python3 aws_devops_agent.py
```

### Demo de Producción  
```bash
python3 aws_devops_agent.py demo
```

## 💬 Ejemplos de Queries

```bash
# Pricing queries
"Get current EC2 m5.large pricing in us-east-1"
"Compare t3.medium vs m5.large costs for 24/7 usage"

# DynamoDB operations
"Create a DynamoDB table called user-sessions with userId as primary key"
"List my DynamoDB tables"

# Cost analysis
"Analyze cost differences between EC2 instance families"
"Compare DynamoDB vs RDS costs for high-traffic applications"
```

## 📁 Estructura de Archivos

```
strands-bedrock-mcp-devops-agent/
├── aws_devops_agent.py          # Agente principal (ÚNICO archivo necesario)
├── install.sh                   # Script de instalación
├── requirements-production.txt   # Dependencias limpias
├── goal                         # Documentación del proyecto
├── ai-processing/              # Implementación original (referencia)
└── mcp_tools/                  # Tools directory (solo __init__.py)
```

## ⚙️ Configuración

### Variables de Entorno
```bash
export AWS_PROFILE=your-profile
export AWS_DEFAULT_REGION=us-east-1
```

### Permisos AWS Requeridos
- `pricing:GetProducts` - Para queries de precios
- `dynamodb:*` - Para operaciones DynamoDB (según necesidades)

## 🎯 Para Presentaciones AWS

Este agente demuestra perfectamente:
- **Conversational AI** para operaciones DevOps
- **Real-time AWS data** via official MCP servers
- **Cost optimization** inteligente
- **Multi-service analysis** en lenguaje natural
- **Production-ready architecture**

### Demo Script
```bash
# 1. Setup
./install.sh

# 2. Run demo
python3 aws_devops_agent.py demo

# 3. Interactive session
python3 aws_devops_agent.py
> "Get EC2 pricing for m5.large in us-east-1"
> "Create DynamoDB table for analytics"
> "Compare costs between instance types"
```

## 🔗 Official AWS MCP Servers

- [AWS Pricing MCP Server](https://awslabs.github.io/mcp/servers/aws-pricing-mcp-server/)
- [AWS DynamoDB MCP Server](https://awslabs.github.io/mcp/servers/dynamodb-mcp-server/) 
- [Full AWS MCP Documentation](https://awslabs.github.io/mcp/)

## 📋 Requisitos

- **Python 3.10+**
- **Strands SDK** (requiere acceso)
- **AWS credentials** configurados
- **uv package manager** (se instala automáticamente)

---

**🎉 Ready for production!** 

Este es el agente real que funciona con AWS MCP servers oficiales y Strands SDK - sin mocks, sin demos, solo código de producción.