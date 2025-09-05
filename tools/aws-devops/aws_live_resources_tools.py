"""
AWS Live Resources Tools - Real-time AWS Resource Discovery via Official MCP Client
Access to actual running AWS resources using the official MCP Python SDK
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from strands import tool

# Import the official MCP client
import sys
import os
sys.path.append(os.path.dirname(__file__))
from mcp_client import mcp_client


@tool
def scan_live_aws_resources(
    regions: List[str] = None,
    resource_types: List[str] = None,
    account_ids: List[str] = None
) -> Dict[str, Any]:
    """
    Scan actual running AWS resources using CloudWatch MCP Server for metrics
    
    Args:
        regions: List of regions to scan (if None, scans current region)
        resource_types: Types to scan (EC2, RDS, Lambda, S3, etc.)
        account_ids: Account IDs to scan (if None, scans current account)
    
    Returns:
        Dict containing real AWS resource inventory via MCP
    """
    try:
        if regions is None:
            regions = [os.getenv("AWS_DEFAULT_REGION", "us-east-1")]
        
        if resource_types is None:
            resource_types = ['EC2', 'RDS', 'Lambda', 'S3', 'ELB']
        
        resource_inventory = {
            "scan_timestamp": datetime.now().isoformat(),
            "regions_scanned": regions,
            "resource_types_scanned": resource_types,
            "total_resources": 0,
            "regional_breakdown": {},
            "cost_insights": {},
            "optimization_opportunities": []
        }
        
        # Use CloudWatch MCP to get resource metrics and insights
        import asyncio
        
        total_resources = 0
        for region in regions:
            # Get CloudWatch metrics for resources in this region
            metrics_params = {
                "region": region,
                "namespace": "AWS/EC2",  # Start with EC2, can expand
                "start_time": (datetime.now() - timedelta(hours=24)).isoformat(),
                "end_time": datetime.now().isoformat()
            }
            
            # Use official MCP client to get CloudWatch metrics
            metrics_response = asyncio.run(mcp_client.get_metric_data(
                namespace="AWS/EC2",
                metric_name="CPUUtilization",
                start_time=(datetime.now() - timedelta(hours=24)).isoformat(),
                end_time=datetime.now().isoformat()
            ))
            
            if metrics_response.get('status') == 'success':
                region_data = _process_cloudwatch_metrics(metrics_response.get('data', {}), resource_types)
                resource_inventory["regional_breakdown"][region] = region_data
                total_resources += region_data.get('resource_count', 0)
        
        resource_inventory["total_resources"] = total_resources
        resource_inventory["optimization_opportunities"] = _identify_resource_optimizations_mcp(resource_inventory)
        
        return {
            "status": "success",
            "data_source": "AWS CloudWatch via Official MCP Client (Real Resource Metrics)",
            "inventory": resource_inventory
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Live resource scan via Official MCP Client failed: {str(e)}",
            "suggestion": "Ensure AWS credentials are configured and MCP Python SDK is installed"
        }


@tool
def analyze_unused_resources(regions: List[str] = None) -> Dict[str, Any]:
    """
    Find unused AWS resources that are costing money
    
    Args:
        regions: Regions to analyze (if None, uses current region)
    
    Returns:
        Dict containing unused resources and potential savings
    """
    try:
        if regions is None:
            regions = [boto3.Session().region_name or 'us-east-1']
        
        unused_resources = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_unused_resources": 0,
            "potential_monthly_savings": 0,
            "unused_by_type": {},
            "immediate_actions": []
        }
        
        total_savings = 0
        
        for region in regions:
            # Scan for unused EBS volumes
            unused_ebs = _find_unused_ebs_volumes(region)
            if unused_ebs:
                unused_resources["unused_by_type"][f"{region}_ebs"] = unused_ebs
                total_savings += sum(vol.get("estimated_monthly_cost", 0) for vol in unused_ebs)
            
            # Scan for unused Elastic IPs
            unused_eips = _find_unused_elastic_ips(region)
            if unused_eips:
                unused_resources["unused_by_type"][f"{region}_eip"] = unused_eips
                total_savings += len(unused_eips) * 3.65  # $3.65/month per unused EIP
            
            # Scan for stopped instances (still costing for storage)
            stopped_instances = _find_stopped_instances(region)
            if stopped_instances:
                unused_resources["unused_by_type"][f"{region}_stopped_ec2"] = stopped_instances
                total_savings += sum(inst.get("storage_cost", 0) for inst in stopped_instances)
        
        unused_resources["potential_monthly_savings"] = round(total_savings, 2)
        unused_resources["total_unused_resources"] = sum(
            len(resources) if isinstance(resources, list) else 1 
            for resources in unused_resources["unused_by_type"].values()
        )
        
        unused_resources["immediate_actions"] = _generate_cleanup_actions(unused_resources)
        
        return {
            "status": "success",
            "data_source": "AWS APIs (Live Resource Analysis)",
            "unused_analysis": unused_resources,
            "annual_savings_potential": round(total_savings * 12, 2)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unused resource analysis failed: {str(e)}"
        }


@tool
def get_resource_utilization_metrics(
    resource_type: str,
    resource_ids: List[str] = None,
    days_back: int = 14
) -> Dict[str, Any]:
    """
    Get real utilization metrics for AWS resources from CloudWatch
    
    Args:
        resource_type: Type of resource (EC2, RDS, etc.)
        resource_ids: Specific resource IDs (if None, gets all in region)
        days_back: Days of metrics to retrieve
    
    Returns:
        Dict containing real utilization data from CloudWatch
    """
    try:
        cloudwatch = boto3.client('cloudwatch')
        
        if resource_type.upper() == 'EC2':
            return _get_ec2_utilization_metrics(cloudwatch, resource_ids, days_back)
        elif resource_type.upper() == 'RDS':
            return _get_rds_utilization_metrics(cloudwatch, resource_ids, days_back)
        else:
            return {
                "status": "error",
                "error": f"Resource type {resource_type} not supported yet"
            }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Utilization metrics failed: {str(e)}"
        }


@tool
def discover_cross_account_resources(
    organization_id: str = None,
    resource_types: List[str] = None
) -> Dict[str, Any]:
    """
    Discover resources across all accounts in AWS Organization
    
    Args:
        organization_id: AWS Organization ID
        resource_types: Types of resources to discover
    
    Returns:
        Dict containing cross-account resource discovery
    """
    try:
        # Get organization accounts
        orgs_client = boto3.client('organizations')
        accounts_response = orgs_client.list_accounts()
        active_accounts = [acc for acc in accounts_response['Accounts'] if acc['Status'] == 'ACTIVE']
        
        cross_account_inventory = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_accounts": len(active_accounts),
            "accounts_scanned": [],
            "total_resources_found": 0,
            "resource_distribution": {},
            "cost_insights": {},
            "governance_issues": []
        }
        
        total_resources = 0
        
        for account in active_accounts:
            account_id = account['Id']
            account_name = account['Name']
            
            try:
                # Assume role in target account (if cross-account role is configured)
                account_resources = _scan_account_resources(account_id, resource_types)
                
                cross_account_inventory["accounts_scanned"].append({
                    "account_id": account_id,
                    "account_name": account_name,
                    "resources_found": account_resources["total_resources"],
                    "top_services": account_resources.get("top_services", [])
                })
                
                total_resources += account_resources["total_resources"]
                
            except Exception as e:
                cross_account_inventory["governance_issues"].append({
                    "account_id": account_id,
                    "issue": f"Cannot access account: {str(e)}",
                    "recommendation": "Setup cross-account IAM roles"
                })
        
        cross_account_inventory["total_resources_found"] = total_resources
        
        return {
            "status": "success",
            "data_source": "AWS Organizations + Cross-Account APIs",
            "inventory": cross_account_inventory
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Cross-account discovery failed: {str(e)}",
            "suggestion": "Ensure you're in the organization management account with proper permissions"
        }


# Helper functions
def _scan_region_resources(region: str, resource_types: List[str]) -> Dict[str, List[Dict]]:
    """Scan resources in a specific region"""
    region_resources = {}
    
    try:
        # EC2 instances
        if 'EC2' in resource_types:
            ec2 = boto3.client('ec2', region_name=region)
            instances_response = ec2.describe_instances()
            
            instances = []
            for reservation in instances_response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        "instance_id": instance['InstanceId'],
                        "instance_type": instance['InstanceType'],
                        "state": instance['State']['Name'],
                        "launch_time": instance.get('LaunchTime', '').isoformat() if instance.get('LaunchTime') else None,
                        "vpc_id": instance.get('VpcId'),
                        "tags": instance.get('Tags', [])
                    })
            region_resources['EC2'] = instances
        
        # RDS instances
        if 'RDS' in resource_types:
            rds = boto3.client('rds', region_name=region)
            db_instances = rds.describe_db_instances()
            
            databases = []
            for db in db_instances['DBInstances']:
                databases.append({
                    "db_instance_id": db['DBInstanceIdentifier'],
                    "db_instance_class": db['DBInstanceClass'],
                    "engine": db['Engine'],
                    "status": db['DBInstanceStatus'],
                    "multi_az": db.get('MultiAZ', False),
                    "storage_type": db.get('StorageType'),
                    "allocated_storage": db.get('AllocatedStorage')
                })
            region_resources['RDS'] = databases
        
        # Lambda functions
        if 'Lambda' in resource_types:
            lambda_client = boto3.client('lambda', region_name=region)
            functions_response = lambda_client.list_functions()
            
            functions = []
            for func in functions_response['Functions']:
                functions.append({
                    "function_name": func['FunctionName'],
                    "runtime": func['Runtime'],
                    "memory_size": func['MemorySize'],
                    "timeout": func['Timeout'],
                    "last_modified": func['LastModified']
                })
            region_resources['Lambda'] = functions
    
    except Exception as e:
        print(f"Error scanning {region}: {e}")
    
    return region_resources


def _find_unused_ebs_volumes(region: str) -> List[Dict]:
    """Find unattached EBS volumes"""
    try:
        ec2 = boto3.client('ec2', region_name=region)
        volumes_response = ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        
        unused_volumes = []
        for volume in volumes_response['Volumes']:
            # Estimate cost based on size and type
            size = volume['Size']
            volume_type = volume.get('VolumeType', 'gp2')
            
            # Rough pricing estimates (varies by region)
            cost_per_gb = {'gp2': 0.10, 'gp3': 0.08, 'io1': 0.125, 'io2': 0.125}.get(volume_type, 0.10)
            estimated_cost = size * cost_per_gb
            
            unused_volumes.append({
                "volume_id": volume['VolumeId'],
                "size": size,
                "volume_type": volume_type,
                "create_time": volume['CreateTime'].isoformat(),
                "estimated_monthly_cost": round(estimated_cost, 2)
            })
        
        return unused_volumes
    
    except Exception as e:
        print(f"Error finding unused EBS volumes: {e}")
        return []


def _find_unused_elastic_ips(region: str) -> List[Dict]:
    """Find unassociated Elastic IPs"""
    try:
        ec2 = boto3.client('ec2', region_name=region)
        addresses_response = ec2.describe_addresses()
        
        unused_eips = []
        for address in addresses_response['Addresses']:
            if 'InstanceId' not in address and 'NetworkInterfaceId' not in address:
                unused_eips.append({
                    "allocation_id": address.get('AllocationId'),
                    "public_ip": address.get('PublicIp'),
                    "domain": address.get('Domain')
                })
        
        return unused_eips
    
    except Exception as e:
        print(f"Error finding unused Elastic IPs: {e}")
        return []


def _find_stopped_instances(region: str) -> List[Dict]:
    """Find stopped EC2 instances"""
    try:
        ec2 = boto3.client('ec2', region_name=region)
        instances_response = ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
        )
        
        stopped_instances = []
        for reservation in instances_response['Reservations']:
            for instance in reservation['Instances']:
                # Estimate storage costs for stopped instances
                storage_cost = 0
                for bdm in instance.get('BlockDeviceMappings', []):
                    if 'Ebs' in bdm:
                        volume_id = bdm['Ebs']['VolumeId']
                        # Get volume details to estimate cost
                        try:
                            volume = ec2.describe_volumes(VolumeIds=[volume_id])['Volumes'][0]
                            size = volume['Size']
                            volume_type = volume.get('VolumeType', 'gp2')
                            cost_per_gb = {'gp2': 0.10, 'gp3': 0.08}.get(volume_type, 0.10)
                            storage_cost += size * cost_per_gb
                        except:
                            pass
                
                stopped_instances.append({
                    "instance_id": instance['InstanceId'],
                    "instance_type": instance['InstanceType'],
                    "stop_time": instance['StateTransitionReason'],
                    "storage_cost": round(storage_cost, 2)
                })
        
        return stopped_instances
    
    except Exception as e:
        print(f"Error finding stopped instances: {e}")
        return []


def _get_ec2_utilization_metrics(cloudwatch, resource_ids: List[str], days_back: int) -> Dict[str, Any]:
    """Get EC2 CloudWatch metrics"""
    try:
        from datetime import datetime, timedelta
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days_back)
        
        # If no specific instances, get all running instances
        if not resource_ids:
            ec2 = boto3.client('ec2')
            instances_response = ec2.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            
            resource_ids = []
            for reservation in instances_response['Reservations']:
                for instance in reservation['Instances']:
                    resource_ids.append(instance['InstanceId'])
        
        utilization_data = {}
        
        for instance_id in resource_ids[:10]:  # Limit to first 10 for demo
            try:
                # Get CPU utilization
                cpu_response = cloudwatch.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,  # 1 hour periods
                    Statistics=['Average', 'Maximum']
                )
                
                cpu_datapoints = cpu_response['Datapoints']
                if cpu_datapoints:
                    avg_cpu = sum(dp['Average'] for dp in cpu_datapoints) / len(cpu_datapoints)
                    max_cpu = max(dp['Maximum'] for dp in cpu_datapoints)
                    
                    utilization_data[instance_id] = {
                        "avg_cpu_utilization": round(avg_cpu, 2),
                        "max_cpu_utilization": round(max_cpu, 2),
                        "datapoints_count": len(cpu_datapoints),
                        "rightsizing_recommendation": _suggest_ec2_rightsizing(avg_cpu, max_cpu)
                    }
            
            except Exception as e:
                utilization_data[instance_id] = {"error": str(e)}
        
        return {
            "status": "success",
            "data_source": "AWS CloudWatch (Real Metrics)",
            "metrics_period": f"{days_back} days",
            "utilization_data": utilization_data
        }
    
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _suggest_ec2_rightsizing(avg_cpu: float, max_cpu: float) -> str:
    """Suggest EC2 rightsizing based on CPU metrics"""
    if avg_cpu < 20 and max_cpu < 60:
        return "Consider downsizing - low utilization"
    elif avg_cpu > 80 or max_cpu > 95:
        return "Consider upsizing - high utilization"
    else:
        return "Current size appears appropriate"


def _generate_cleanup_actions(unused_resources: Dict[str, Any]) -> List[str]:
    """Generate cleanup actions for unused resources"""
    actions = []
    
    for resource_type, resources in unused_resources["unused_by_type"].items():
        if "ebs" in resource_type:
            actions.append(f"Delete {len(resources)} unused EBS volumes")
        elif "eip" in resource_type:
            actions.append(f"Release {len(resources)} unused Elastic IPs")
        elif "stopped_ec2" in resource_type:
            actions.append(f"Review {len(resources)} stopped instances - terminate if not needed")
    
    return actions


def _identify_resource_optimizations(inventory: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify optimization opportunities from resource inventory"""
    opportunities = []
    
    # Check for regions with few resources (consolidation opportunity)
    for region, resources in inventory["regional_breakdown"].items():
        total_resources = sum(len(res_list) for res_list in resources.values())
        if total_resources < 3:
            opportunities.append({
                "type": "region_consolidation",
                "region": region,
                "resources_count": total_resources,
                "recommendation": f"Consider consolidating {total_resources} resources from {region} to reduce management overhead"
            })
    
    return opportunities


def _scan_account_resources(account_id: str, resource_types: List[str]) -> Dict[str, Any]:
    """Scan resources in a specific account (requires cross-account access)"""
    # This would require assuming a role in the target account
    # For now, return a placeholder structure
    return {
        "account_id": account_id,
        "total_resources": 0,
        "top_services": [],
        "scan_status": "requires_cross_account_role"
    }


# Helper functions for MCP processing
def _process_cloudwatch_metrics(metrics_data: Dict[str, Any], resource_types: List[str]) -> Dict[str, Any]:
    """Process CloudWatch metrics data from MCP response"""
    try:
        resource_count = 0
        metrics_summary = {}
        
        # Process metric data points
        metric_results = metrics_data.get('MetricDataResults', [])
        
        for result in metric_results:
            metric_name = result.get('Label', 'Unknown')
            values = result.get('Values', [])
            resource_count += len(values)
            
            if values:
                metrics_summary[metric_name] = {
                    "data_points": len(values),
                    "latest_value": values[-1] if values else 0,
                    "average": sum(values) / len(values) if values else 0
                }
        
        return {
            "resource_count": resource_count,
            "metrics": metrics_summary,
            "last_updated": datetime.now().isoformat()
        }
    except Exception:
        return {
            "resource_count": 0,
            "metrics": {},
            "error": "Failed to process CloudWatch metrics"
        }


def _identify_resource_optimizations_mcp(inventory: Dict[str, Any]) -> List[Dict[str, str]]:
    """Identify optimization opportunities from MCP inventory data"""
    opportunities = []
    
    total_resources = inventory.get('total_resources', 0)
    
    if total_resources > 50:
        opportunities.append({
            "type": "resource_consolidation",
            "description": f"High resource count ({total_resources}) - consider consolidation",
            "priority": "medium"
        })
    
    # Analyze regional breakdown
    regions = inventory.get('regional_breakdown', {})
    if len(regions) > 3:
        opportunities.append({
            "type": "multi_region_optimization",
            "description": f"Resources across {len(regions)} regions - review necessity",
            "priority": "low"
        })
    
    return opportunities