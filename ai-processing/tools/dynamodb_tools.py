"""DynamoDB tools for the agent"""

import os
from datetime import datetime
from typing import Dict

import boto3

# Remove strands dependency for local execution
try:
    from strands import tool
except ImportError:
    # Fallback decorator for local execution
    def tool(func):
        return func


def clean_nan_values(obj):
    """Clean NaN and Infinity values for DynamoDB compatibility."""
    import math
    
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return "null"
        return obj
    elif isinstance(obj, dict):
        return {k: clean_nan_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan_values(v) for v in obj]
    else:
        return obj


def flatten_for_dynamodb(data):
    """Flatten nested structures for minimal DynamoDB storage"""
    # First clean NaN values
    data = clean_nan_values(data)
    flattened = {}

    # Store only ESSENTIAL fields to reduce size and prevent timeouts
    if "metadata" in data and isinstance(data["metadata"], dict):
        metadata = data["metadata"]
        
        # Essential fields only
        flattened["account_id"] = str(metadata.get("AccountId", ""))
        flattened["region"] = str(metadata.get("Region", ""))
        flattened["vm"] = str(metadata.get("VM", data.get("vm_name", "unknown")))
        flattened["wave"] = str(metadata.get("wave", "default"))
        flattened["project_id"] = str(metadata.get("ProjectId", ""))
        flattened["cpu"] = str(metadata.get("cpu", ""))
        flattened["memory"] = str(metadata.get("memory", ""))
        flattened["instance_type"] = str(metadata.get("instance type", ""))

    # Set VMKeyID from VM column - this is required for DynamoDB
    vm_key_id = None

    # Simple VM name extraction - prioritize vm_name field
    vm_key_id = (
        data.get("vm_name") or 
        data.get("VM") or 
        flattened.get("vm") or 
        (data.get("metadata", {}).get("VM") if "metadata" in data else None) or
        "unknown_vm"
    )
    
    # Ensure it's a clean string
    vm_key_id = str(vm_key_id).strip() if vm_key_id else "unknown_vm"
    
    # Set the required fields
    flattened["VMKeyID"] = vm_key_id
    flattened["vm_name"] = vm_key_id
    print(f"DEBUG: VMKeyID set to: {vm_key_id}")

    # Ensure required fields for GSI are present and force string conversion
    if "wave" not in flattened:
        if "metadata" in data:
            flattened["wave"] = str(data["metadata"].get("wave", "default"))
        else:
            flattened["wave"] = "default"
    
    # Fix account_id extraction - prioritize metadata
    if "metadata" in data and data["metadata"].get("AccountId"):
        flattened["account_id"] = str(data["metadata"]["AccountId"])
    elif "account_id" in data and data["account_id"]:
        flattened["account_id"] = str(data["account_id"])
    elif "account_id" in flattened and flattened["account_id"]:
        flattened["account_id"] = str(flattened["account_id"])
    else:
        flattened["account_id"] = "unknown"
    if "region" not in flattened or flattened["region"] == "":
        if "metadata" in data:
            region_value = data["metadata"].get("Region", "us-east-1")
            flattened["region"] = str(region_value) if region_value else "us-east-1"
        else:
            flattened["region"] = "us-east-1"
    
    # Ensure region is never empty for DynamoDB RegionIndex
    if not flattened["region"] or flattened["region"] == "":
        flattened["region"] = "us-east-1"

    # Process other fields
    for key, value in data.items():
        if key == "metadata":  # Skip metadata as we already processed it
            continue
        elif isinstance(value, dict):
            # Flatten nested dictionaries
            if key == "current_specs":
                flattened["current_cpu"] = str(value.get("cpu", 0))
                flattened["current_memory_gb"] = str(value.get("memory_gb", value.get("memory", 0)))
            elif key == "recommendation":
                # ALWAYS put the recommendation in instance_type field
                recommended_instance = value.get("primary_instance", "unknown")
                flattened["instance_type"] = recommended_instance
                
                # Consolidate all recommendation details into single JSON field
                import json
                recommendation_details = {
                    "instance": recommended_instance,
                    "manufacturer": value.get("manufacturer", ""),
                    "vcpus": value.get("vcpus", ""),
                    "memory_gb": value.get("memory_gb", ""),
                    "price": value.get("price", ""),
                    "generation": value.get("generation", ""),
                    "method": value.get("method", "unknown")
                }
                flattened["recommendation_details"] = json.dumps(recommendation_details)
                
                # Keep reasoning separate but limited
                reasoning = value.get("reasoning", "")
                flattened["reasoning"] = reasoning[:400] + "..." if len(reasoning) > 400 else reasoning
                
                # Store only top 3 alternatives to limit size
                alternatives = value.get("alternatives", [])
                if alternatives and len(alternatives) > 0:
                    alt_strings = []
                    for alt in alternatives[:3]:  # Only first 3 alternatives
                        if isinstance(alt, dict) and alt.get("instance_type"):
                            alt_str = alt.get('instance_type', '')
                            alt_strings.append(alt_str)
                    flattened["alternatives"] = ", ".join(alt_strings) if alt_strings else ""
                else:
                    flattened["alternatives"] = ""
            else:
                # For other nested objects, convert to string
                flattened[key] = str(value)
        elif isinstance(value, list):
            # Convert lists to comma-separated strings with underscore key format
            underscore_key = key.lower().replace(" ", "_").replace("-", "_")
            flattened[underscore_key] = ", ".join([str(item) for item in value])
        else:
            # Convert field names to underscore format for non-metadata fields
            if key == "AccountId":
                flattened["account_id"] = str(value) if value is not None else ""
            elif key == "Region":
                flattened["region"] = str(value) if value is not None else ""
            elif key == "VM":
                flattened["vm"] = str(value) if value is not None else ""
            elif key == "ProjectId":
                flattened["project_id"] = str(value) if value is not None else ""
            elif key == "SourceIpAddress":
                flattened["source_ip_address"] = str(value) if value is not None else ""
            elif key == "SSMKey":
                flattened["ssm_key"] = str(value) if value is not None else ""
            elif key == "Tags":
                flattened["tags"] = str(value) if value is not None else ""
            elif key == "Testing Subnet":
                flattened["testing_subnet"] = str(value) if value is not None else ""
            elif key == "Testing Security Groups":
                flattened["testing_security_groups"] = str(value) if value is not None else ""
            elif key == "Prod Subnet":
                flattened["prod_subnet"] = str(value) if value is not None else ""
            elif key == "Prod Security Groups":
                flattened["prod_security_groups"] = str(value) if value is not None else ""
            elif key == "Public Ip":
                flattened["public_ip"] = str(value) if value is not None else ""
            elif key == "instance type":
                flattened["instance_type"] = str(value) if value is not None else ""
            elif key == "boot mode":
                flattened["boot_mode"] = str(value) if value is not None else ""
            else:
                # Convert other field names to underscore format
                underscore_key = key.lower().replace(" ", "_").replace("-", "_")
                flattened[underscore_key] = str(value) if value is not None else ""

    # Final cleanup - ensure all values are strings for DynamoDB
    for key, value in flattened.items():
        if value is None:
            flattened[key] = ""
        else:
            flattened[key] = str(value)

    return flattened


@tool
def store_in_central_table(data: Dict, table_name: str = None) -> dict:
    """
    Store data in central DynamoDB table.

    Args:
        data: Data to store
        table_name: DynamoDB table name

    Returns:
        Storage result
    """
    try:
        # Use environment variable or default - ALWAYS use shared-mapping-table
        if not table_name:
            table_name = os.environ.get("CENTRAL_TABLE_NAME", "shared-mapping-table")

        # Force correct table name
        if table_name != "shared-mapping-table":
            table_name = "shared-mapping-table"

        print(f"DEBUG: Attempting to connect to table: {table_name} in region: {os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')}")
        dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
        table = dynamodb.Table(table_name)
        print(f"DEBUG: Table object created: {table}")

        # Handle list of recommendations or single item
        if isinstance(data, list):
            # Store multiple items - each VM gets its own record
            stored_count = 0
            errors = []

            for item_data in data:
                try:
                    # Check if this is a grouped recommendation with multiple VMs
                    if "recommendations" in item_data and isinstance(item_data["recommendations"], list):
                        # Store each VM recommendation separately
                        for vm_rec in item_data["recommendations"]:
                            vm_item = flatten_for_dynamodb(vm_rec)
                            vm_item["timestamp"] = datetime.utcnow().isoformat()
                            vm_item["processed_by"] = "ec2-sizer-agent"
                            table.put_item(Item=vm_item)
                            stored_count += 1
                    else:
                        # Single VM recommendation
                        item = flatten_for_dynamodb(item_data)
                        item["timestamp"] = datetime.utcnow().isoformat()
                        item["processed_by"] = "ec2-sizer-agent"
                        table.put_item(Item=item)
                        stored_count += 1
                except Exception as e:
                    error_msg = str(e)
                    errors.append(error_msg)
                    print(f"DEBUG: Error storing item: {error_msg}")

            if errors:
                print(f"DEBUG: Storage errors: {errors}")
            
            return {
                "status": "success" if stored_count > 0 else "error",
                "stored_count": stored_count,
                "errors": errors if errors else None
            }
        else:
            # Handle single item - could be grouped or individual
            if "recommendations" in data and isinstance(data["recommendations"], list):
                # Store each VM recommendation separately
                stored_count = 0
                for vm_rec in data["recommendations"]:
                    vm_item = flatten_for_dynamodb(vm_rec)
                    vm_item["timestamp"] = datetime.utcnow().isoformat()
                    vm_item["processed_by"] = "ec2-sizer-agent"
                    table.put_item(Item=vm_item)
                    stored_count += 1

                return {"status": "success", "stored_count": stored_count}
            else:
                # Single VM recommendation
                item = flatten_for_dynamodb(data)
                item["timestamp"] = datetime.utcnow().isoformat()
                item["processed_by"] = "ec2-sizer-agent"

            try:
                table.put_item(Item=item)
                return {"status": "success", "stored_count": 1}
            except Exception as e:
                print(f"DEBUG: Single item storage error: {str(e)}")
                return {"status": "error", "stored_count": 0, "error": str(e)}
    except Exception as e:
        print(f"DEBUG: DynamoDB connection error: {str(e)}")
        print(f"DEBUG: Table name used: {table_name}")
        return {"status": "error", "message": f"Storage failed: {str(e)}"}


@tool
def store_in_destination_table(data: Dict, account_id: str, region: str, role_arn: str) -> dict:
    """
    Store data in destination account DynamoDB table using cross-account role.

    Args:
        data: Data to store
        account_id: Destination account ID
        region: AWS region
        role_arn: Cross-account role ARN

    Returns:
        Storage result
    """
    try:
        # Assume cross-account role
        sts = boto3.client("sts")
        assumed_role = sts.assume_role(RoleArn=role_arn, RoleSessionName=f"ec2-sizer-{account_id}")

        credentials = assumed_role["Credentials"]

        # Create DynamoDB client with assumed role
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=region,
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )

        table_name = f"{account_id}-{region}-mapping-table"
        table = dynamodb.Table(table_name)

        # Add metadata
        item = {**data, "timestamp": datetime.utcnow().isoformat(), "processed_by": "ec2-sizer-agent", "account_id": account_id, "region": region}

        table.put_item(Item=item)

        return {"status": "success", "table": table_name, "account_id": account_id, "region": region}
    except Exception as e:
        return {"status": "error", "error": str(e), "account_id": account_id, "region": region}
