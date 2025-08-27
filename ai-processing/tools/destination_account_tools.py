"""Tools for storing data in destination accounts"""

import boto3
import json
import os
import time
from decimal import Decimal
from typing import List, Dict
from strands import tool


def convert_floats_to_decimal(obj):
    """Convert floats to Decimal for DynamoDB compatibility and handle NaN/Infinity."""
    import math
    
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return "null"  # Convert NaN/Infinity to string
        return Decimal(str(obj))
    elif isinstance(obj, dict):
        return {k: convert_floats_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_floats_to_decimal(v) for v in obj]
    else:
        return obj

@tool
def store_in_destination_accounts(recommendations: List[Dict]) -> dict:
    """
    Store VM recommendations in destination account DynamoDB tables.
    
    Args:
        recommendations: List of VM recommendations with account/region info
    
    Returns:
        Storage results for each destination account
    """
    try:
        results = {}
        
        # Group recommendations by account_id and region
        account_groups = {}
        for rec in recommendations:
            account_id = rec.get('account_id', 'unknown')
            region = rec.get('region', 'us-east-1')
            key = f"{account_id}_{region}"
            
            if key not in account_groups:
                account_groups[key] = {
                    'account_id': account_id,
                    'region': region,
                    'recommendations': []
                }
            account_groups[key]['recommendations'].append(rec)
        
        # Store in each destination account
        for group_key, group_data in account_groups.items():
            account_id = group_data['account_id']
            region = group_data['region']
            recs = group_data['recommendations']
            
            try:
                # Assume cross-account role or use local credentials
                table_name = os.environ.get('DESTINATION_TABLE_NAME', 'vm-migration-recommendations')
                
                # Create DynamoDB client for the target region
                dynamodb = boto3.resource('dynamodb', region_name=region)
                table = dynamodb.Table(table_name)
                
                # Store each recommendation
                stored_count = 0
                for rec in recs:
                    # Create item for DynamoDB
                    item = {
                        'vm_name': rec['vm_name'],
                        'account_id': account_id,
                        'region': region,
                        'current_specs': rec.get('current_specs', {}),
                        'recommendation': rec.get('recommendation', {}),
                        'timestamp': str(int(time.time() * 1000)),
                        'metadata': rec.get('metadata', {})
                    }
                    
                    # Convert floats to Decimal for DynamoDB
                    item = convert_floats_to_decimal(item)
                    
                    # Store in DynamoDB
                    table.put_item(Item=item)
                    stored_count += 1
                
                results[group_key] = {
                    'status': 'success',
                    'account_id': account_id,
                    'region': region,
                    'stored_count': stored_count,
                    'table_name': table_name
                }
                
            except Exception as e:
                results[group_key] = {
                    'status': 'error',
                    'account_id': account_id,
                    'region': region,
                    'error': str(e)
                }
        
        # Summary
        total_stored = sum(r.get('stored_count', 0) for r in results.values())
        success_count = sum(1 for r in results.values() if r['status'] == 'success')
        
        return {
            'status': 'completed',
            'total_recommendations': len(recommendations),
            'total_stored': total_stored,
            'destination_accounts': len(results),
            'successful_accounts': success_count,
            'results': results
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

@tool
def create_destination_tables(account_regions: List[Dict]) -> dict:
    """
    Create DynamoDB tables in destination accounts if they don't exist.
    
    Args:
        account_regions: List of {account_id, region} combinations
    
    Returns:
        Table creation results
    """
    try:
        results = {}
        table_name = os.environ.get('DESTINATION_TABLE_NAME', 'vm-migration-recommendations')
        
        for account_region in account_regions:
            account_id = account_region['account_id']
            region = account_region['region']
            key = f"{account_id}_{region}"
            
            try:
                # Create DynamoDB client
                dynamodb = boto3.client('dynamodb', region_name=region)
                
                # Check if table exists
                try:
                    dynamodb.describe_table(TableName=table_name)
                    results[key] = {
                        'status': 'exists',
                        'account_id': account_id,
                        'region': region,
                        'table_name': table_name
                    }
                except dynamodb.exceptions.ResourceNotFoundException:
                    # Create table
                    table_definition = {
                        'TableName': table_name,
                        'KeySchema': [
                            {'AttributeName': 'vm_name', 'KeyType': 'HASH'},
                            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                        ],
                        'AttributeDefinitions': [
                            {'AttributeName': 'vm_name', 'AttributeType': 'S'},
                            {'AttributeName': 'timestamp', 'AttributeType': 'S'}
                        ],
                        'BillingMode': 'PAY_PER_REQUEST',
                        'Tags': [
                            {'Key': 'Purpose', 'Value': 'VM-Migration-Recommendations'},
                            {'Key': 'CreatedBy', 'Value': 'IaC-Polyglot'}
                        ]
                    }
                    
                    dynamodb.create_table(**table_definition)
                    
                    results[key] = {
                        'status': 'created',
                        'account_id': account_id,
                        'region': region,
                        'table_name': table_name
                    }
                    
            except Exception as e:
                results[key] = {
                    'status': 'error',
                    'account_id': account_id,
                    'region': region,
                    'error': str(e)
                }
        
        return {
            'status': 'completed',
            'results': results,
            'total_accounts': len(account_regions)
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }