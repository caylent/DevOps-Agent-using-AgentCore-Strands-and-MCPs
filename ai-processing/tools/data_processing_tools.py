"""Data processing tools for the agent"""

from typing import Dict, List

import pandas as pd
from strands import tool


@tool
def group_data_by_account_region(data: List[Dict]) -> dict:
    """
    Group data by account_id and region.

    Args:
        data: List of dictionaries containing the data

    Returns:
        Dictionary with grouped data
    """
    try:
        df = pd.DataFrame(data)

        # Handle both AccountId/account_id and Region/region field names
        account_field = "AccountId" if "AccountId" in df.columns else "account_id"
        region_field = "Region" if "Region" in df.columns else "region"

        # Group by account and region (pandas future-compatible)
        grouped = df.groupby([account_field, region_field], group_keys=False).apply(
            lambda x: x.to_dict("records"), include_groups=False
        ).to_dict()

        result = {}
        for (account_id, region), records in grouped.items():
            key = f"{account_id}_{region}"
            result[key] = {"account_id": account_id, "region": region, "count": len(records), "data": records}

        return {"status": "success", "groups": len(result), "grouped_data": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool
def generate_ec2_recommendations_with_ai(vm_data: List[Dict], agent) -> dict:
    """
    Generate EC2 instance recommendations using AI analysis.

    Args:
        vm_data: List of VM specifications with rich metadata
        agent: The Strands agent instance for AI analysis

    Returns:
        AI-powered EC2 recommendations
    """
    try:
        recommendations = []

        for vm in vm_data:
            # Extract VM details
            vm_name = vm.get("name", "unknown")
            cpus = vm.get("cpu", vm.get("cpus", 1))
            memory_gb = vm.get("memory_gb", vm.get("memory", 1))

            # Build utilization info if available
            utilization_info = ""
            if vm.get("cpu_utilization"):
                utilization_info += f"\n- CPU Utilization: {vm.get('cpu_utilization')}%"
            if vm.get("memory_utilization"):
                utilization_info += f"\n- Memory Utilization: {vm.get('memory_utilization')}%"
            if vm.get("disk_iops"):
                utilization_info += f"\n- Disk IOPS: {vm.get('disk_iops')}"

            # Build workload info if available
            workload_info = ""
            if vm.get("workload_type"):
                workload_info += f"\n- Workload Type: {vm.get('workload_type')}"
            if vm.get("application"):
                workload_info += f"\n- Application: {vm.get('application')}"
            if vm.get("environment"):
                workload_info += f"\n- Environment: {vm.get('environment')}"
            if vm.get("criticality"):
                workload_info += f"\n- Criticality: {vm.get('criticality')}"

            # Create AI prompt
            prompt = f"""You are an AWS EC2 instance sizing expert. Analyze the following VM specifications and recommend the most appropriate EC2 instance type for migration.

VM Details:
- VM Name: {vm_name}
- CPUs: {cpus}
- Memory: {memory_gb} GB{utilization_info}{workload_info}

Requirements:
1. Recommend the PRIMARY instance type that best matches the specifications
2. Provide 1-2 ALTERNATIVE options (smaller/larger) for different scenarios
3. Consider cost optimization vs performance balance
4. Account for AWS overhead and recommended headroom

Please respond in JSON format only:
{{
    "primary_instance": "instance-type",
    "alternatives": [
        {{
            "instance_type": "smaller-option",
            "use_case": "cost-optimized scenario"
        }},
        {{
            "instance_type": "larger-option",
            "use_case": "performance-optimized scenario"
        }}
    ],
    "reasoning": "Brief explanation of why this instance type was chosen",
    "cost_considerations": "Cost impact summary",
    "confidence": "high|medium|low"
}}

Focus on:
- General purpose instances (t3, m5, m6i) for balanced workloads
- Compute optimized (c5, c6i) for CPU-intensive applications
- Memory optimized (r5, r6i) for memory-intensive applications
- Consider burstable instances (t3) for variable workloads
- Avoid legacy instance types

Respond with valid JSON only, no additional text."""

            # Get AI recommendation
            try:
                ai_response = agent(prompt)
                import json

                ai_recommendation = json.loads(ai_response)

                recommendations.append(
                    {
                        "vm_name": vm_name,
                        "current_specs": {
                            "cpu": cpus,
                            "memory_gb": memory_gb,
                            "utilization": vm.get("cpu_utilization"),
                            "workload_type": vm.get("workload_type"),
                        },
                        "ai_recommendation": ai_recommendation,
                        "metadata": vm,  # Keep original metadata
                    }
                )
            except Exception as ai_error:
                # Fallback to basic logic if AI fails
                if cpus <= 2 and memory_gb <= 4:
                    instance_type = "t3.small"
                elif cpus <= 4 and memory_gb <= 8:
                    instance_type = "t3.medium"
                elif cpus <= 8 and memory_gb <= 16:
                    instance_type = "t3.large"
                else:
                    instance_type = "t3.xlarge"

                recommendations.append(
                    {
                        "vm_name": vm_name,
                        "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                        "fallback_recommendation": instance_type,
                        "ai_error": str(ai_error),
                        "metadata": vm,
                    }
                )

        return {"status": "success", "recommendations": recommendations, "total_vms": len(recommendations), "ai_powered": True}
    except Exception as e:
        return {"status": "error", "error": str(e)}
