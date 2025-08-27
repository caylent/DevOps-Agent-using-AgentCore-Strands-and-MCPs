# AWS EC2 Instance Sizing Guide

## Overview
This guide provides the methodology used by the IaC Migration Polyglot for selecting optimal EC2 instances based on VM specifications and AWS best practices.

## AWS vCPU:Memory Ratios

### Standard Ratios and Instance Families

| Ratio (vCPU : Memory) | Memory per vCPU | Workload Type | Instance Families | Use Cases |
|----------------------|-----------------|---------------|-------------------|-----------|
| **1:2** | 2 GB per vCPU | Compute Optimized | C5, C6i, C7i, C6g, C7g | CPU-intensive workloads, web servers, scientific computing |
| **1:4** | 4 GB per vCPU | General Purpose | M5, M6i, M7i, M6g, M7g, T3, T4g | Balanced workloads, web applications, microservices |
| **1:8** | 8 GB per vCPU | Memory Optimized | R5, R6i, R7i, R6g, R7g | In-memory databases, real-time analytics, caching |
| **1:16+** | 16+ GB per vCPU | High Memory | X1e, X2gd, u-6tb1, u-12tb1 | Large in-memory databases, big data processing |

## Instance Family Selection Logic

### 1. Compute Optimized (C Family)
- **Trigger**: VM ratio ≤ 2.5:1 (memory/cpu)
- **Best for**: CPU-bound applications
- **Families**: c7g (AWS Graviton), c7i (Intel), c6i (Intel), c5 (Intel)
- **Example**: 8 vCPU, 8GB → c7g.2xlarge

### 2. General Purpose (M Family)
- **Trigger**: VM ratio 2.5:1 to 6:1
- **Best for**: Balanced workloads
- **Families**: m7g (AWS Graviton), m7i (Intel), m6i (Intel), t4g (AWS Graviton), t3 (Intel)
- **Example**: 4 vCPU, 16GB → m7g.xlarge

### 3. Memory Optimized (R Family)
- **Trigger**: VM ratio 6:1 to 12:1
- **Best for**: Memory-intensive applications
- **Families**: r7g (AWS Graviton), r7i (Intel), r6i (Intel), r5 (Intel)
- **Example**: 2 vCPU, 16GB → r7g.large

### 4. High Memory (X Family)
- **Trigger**: VM ratio > 12:1
- **Best for**: Extremely memory-heavy workloads
- **Families**: x2gd (AWS Graviton), x1e (Intel), u-series (Intel)
- **Example**: 4 vCPU, 64GB → x2gd.xlarge

## Manufacturer Preferences

### AWS Graviton (ARM-based)
- **Advantages**: Up to 40% better price-performance, lower cost
- **Best for**: Most workloads, especially cost-sensitive deployments
- **Families**: c7g, m7g, r7g, t4g, x2gd

### Intel (x86-64)
- **Advantages**: Broad compatibility, mature ecosystem
- **Best for**: Legacy applications, specific software requirements
- **Families**: c7i, m7i, r7i, c6i, m6i, r6i

### AMD (x86-64)
- **Advantages**: Good price-performance for x86 workloads
- **Best for**: Cost-conscious x86 deployments
- **Families**: c7a, m7a, r7a, c6a, m6a, r6a

## Selection Algorithm

```python
def select_instance(cpu_req, memory_req, manufacturer='Intel'):
    # 1. Calculate VM ratio
    vm_ratio = memory_req / cpu_req

    # 2. Determine instance family
    if vm_ratio <= 2.5:
        family = 'Compute Optimized (C)'
        families = ['c7', 'c6', 'c5']
    elif vm_ratio <= 6:
        family = 'General Purpose (M/T)'
        families = ['m7', 'm6', 't4', 't3']
    elif vm_ratio <= 12:
        family = 'Memory Optimized (R)'
        families = ['r7', 'r6', 'r5']
    else:
        family = 'High Memory (X)'
        families = ['x2', 'x1', 'u-']

    # 3. Filter by manufacturer and find cheapest
    # 4. Return recommendation with alternatives
```

## Cost Optimization Tips

1. **AWS Graviton First**: Always consider Graviton instances for best price-performance
2. **Right-size**: Don't over-provision - use smallest instance that meets requirements
3. **Family Selection**: Choose the right family based on workload characteristics
4. **Spot Instances**: Consider for non-critical workloads (not covered in this tool)
5. **Reserved Instances**: For predictable workloads (pricing consideration)

## Example Recommendations

| VM Specs | Ratio | Family | Recommended Instance | Price | Reasoning |
|----------|-------|--------|---------------------|-------|-----------|
| 8 vCPU, 8GB | 1:1 | Compute | c7g.2xlarge (AWS) | $0.29 | CPU-intensive, Graviton cost advantage |
| 4 vCPU, 16GB | 4:1 | General | m7g.xlarge (AWS) | $0.16 | Balanced workload, cost-effective |
| 2 vCPU, 16GB | 8:1 | Memory | r7g.large (AWS) | $0.11 | Memory-optimized, best price |
| 4 vCPU, 64GB | 16:1 | High Memory | x2gd.xlarge (AWS) | $0.33 | High memory ratio, Graviton efficiency |

## Data Sources

- **Instance Data**: `Amazon EC2 Instance Comparison.csv`
- **Pricing**: AWS public pricing (hourly rates)
- **Ratios**: AWS Well-Architected Framework guidelines
- **Best Practices**: AWS Migration Best Practices

## Usage in IaC Migration Polyglot

This sizing logic is implemented in:
- `tools/ec2_sizing_tools.py` - Main sizing functions
- `find_best_instance()` - Core selection algorithm
- `generate_ec2_recommendations_traditional()` - Traditional method implementation

The tool automatically:
1. Analyzes VM specifications from Excel files
2. Calculates optimal vCPU:Memory ratios
3. Selects appropriate instance families
4. Filters by manufacturer preference
5. Returns cheapest options with alternatives
6. Stores recommendations in DynamoDB

## Future Enhancements

- **Workload-specific optimization** (database, web server, etc.)
- **Performance metrics integration** (CPU utilization, memory usage)
- **Reserved Instance pricing** consideration
- **Multi-region pricing** comparison
- **Spot Instance recommendations** for cost savings
