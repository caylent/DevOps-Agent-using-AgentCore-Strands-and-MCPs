#!/usr/bin/env python3
"""
Optimized Multi-threaded Bedrock Agent with Strands SDK
Fast processing of VM migration data with parallel execution.
"""

import asyncio
import concurrent.futures
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any
from urllib.parse import urlparse

import boto3
import pandas as pd
from strands import Agent

# Import tools
from tools.s3_tools import read_excel_from_s3
from tools.data_processing_tools import group_data_by_account_region
from tools.ec2_sizing_tools import generate_ec2_recommendations
from tools.dynamodb_tools import store_in_central_table
from tools.destination_account_tools import store_in_destination_accounts

class OptimizedStrandsProcessor:
    """Optimized processor using Strands SDK with threading."""
    
    def __init__(self):
        self.bedrock_region = os.getenv("BEDROCK_REGION", "us-east-1")
        self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
        self.max_workers = int(os.getenv("MAX_WORKERS", "10"))
        
        # Initialize Strands agent with optimized configuration
        self.agent = Agent(
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",
            tools=[
                read_excel_from_s3,
                group_data_by_account_region,
                generate_ec2_recommendations,
                store_in_central_table,
                store_in_destination_accounts,
            ],
            system_prompt="""You are an EC2 sizing specialist. Execute tasks efficiently:
1. Read Excel from S3
2. Group by account/region
3. Calculate EC2 recommendations
4. Store in central DynamoDB
5. Store in destination accounts
Be precise and fast."""
        )
        
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        
        if self.debug_mode:
            print(f"OptimizedStrandsProcessor initialized with {self.max_workers} workers")

    def parse_s3_path(self, s3_path: str) -> Dict[str, str]:
        """Parse S3 path into bucket and key."""
        if s3_path.startswith('s3://'):
            parsed = urlparse(s3_path)
            return {"bucket": parsed.netloc, "key": parsed.path.lstrip('/')}
        elif "/" in s3_path:
            parts = s3_path.split("/", 1)
            return {"bucket": parts[0], "key": parts[1]}
        else:
            return {"bucket": s3_path, "key": ""}

    async def step_1_read_excel(self, s3_path: str) -> Dict[str, Any]:
        """Step 1: Read Excel from S3."""
        start_time = time.time()
        
        try:
            s3_info = self.parse_s3_path(s3_path)
            bucket = s3_info["bucket"]
            key = s3_info["key"]
            
            if self.debug_mode:
                print(f"Step 1: Reading from s3://{bucket}/{key}")
            
            # Use tool directly for faster execution
            result = read_excel_from_s3(bucket, key)
            
            elapsed = time.time() - start_time
            if self.debug_mode:
                print(f"Step 1 completed in {elapsed:.2f}s - {result.get('rows', 0)} rows")
            
            return result
        except Exception as e:
            return {"status": "error", "error": f"Step 1 failed: {str(e)}"}

    async def step_2_group_data(self, data: List[Dict]) -> Dict[str, Any]:
        """Step 2: Group data by account and region."""
        start_time = time.time()
        
        try:
            if self.debug_mode:
                print(f"Step 2: Grouping {len(data)} VMs by account/region")
            
            result = group_data_by_account_region(data)
            
            elapsed = time.time() - start_time
            if self.debug_mode:
                print(f"Step 2 completed in {elapsed:.2f}s - {result.get('groups', 0)} groups")
            
            return result
        except Exception as e:
            return {"status": "error", "error": f"Step 2 failed: {str(e)}"}

    async def step_3_process_group(self, group_key: str, group_data: Dict, use_ai: bool) -> Dict[str, Any]:
        """Step 3: Process a single group (account/region) with EC2 sizing."""
        start_time = time.time()
        
        try:
            vms = group_data["data"]
            account_id = group_data["account_id"]
            region = group_data["region"]
            
            if self.debug_mode:
                print(f"Step 3: Processing {len(vms)} VMs for {account_id}/{region}")
            
            # Use tool directly for faster execution
            result = generate_ec2_recommendations(vms, use_ai=use_ai)
            
            # Add group metadata and inject account_id/region into each recommendation
            if result.get("status") == "success":
                result["group_key"] = group_key
                result["account_id"] = account_id
                result["region"] = region
                
                # CRITICAL: Add account_id and region to each individual recommendation
                if "recommendations" in result:
                    for rec in result["recommendations"]:
                        rec["account_id"] = account_id
                        rec["region"] = region
                        # Also add to metadata for DynamoDB flattening
                        if "metadata" in rec:
                            rec["metadata"]["AccountId"] = account_id
                            rec["metadata"]["Region"] = region
            
            elapsed = time.time() - start_time
            if self.debug_mode:
                print(f"Step 3 completed for {group_key} in {elapsed:.2f}s")
            
            return result
        except Exception as e:
            return {"status": "error", "error": f"Step 3 failed for {group_key}: {str(e)}"}

    async def step_4_store_central(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """Step 4: Store all recommendations in central DynamoDB."""
        start_time = time.time()
        
        try:
            if self.debug_mode:
                print(f"Step 4: Storing {len(recommendations)} recommendations in central DB")
            
            # Flatten all recommendations for storage
            all_recs = []
            for rec_group in recommendations:
                if rec_group.get("status") == "success" and "recommendations" in rec_group:
                    all_recs.extend(rec_group["recommendations"])
            
            result = store_in_central_table(all_recs)
            
            elapsed = time.time() - start_time
            if self.debug_mode:
                print(f"Step 4 completed in {elapsed:.2f}s - {result.get('stored_count', 0)} stored")
            
            return result
        except Exception as e:
            return {"status": "error", "error": f"Step 4 failed: {str(e)}"}

    async def step_5_store_destinations(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """Step 5: Store recommendations in destination accounts."""
        start_time = time.time()
        
        try:
            if self.debug_mode:
                print(f"Step 5: Storing recommendations in destination accounts")
            
            # Flatten all recommendations for destination storage
            all_recs = []
            for rec_group in recommendations:
                if rec_group.get("status") == "success" and "recommendations" in rec_group:
                    # Add account/region info to each recommendation
                    account_id = rec_group.get("account_id")
                    region = rec_group.get("region")
                    for rec in rec_group["recommendations"]:
                        rec["account_id"] = account_id
                        rec["region"] = region
                        all_recs.append(rec)
            
            result = store_in_destination_accounts(all_recs)
            
            elapsed = time.time() - start_time
            if self.debug_mode:
                print(f"Step 5 completed in {elapsed:.2f}s")
            
            return result
        except Exception as e:
            return {"status": "error", "error": f"Step 5 failed: {str(e)}"}

    async def process_workflow(self, s3_path: str, use_ai: bool = False, project_id: str = "default") -> Dict[str, Any]:
        """Execute the complete workflow with optimized threading."""
        workflow_start = time.time()
        
        try:
            if self.debug_mode:
                print(f"Starting optimized workflow for {s3_path}")
            
            # Step 1: Read Excel from S3
            excel_result = await self.step_1_read_excel(s3_path)
            if excel_result.get("status") != "success":
                return excel_result
            
            vm_data = excel_result.get("data", [])
            if not vm_data:
                return {"status": "error", "error": "No VM data found in Excel file"}
            
            # Step 2: Group data by account/region
            group_result = await self.step_2_group_data(vm_data)
            if group_result.get("status") != "success":
                return group_result
            
            grouped_data = group_result.get("grouped_data", {})
            if not grouped_data:
                return {"status": "error", "error": "No groups created from VM data"}
            
            # Step 3: Process all groups in parallel
            if self.debug_mode:
                print(f"Processing {len(grouped_data)} groups in parallel")
            
            # Create tasks for parallel processing
            tasks = []
            for group_key, group_data in grouped_data.items():
                task = self.step_3_process_group(group_key, group_data, use_ai)
                tasks.append(task)
            
            # Execute all group processing in parallel
            group_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter successful results
            successful_results = []
            for result in group_results:
                if isinstance(result, dict) and result.get("status") == "success":
                    successful_results.append(result)
                elif isinstance(result, Exception):
                    if self.debug_mode:
                        print(f"Group processing error: {result}")
            
            if not successful_results:
                return {"status": "error", "error": "No groups processed successfully"}
            
            # Step 4 & 5: Store results in parallel
            storage_tasks = [
                self.step_4_store_central(successful_results),
                self.step_5_store_destinations(successful_results)
            ]
            
            storage_results = await asyncio.gather(*storage_tasks, return_exceptions=True)
            central_result, destination_result = storage_results
            
            # Calculate totals
            total_vms = sum(len(r.get("recommendations", [])) for r in successful_results)
            
            workflow_elapsed = time.time() - workflow_start
            
            return {
                "status": "success",
                "processing_time": f"{workflow_elapsed:.2f}s",
                "total_vms_processed": total_vms,
                "groups_processed": len(successful_results),
                "central_storage": central_result if not isinstance(central_result, Exception) else {"status": "error"},
                "destination_storage": destination_result if not isinstance(destination_result, Exception) else {"status": "error"},
                "use_ai": use_ai,
                "project_id": project_id
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "error": f"Workflow failed: {str(e)}",
                "processing_time": f"{time.time() - workflow_start:.2f}s"
            }

    def close(self):
        """Clean up resources."""
        self.executor.shutdown(wait=True)

# Global processor instance
processor = OptimizedStrandsProcessor()


async def main_handler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for the optimized processor."""
    try:
        # Extract parameters
        s3_path = payload.get("s3_path", payload.get("input", {}).get("s3_path"))
        use_ai = payload.get("use_ai", payload.get("input", {}).get("use_ai", False))
        project_id = payload.get("project_id", payload.get("input", {}).get("project_id", "default"))
        
        if not s3_path:
            return {"status": "error", "error": "s3_path is required"}
        
        # Process workflow
        result = await processor.process_workflow(s3_path, use_ai, project_id)
        return result
        
    except Exception as e:
        return {"status": "error", "error": f"Handler failed: {str(e)}"}


def sync_handler(payload):
    """Synchronous wrapper for async handler."""
    try:
        # Run the async handler
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(main_handler(payload))
            return result
        finally:
            loop.close()
    except Exception as e:
        return {"status": "error", "error": f"Sync handler failed: {str(e)}"}

if __name__ == "__main__":
    # Test mode
    if len(sys.argv) > 1:
        test_payload = {
            "s3_path": sys.argv[1],
            "use_ai": len(sys.argv) > 2 and sys.argv[2].lower() == "true",
            "project_id": sys.argv[3] if len(sys.argv) > 3 else "test-project"
        }
        
        print(f"Testing optimized processor with payload: {test_payload}")
        result = sync_handler(test_payload)
        print(f"Result: {json.dumps(result, indent=2)}")
    else:
        print("Usage: python optimized_processor.py <s3_path> [use_ai] [project_id]")
        print("Example: python optimized_processor.py s3://my-bucket/vms.xlsx true my-project")