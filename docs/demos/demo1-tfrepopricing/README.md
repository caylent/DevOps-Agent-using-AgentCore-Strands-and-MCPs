# Demo 1: Terraform Repository Pricing Analysis

**Objective**: Analyze Terraform infrastructure costs using our **real AWS DevOps Agent** before deployment.

## 📁 Demo Structure

```
demo1-tfrepopricing/
├── README.md                   # This file - overview
├── 01-setup.md                # Prerequisites and setup
├── 02-terraform-plan.md       # Generate terraform plan
├── 03-agent-interaction.md    # Interactive cost analysis with our agent
└── expected-outputs/          # Sample outputs for reference
    ├── cost-analysis-sample.json
    └── s3-pricing-sample.json
```

## 🎯 What You'll Accomplish

1. **Setup** the simple Terraform project
2. **Generate** terraform plan.json 
3. **Use** our **real AWS DevOps Agent** (`main.py`) interactively
4. **Get** real-time cost estimates via natural language
5. **Receive** optimization recommendations from the agent

## 🤖 Key Feature: Real Agent Interaction

This demo shows how to use the **actual production agent** at:
- `/root/linux-code/strands-bedrock-mcp-devops-agent/main.py`
- Interactive natural language interface
- Real AWS Pricing MCP integration

## 📋 Target Project

- **Location**: `/root/linux-code/simple-terraform-project`
- **Type**: S3 Static Website
- **Resources**: S3 bucket, objects, website configuration
- **Perfect for**: First-time cost analysis demo

## 🚀 Quick Start

1. **Setup**: Follow [01-setup.md](01-setup.md)
2. **Generate Plan**: Follow [02-terraform-plan.md](02-terraform-plan.md)
3. **Use Agent**: Follow [03-agent-interaction.md](03-agent-interaction.md) ⭐

## 💰 Expected Results

- **Monthly Cost**: ~$2.50 USD
- **Status**: Already cost-optimized
- **Optimization**: Regional alternatives save $0.20-0.46/month

## 🎯 Learning Outcomes

- ✅ How to interact with our DevOps Agent
- ✅ Real-time AWS pricing analysis  
- ✅ Cost optimization before deployment
- ✅ Natural language infrastructure analysis

---

**Start here**: [01-setup.md](01-setup.md) →