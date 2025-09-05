# ⚡ QUICK SETUP - MCP Servers Ready in 2 Minutes

## 1️⃣ Install UV (if not installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# OR
pip install uv
```

## 2️⃣ Install AWS MCP Servers (1 command)
```bash
uvx install awslabs.cost-explorer-mcp-server@latest && \
uvx install awslabs.cloudwatch-mcp-server@latest && \
uvx install awslabs.aws-pricing-mcp-server@latest
```

## 3️⃣ Configure AWS Credentials (if not done)
```bash
aws configure
# OR set environment variables:
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## 4️⃣ Test MCP Integration
```bash
python test_mcp_integration.py
```

## 5️⃣ Run the Agent
```bash
python aws_devops_agent_v2.py --mode interactive
```

## ✅ Done! 
Your AWS DevOps Agent now has real MCP integration with:
- Real AWS Cost Explorer data
- Real CloudWatch metrics and alarms  
- Real AWS pricing information
- Official MCP Python SDK

## 🔧 IAM Permissions Needed:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetForecast",
                "cloudwatch:GetMetricData",
                "cloudwatch:DescribeAlarms",
                "logs:StartQuery",
                "logs:GetQueryResults"
            ],
            "Resource": "*"
        }
    ]
}
```

That's it! 🎯