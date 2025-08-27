"""EC2 sizing tools for the agent"""

import json
import os
from typing import Dict, List

import pandas as pd

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


def find_best_instance(cpu_req: int, memory_req: int, manufacturer: str = "Intel") -> dict:
    """Find the best EC2 instance based on requirements, AWS ratios, and manufacturer preference"""
    df = load_ec2_instance_data()
    if df is None:
        return None

    # Calculate VM's vCPU:Memory ratio
    vm_ratio = memory_req / cpu_req if cpu_req > 0 else 4

    # Determine optimal instance family based on AWS ratios
    if vm_ratio <= 2.5:  # 1:2 ratio - Compute optimized
        family_preference = ["c7", "c6", "c5"]
        workload_type = "Compute Optimized"
    elif vm_ratio <= 6:  # 1:4 ratio - General purpose
        family_preference = ["m7", "m6", "m5"]
        workload_type = "General Purpose"
    elif vm_ratio <= 12:  # 1:8 ratio - Memory optimized
        family_preference = ["r7", "r6", "r5"]
        workload_type = "Memory Optimized"
    else:  # 1:16+ ratio - High memory
        family_preference = ["x2", "x1", "u-"]
        workload_type = "High Memory"

    # Filter by manufacturer
    if manufacturer.lower() == "aws":
        filtered_df = df[df["Manufacturer"] == "AWS"]
    elif manufacturer.lower() == "amd":
        filtered_df = df[df["Manufacturer"] == "AMD"]
    else:  # Intel default
        filtered_df = df[df["Manufacturer"] == "Intel"]

    # Find instances that meet requirements
    suitable_instances = filtered_df[(filtered_df["VCpus"] >= cpu_req) & (filtered_df["MemoryGB"] >= memory_req) & (filtered_df["Price"] > 0)]

    if suitable_instances.empty:
        # Fallback to any manufacturer
        suitable_instances = df[(df["VCpus"] >= cpu_req) & (df["MemoryGB"] >= memory_req) & (df["Price"] > 0)]

    if suitable_instances.empty:
        return None

    # Get primary recommendation from preferred manufacturer
    primary_instances = suitable_instances.sort_values("Price").head(1)

    if primary_instances.empty:
        return None

    primary = primary_instances.iloc[0]

    # Get 2 alternatives from different manufacturers
    alternatives = []

    # Alternative 1: Different manufacturer, same family preference
    other_manufacturers = ["Intel", "AMD", "AWS"]
    other_manufacturers = [m for m in other_manufacturers if m != manufacturer]

    for alt_manufacturer in other_manufacturers:
        if alt_manufacturer == "AWS":
            alt_filtered = df[df["Manufacturer"] == "AWS"]
        elif alt_manufacturer == "AMD":
            alt_filtered = df[df["Manufacturer"] == "AMD"]
        else:
            alt_filtered = df[df["Manufacturer"] == "Intel"]

        alt_suitable = alt_filtered[(alt_filtered["VCpus"] >= cpu_req) & (alt_filtered["MemoryGB"] >= memory_req) & (alt_filtered["Price"] > 0)]

        if not alt_suitable.empty:
            # Try to match family preference first
            alt_family_match = None
            for family in family_preference:
                family_match = alt_suitable[alt_suitable["InstanceType"].str.contains(family, case=False)]
                if not family_match.empty:
                    alt_family_match = family_match.sort_values("Price").iloc[0]
                    break

            # If no family match, get cheapest
            if alt_family_match is None:
                alt_family_match = alt_suitable.sort_values("Price").iloc[0]

            alternatives.append(
                {
                    "instance_type": alt_family_match["InstanceType"],
                    "manufacturer": alt_family_match["Manufacturer"],
                    "vcpus": int(alt_family_match["VCpus"]),
                    "memory_gb": round(alt_family_match["MemoryGB"], 1),
                    "price": f"${alt_family_match['Price']:.2f}",
                    "use_case": f"{alt_manufacturer} alternative",
                }
            )

            if len(alternatives) >= 2:
                break

    return {
        "primary": {
            "instance_type": primary["InstanceType"],
            "manufacturer": primary["Manufacturer"],
            "vcpus": int(primary["VCpus"]),
            "memory_gb": round(primary["MemoryGB"], 1),
            "price": f"${primary['Price']:.2f}",
        },
        "alternatives": alternatives[:2],  # Ensure exactly 2 alternatives
        "reasoning": f"VM ratio {vm_ratio:.1f}:1 → {workload_type} family. Primary: {primary['Manufacturer']} (cheapest). Alternatives from other manufacturers for flexibility.",
    }


@tool
def generate_ec2_recommendations_traditional(vm_data: List[Dict], manufacturer: str = "Intel") -> dict:
    """
    Generate EC2 instance recommendations using traditional ratio-based calculations.

    Args:
        vm_data: List of VM specifications

    Returns:
        Traditional EC2 recommendations
    """
    try:
        recommendations = []

        for vm in vm_data:
            vm_name = vm.get("VM", vm.get("name", "unknown"))
            cpus = vm.get("cpu", 1)
            memory_mb = vm.get("memory", 1024)
            memory_gb = memory_mb / 1024 if memory_mb > 100 else memory_mb

            # Check if instance type is pre-defined (has actual value, not empty)
            predefined_instance = vm.get("instance type", vm.get("instance_type", vm.get("InstanceType")))
            if (
                predefined_instance
                and str(predefined_instance).strip()
                and str(predefined_instance).strip().lower() not in ["", "nan", "none", "null"]
            ):
                predefined_instance = str(predefined_instance).strip()
            else:
                predefined_instance = None

            # Get manufacturer preference from VM data
            vm_manufacturer = vm.get("manufacturer", vm.get("Manufacturer", manufacturer))
            if vm_manufacturer and str(vm_manufacturer).strip():
                vm_manufacturer = str(vm_manufacturer).strip().title()
                # Map common values
                if vm_manufacturer.lower() in ["aws", "graviton"]:
                    vm_manufacturer = "AWS"
                elif vm_manufacturer.lower() == "amd":
                    vm_manufacturer = "AMD"
                elif vm_manufacturer.lower() == "intel":
                    vm_manufacturer = "Intel"
            else:
                vm_manufacturer = manufacturer

            # No need to extract individual fields - keep all metadata intact

            if predefined_instance:
                # Use predefined instance type - no calculation needed
                recommendations.append(
                    {
                        "vm_name": vm_name,
                        "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                        "recommendation": {
                            "primary_instance": predefined_instance,
                            "manufacturer": vm_manufacturer,
                            "reasoning": f"Pre-defined instance type from Excel data: {predefined_instance}",
                            "method": "predefined",
                            "alternatives": [],
                        },
                        "metadata": vm,  # Keep ALL original Excel data
                    }
                )
            else:
                # Calculate best instance using manufacturer preference
                best_instance = find_best_instance(cpus, memory_gb, vm_manufacturer)

                if best_instance:
                    recommendations.append(
                        {
                            "vm_name": vm_name,
                            "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                            "recommendation": {
                                "primary_instance": best_instance["primary"]["instance_type"],
                                "manufacturer": best_instance["primary"]["manufacturer"],
                                "vcpus": best_instance["primary"]["vcpus"],
                                "memory_gb": best_instance["primary"]["memory_gb"],
                                "price": best_instance["primary"]["price"],
                                "alternatives": best_instance["alternatives"],
                                "reasoning": f"{best_instance['reasoning']} (Preferred manufacturer: {vm_manufacturer})",
                                "method": "calculated_with_manufacturer",
                            },
                            "metadata": vm,  # Keep ALL original Excel data
                        }
                    )
                else:
                    # Fallback to basic logic if CSV lookup fails
                    recommendations.append(
                        {
                            "vm_name": vm_name,
                            "current_specs": {"cpu": cpus, "memory_gb": memory_gb},
                            "recommendation": {
                                "primary_instance": "m6i.large",
                                "reasoning": f"Fallback recommendation - CSV lookup failed for {vm_manufacturer} preference",
                                "alternatives": [],
                                "method": "fallback",
                            },
                            "metadata": vm,  # Keep ALL original Excel data
                        }
                    )

        return {
            "status": "success",
            "recommendations": recommendations,
            "total_vms": len(recommendations),
            "method": "traditional_csv_based",
            "manufacturer_preference": manufacturer,
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}





@tool
def generate_ec2_recommendations(vm_data: List[Dict], use_ai: bool = False, manufacturer: str = "Intel") -> dict:
    """
    Generate EC2 recommendations with AI or traditional method.

    Args:
        vm_data: List of VM specifications
        use_ai: Whether to use AI analysis or traditional calculation
        manufacturer: Preferred manufacturer (Intel, AMD, AWS)

    Returns:
        EC2 recommendations using specified method
    """
    if use_ai:
        try:
            # Import AI function from AI tools
            from tools.ec2_sizing_ai_tools import generate_ec2_recommendations_ai
            return generate_ec2_recommendations_ai(vm_data, manufacturer)
        except ImportError as e:
            print(f"AI tools not available, falling back to traditional: {e}")
            return generate_ec2_recommendations_traditional(vm_data, manufacturer)
    else:
        return generate_ec2_recommendations_traditional(vm_data, manufacturer)
