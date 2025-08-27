"""AI-powered EC2 sizing tools"""

import hashlib
import json
import os
import time
from typing import Dict, List

import pandas as pd
from strands import Agent

# Simple in-memory cache for AI responses
AI_CACHE = {}
CACHE_TTL = 3600  # 1 hour cache
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Remove strands dependency for local execution
try:
    from strands import tool
except ImportError:
    # Fallback decorator for local execution
    def tool(func):
        return func


# Load EC2 instance data
def load_ec2_instance_data():
    """Load EC2 instance comparison data from CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), "data", "Amazon EC2 Instance Comparison.csv")
    try:
        df = pd.read_csv(csv_path)
        # Clean price column - remove $ and convert to float
        df["Price"] = df["Price"].replace("N/A", "0").str.replace("$", "").astype(float)
        # Convert memory from MiB to GB for easier comparison
        df["MemoryGB"] = df["MemoryMiB"] / 1024
        return df
    except Exception as e:
        print(f"Error loading EC2 data: {e}")
        return None


def get_cache_key(vm_specs: dict) -> str:
    """Generate cache key for VM specifications"""
    cache_data = {
        "cpu": vm_specs.get("cpu", 1),
        "memory": vm_specs.get("memory", 1024),
        "manufacturer": vm_specs.get("manufacturer", "Intel"),
        "server_stats": vm_specs.get("server_statistics", vm_specs.get("server_stats", ""))
    }
    return hashlib.md5(json.dumps(cache_data, sort_keys=True).encode()).hexdigest()

def get_cached_recommendation(cache_key: str) -> dict:
    """Get cached recommendation if valid"""
    if cache_key in AI_CACHE:
        cached_data = AI_CACHE[cache_key]
        if time.time() - cached_data["timestamp"] < CACHE_TTL:
            print(f"Using cached recommendation for key: {cache_key[:8]}...")
            return cached_data["recommendation"]
        else:
            del AI_CACHE[cache_key]
    return None

def cache_recommendation(cache_key: str, recommendation: dict):
    """Cache AI recommendation"""
    AI_CACHE[cache_key] = {
        "timestamp": time.time(),
        "recommendation": recommendation
    }
    print(f"Cached recommendation for key: {cache_key[:8]}...")

def ai_call_with_retry(sizing_agent, prompt: str, max_retries: int = MAX_RETRIES) -> str:
    """Make AI call with timeout and retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"AI call attempt {attempt + 1}/{max_retries}")
            # Set timeout context (simplified - actual timeout would need async implementation)
            response = sizing_agent(prompt)
            
            # Handle AgentResult object properly
            if hasattr(response, 'content'):
                return response.content
            elif hasattr(response, 'text'):
                return response.text
            else:
                return str(response)
                
        except Exception as e:
            print(f"AI call attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception("All AI call attempts failed")

@tool
def generate_ec2_recommendations_ai(vm_data: List[Dict], manufacturer: str = "Intel") -> dict:
    """
    Generate EC2 instance recommendations using AI analysis with CSV data context.

    Args:
        vm_data: List of VM specifications
        manufacturer: Preferred manufacturer

    Returns:
        AI-powered EC2 recommendations
    """
    try:
        # Load CSV data for AI context
        df = load_ec2_instance_data()
        if df is None:
            return {"status": "error", "error": "Could not load EC2 instance data"}

        # Create specialized AI agent for EC2 sizing (using Nova for cost optimization)
        sizing_agent = Agent(
            model="us.amazon.nova-micro-v1:0",
            system_prompt="""You are an AWS EC2 cost optimization expert. Analyze server statistics and recommend the cheapest instance from the newest generation that meets all requirements. NEVER recommend T-instances. Always respond with valid JSON only."""
        )

        recommendations = []

        for vm in vm_data:
            vm_name = vm.get("VM", vm.get("name", "unknown"))
            cpus = vm.get("cpu", 1)
            memory_mb = vm.get("memory", 1024)
            memory_gb = memory_mb / 1024 if memory_mb > 100 else memory_mb
            vm_manufacturer = vm.get("manufacturer", manufacturer)

            # Check if instance type is pre-defined
            predefined_instance = vm.get("instance type", vm.get("instance_type"))
            if (
                predefined_instance
                and str(predefined_instance).strip()
                and str(predefined_instance).strip().lower() not in ["", "nan", "none", "null"]
            ):
                recommendations.append(
                    {
                        "vm_name": vm_name,
                        "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                        "recommendation": {
                            "primary_instance": str(predefined_instance).strip(),
                            "manufacturer": vm_manufacturer,
                            "reasoning": f"Pre-defined instance type from Excel: {predefined_instance}",
                            "method": "predefined",
                            "alternatives": [],
                        },
                        "metadata": vm,
                    }
                )
                continue

            # Get suitable instances for AI analysis - EXCLUDE T-instances and FILTER by manufacturer
            # Sort by generation (newest first) then by price (cheapest first)
            manufacturer_filter = df["Manufacturer"].str.contains(vm_manufacturer, case=False, na=False)
            
            # If no instances match the specified manufacturer, fall back to Intel as default
            if not manufacturer_filter.any():
                print(f"No instances found for manufacturer '{vm_manufacturer}', defaulting to Intel")
                manufacturer_filter = df["Manufacturer"].str.contains("Intel", case=False, na=False)
            
            suitable_instances = df[
                (df["VCpus"] >= cpus)
                & (df["MemoryGB"] >= memory_gb)
                & (df["Price"] > 0)
                & (~df["InstanceType"].str.startswith("t"))  # EXCLUDE T-instances
                & manufacturer_filter  # FILTER by manufacturer preference
            ].copy()
            
            # Extract generation number for sorting (7th gen > 6th gen > 5th gen)
            suitable_instances["generation"] = suitable_instances["InstanceType"].str.extract(r'([0-9]+)').astype(int)
            
            # Sort by generation (descending) then price (ascending) for cost optimization
            suitable_instances = (
                suitable_instances
                .sort_values(["generation", "Price"], ascending=[False, True])
                .head(20)
            )

            # Prepare instance options for AI with generation info
            instance_options = []
            for _, row in suitable_instances.iterrows():
                instance_options.append(
                    {
                        "type": row["InstanceType"],
                        "vcpus": int(row["VCpus"]),
                        "memory_gb": round(row["MemoryGB"], 1),
                        "manufacturer": row["Manufacturer"],
                        "price_per_hour": f"${row['Price']:.3f}",
                        "family": row["InstanceType"].split(".")[0],
                        "generation": int(row["generation"]),
                        "cost_rank": len(instance_options) + 1  # Lower number = cheaper
                    }
                )

            # Check cache first
            cache_key = get_cache_key(vm)
            cached_rec = get_cached_recommendation(cache_key)
            if cached_rec:
                recommendations.append({
                    "vm_name": vm_name,
                    "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                    "recommendation": {**cached_rec, "method": "ai_cached"},
                    "metadata": vm,
                })
                continue

            # Extract comprehensive VM metadata with enhanced server statistics
            vm_ratio = memory_gb / cpus if cpus > 0 else 4

            # Priority: Extract server statistics/analysis column - ENHANCED EXTRACTION
            server_stats = (
                vm.get("Server Statistics") or      # PRIMARY - exact Excel column name
                vm.get("server_statistics") or 
                vm.get("server_stats") or 
                vm.get("Server Stats") or 
                vm.get("statistics") or 
                vm.get("workload_info") or 
                vm.get("performance_data") or 
                vm.get("usage_patterns") or 
                ""
            )
            
            # Extract additional relevant fields that help with AI analysis
            additional_context = []
            
            # Extract budget/cost constraints
            budget_info = vm.get("budget") or vm.get("Budget") or vm.get("cost") or vm.get("Cost") or ""
            if budget_info and str(budget_info).strip():
                additional_context.append(f"BUDGET CONSTRAINT: {budget_info}")
            
            # Extract environment/criticality info
            env_info = vm.get("environment") or vm.get("Environment") or vm.get("criticality") or vm.get("Criticality") or ""
            if env_info and str(env_info).strip():
                additional_context.append(f"ENVIRONMENT/CRITICALITY: {env_info}")
            
            # Extract compliance requirements
            compliance_fields = ["compliance", "Compliance", "security", "Security", "requirements", "Requirements"]
            for field in compliance_fields:
                if field in vm and vm[field] and str(vm[field]).strip():
                    additional_context.append(f"COMPLIANCE/SECURITY: {vm[field]}")
                    break

            # Extract ALL additional metadata flexibly
            core_fields = {"VM", "cpu", "memory", "manufacturer", "instance type", "instance_type", 
                          "server_statistics", "server_stats", "Server Statistics", "Server Stats"}
            additional_metadata = {k: v for k, v in vm.items() if k not in core_fields}

            # Build enhanced metadata with server statistics priority
            metadata_sections = []
            
            # SERVER STATISTICS - HIGHEST PRIORITY (Most important for AI analysis)
            if server_stats and str(server_stats).strip():
                metadata_sections.append(f"🔍 DETAILED SERVER STATISTICS & WORKLOAD ANALYSIS:\n{server_stats}")
            
            # Add extracted context
            if additional_context:
                metadata_sections.extend(additional_context)
            
            # Add key operational metadata
            operational_fields = {
                "wave": "MIGRATION WAVE",
                "ProjectId": "PROJECT ID", 
                "Tags": "RESOURCE TAGS",
                "SourceIpAddress": "SOURCE IP",
                "SSMKey": "SSM KEY",
                "Testing Subnet": "TESTING SUBNET",
                "Testing Security Groups": "TESTING SECURITY GROUPS",
                "Prod Subnet": "PRODUCTION SUBNET", 
                "Prod Security Groups": "PRODUCTION SECURITY GROUPS",
                "Public Ip": "PUBLIC IP REQUIRED",
                "boot mode": "BOOT MODE"
            }
            
            for field, label in operational_fields.items():
                if field in vm and vm[field] and str(vm[field]).strip():
                    metadata_sections.append(f"📋 {label}: {vm[field]}")

            metadata_info = "\n\n".join(metadata_sections) if metadata_sections else "No additional server statistics or metadata provided"

            prompt = f"""ENHANCED VM ANALYSIS FOR AWS EC2 MIGRATION:

BASIC VM SPECS:
- Name: {vm_name}
- CPU: {cpus} cores
- Memory: {memory_gb} GB
- CPU:Memory Ratio: {vm_ratio:.1f}:1
- Manufacturer Preference: {vm_manufacturer}

SERVER STATISTICS & BUSINESS CONTEXT:
{metadata_info}

AVAILABLE EC2 OPTIONS (sorted by generation/cost):
{json.dumps(instance_options[:10], indent=2)}

ANALYSIS REQUIREMENTS:
1. ANALYZE server statistics for workload patterns, performance requirements, scaling needs
2. CONSIDER business context, compliance, SLA requirements from metadata
3. FACTOR IN storage IOPS, network bandwidth, seasonal patterns if mentioned
4. EVALUATE cost vs performance trade-offs based on business criticality
5. RECOMMEND cheapest instance from newest generation that meets ALL requirements
6. NEVER recommend T-instances (burstable) for production
7. PROVIDE alternatives for different scenarios (cost-optimized, performance-optimized)

RESPOND WITH VALID JSON ONLY:
{{
    "primary_instance": "instance-type",
    "manufacturer": "selected-manufacturer",
    "vcpus": number,
    "memory_gb": number,
    "price": "$X.XXX",
    "generation": "Xth",
    "reasoning": "detailed analysis based on server statistics and business context",
    "workload_analysis": "analysis of server statistics and usage patterns",
    "business_context_analysis": "how business requirements influenced the decision",
    "cost_optimization": "cost analysis and savings explanation",
    "alternatives": [
        {{
            "instance_type": "alt-type",
            "manufacturer": "alt-manufacturer",
            "price": "$X.XXX",
            "use_case": "when to use this alternative"
        }}
    ]
}}"""

            try:
                # Make AI call with retry and timeout
                response_text = ai_call_with_retry(sizing_agent, prompt)
                
                # Clean response - remove any markdown formatting
                clean_response = response_text.strip()
                if clean_response.startswith("```json"):
                    clean_response = clean_response[7:]
                if clean_response.endswith("```"):
                    clean_response = clean_response[:-3]

                ai_recommendation = json.loads(clean_response.strip())
                
                # Cache successful recommendation
                cache_recommendation(cache_key, ai_recommendation)

                # Ensure alternatives is properly formatted
                if "alternatives" not in ai_recommendation:
                    ai_recommendation["alternatives"] = []
                
                recommendations.append(
                    {
                        "vm_name": vm_name,
                        "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                        "recommendation": {**ai_recommendation, "method": "ai_enhanced_analysis"},
                        "metadata": vm,
                    }
                )

            except Exception as ai_error:
                print(f"AI analysis failed for {vm_name}: {ai_error}")
                # Fallback to simple best match with proper alternatives
                if not suitable_instances.empty:
                    fallback = suitable_instances.iloc[0]
                    
                    # Get 2 alternatives
                    alternatives = []
                    for i in range(1, min(3, len(suitable_instances))):
                        alt = suitable_instances.iloc[i]
                        alternatives.append({
                            "instance_type": alt["InstanceType"],
                            "manufacturer": alt["Manufacturer"],
                            "vcpus": int(alt["VCpus"]),
                            "memory_gb": round(alt["MemoryGB"], 1),
                            "price": f"${alt['Price']:.3f}",
                            "generation": f"{int(alt['generation'])}th",
                            "price_difference": f"+${alt['Price'] - fallback['Price']:.3f}/hr",
                            "use_case": "Alternative option if primary unavailable"
                        })
                    
                    recommendations.append(
                        {
                            "vm_name": vm_name,
                            "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                            "recommendation": {
                                "primary_instance": fallback["InstanceType"],
                                "manufacturer": fallback["Manufacturer"],
                                "vcpus": int(fallback["VCpus"]),
                                "memory_gb": round(fallback["MemoryGB"], 1),
                                "price": f"${fallback['Price']:.3f}",
                                "generation": f"{int(fallback['generation'])}th",
                                "reasoning": f"AI analysis failed, using cheapest {int(fallback['generation'])}th gen fallback: {fallback['InstanceType']}",
                                "alternatives": alternatives,
                                "method": "ai_fallback",
                                "ai_error": str(ai_error),
                            },
                            "metadata": vm,
                        }
                    )

        return {
            "status": "success",
            "recommendations": recommendations,
            "total_vms": len(recommendations),
            "method": "ai_intelligent_analysis",
            "model_used": "us.amazon.nova-micro-v1:0",
            "cache_hits": len([r for r in recommendations if r["recommendation"].get("method") == "ai_cached"]),
            "ai_calls": len([r for r in recommendations if r["recommendation"].get("method") == "ai_enhanced_analysis"]),
        }

    except Exception as e:
        return {"status": "error", "error": str(e), "method": "ai_intelligent_analysis"}


@tool
def generate_ec2_recommendations(vm_data: List[Dict], use_ai: bool = True, manufacturer: str = "Intel") -> dict:
    """
    Generate EC2 recommendations - AI version always uses AI analysis.

    Args:
        vm_data: List of VM specifications
        use_ai: Always True for AI agent (parameter kept for compatibility)
        manufacturer: Preferred manufacturer

    Returns:
        AI-powered EC2 recommendations
    """
    # AI agent always uses AI analysis
    return generate_ec2_recommendations_ai(vm_data, manufacturer)
