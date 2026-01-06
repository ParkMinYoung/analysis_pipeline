#!/usr/bin/env python3
"""
Step 2: Calculate AWS Batch costs for bioinformatics pipelines
- Apply AWS EC2 pricing for compute resources
- Consider CPU, memory, time, and parallel tasks
- Use us-east-1 pricing (most common region for genomics)
"""

import pandas as pd
import numpy as np
import argparse
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# AWS EC2 Pricing for us-east-1 (On-Demand, Linux, January 2026)
# Source: https://www.economize.cloud/resources/aws/pricing/ec2/
# Compute-optimized (C6i) - Best for CPU-intensive genomics workloads
EC2_PRICING = {
    # Instance Type: (vCPU, Memory GB, Hourly Rate USD)
    'c6i.large': (2, 4, 0.085),
    'c6i.xlarge': (4, 8, 0.17),
    'c6i.2xlarge': (8, 16, 0.34),
    'c6i.4xlarge': (16, 32, 0.68),
    'c6i.8xlarge': (32, 64, 1.36),
    'c6i.12xlarge': (48, 96, 2.04),
    'c6i.16xlarge': (64, 128, 2.72),
    'c6i.24xlarge': (96, 192, 4.08),

    # Memory-optimized (R6i) - For memory-intensive workloads
    'r6i.large': (2, 16, 0.126),
    'r6i.xlarge': (4, 32, 0.252),
    'r6i.2xlarge': (8, 64, 0.504),
    'r6i.4xlarge': (16, 128, 1.008),
    'r6i.8xlarge': (32, 256, 2.016),
    'r6i.12xlarge': (48, 384, 3.024),
    'r6i.16xlarge': (64, 512, 4.032),
}

# EBS Storage pricing (gp3 volumes, us-east-1)
# $0.08 per GB-month = $0.00011 per GB-hour
EBS_PRICE_PER_GB_HOUR = 0.08 / (30 * 24)

def select_instance_type(cpu, mem_gb):
    """
    Select the most cost-effective EC2 instance type based on CPU and memory requirements.

    Strategy:
    1. Find instances that meet both CPU and memory requirements
    2. Among those, choose the cheapest option
    3. Prefer compute-optimized (C6i) for CPU-heavy workloads
    4. Use memory-optimized (R6i) only when memory requirements demand it
    """
    # Handle edge cases
    if pd.isna(cpu) or pd.isna(mem_gb):
        return None, None, 0.0

    cpu = max(1, int(cpu))
    mem_gb = max(1, int(mem_gb))

    # Find suitable instances
    suitable_instances = []
    for instance_type, (inst_cpu, inst_mem, hourly_rate) in EC2_PRICING.items():
        if inst_cpu >= cpu and inst_mem >= mem_gb:
            # Calculate cost efficiency (lower is better)
            cost_per_cpu = hourly_rate / inst_cpu
            cost_per_mem = hourly_rate / inst_mem
            efficiency_score = (cost_per_cpu + cost_per_mem) / 2

            suitable_instances.append({
                'type': instance_type,
                'cpu': inst_cpu,
                'mem': inst_mem,
                'rate': hourly_rate,
                'efficiency': efficiency_score,
                'waste_cpu': inst_cpu - cpu,
                'waste_mem': inst_mem - mem_gb,
            })

    if not suitable_instances:
        # No suitable instance found - need larger than available
        print(f"⚠ Warning: No instance found for CPU={cpu}, MEM={mem_gb}GB. Using largest available.")
        # Use the largest instance available
        largest = max(EC2_PRICING.items(), key=lambda x: (x[1][0], x[1][1]))
        return largest[0], largest[1][0], largest[1][2]

    # Sort by efficiency (prefer less wasted resources and lower cost)
    suitable_instances.sort(key=lambda x: (x['efficiency'], x['waste_cpu'] + x['waste_mem']))
    best = suitable_instances[0]

    return best['type'], best['cpu'], best['rate']

def calculate_costs(df, team):
    """Calculate AWS costs for each pipeline step"""

    print("=" * 80)
    print(f"Step 2: Calculating AWS Batch Costs for Team {team}")
    print("=" * 80)

    print("\n1. AWS Pricing Model:")
    print("   - Region: us-east-1 (N. Virginia)")
    print("   - Instance families:")
    print("     * C6i (Compute-optimized): CPU-intensive workloads")
    print("     * R6i (Memory-optimized): Memory-intensive workloads")
    print(f"   - EBS Storage: ${EBS_PRICE_PER_GB_HOUR:.6f} per GB-hour")

    # Apply instance selection
    print("\n2. Selecting optimal EC2 instances for each step...")

    results = []
    for idx, row in df.iterrows():
        cpu = row['CPUs']
        mem_gb = row['MEM(G)']
        time_hr = row['TIME(hr)']
        n_task = row['nTask(병렬)']
        size_mb = row['SIZE(MB)']

        # Select instance type
        instance_type, instance_cpu, hourly_rate = select_instance_type(cpu, mem_gb)

        # Handle missing values
        if pd.isna(time_hr):
            time_hr = 0.0
        if pd.isna(n_task):
            n_task = 1
        if pd.isna(size_mb):
            size_mb = 0.0

        # Calculate compute cost
        # Cost = hourly_rate * time * n_parallel_tasks
        compute_cost = hourly_rate * time_hr * n_task if instance_type else 0.0

        # Calculate storage cost
        # Cost = GB * time * price_per_gb_hour
        storage_gb = size_mb / 1024
        storage_cost = storage_gb * time_hr * EBS_PRICE_PER_GB_HOUR if size_mb > 0 else 0.0

        # Total cost
        total_cost = compute_cost + storage_cost

        results.append({
            'instance_type': instance_type,
            'instance_vcpu': instance_cpu,
            'instance_hourly_rate': hourly_rate,
            'compute_cost_usd': compute_cost,
            'storage_cost_usd': storage_cost,
            'total_cost_usd': total_cost,
        })

    # Add cost columns to dataframe
    results_df = pd.DataFrame(results)
    df_with_costs = pd.concat([df, results_df], axis=1)

    # Summary statistics
    print(f"   - Total steps processed: {len(df)}")
    print(f"   - Steps with costs: {(df_with_costs['total_cost_usd'] > 0).sum()}")

    print("\n3. Cost Summary by Instance Type:")
    instance_summary = df_with_costs.groupby('instance_type').agg({
        'total_cost_usd': ['count', 'sum', 'mean'],
        'compute_cost_usd': 'sum',
        'storage_cost_usd': 'sum',
    }).round(4)
    print(instance_summary.to_string())

    print("\n4. Cost Summary by Job (직무):")
    job_summary = df_with_costs.groupby('직무(업무명)').agg({
        'total_cost_usd': ['sum', 'mean'],
        'compute_cost_usd': 'sum',
        'storage_cost_usd': 'sum',
    }).round(4)
    print(job_summary.to_string())

    print("\n5. Cost Summary by Task Detail (업무세부내역):")
    task_summary = df_with_costs.groupby(['직무(업무명)', '업무세부내역']).agg({
        'total_cost_usd': 'sum',
        'compute_cost_usd': 'sum',
        'storage_cost_usd': 'sum',
    }).round(4)
    print(task_summary.to_string())

    # Top 10 most expensive steps
    print("\n6. Top 10 Most Expensive Pipeline Steps:")
    top_10 = df_with_costs.nlargest(10, 'total_cost_usd')[
        ['직무(업무명)', '업무세부내역', 'Group', 'Step', 'tools',
         'CPUs', 'MEM(G)', 'TIME(hr)', 'nTask(병렬)',
         'instance_type', 'total_cost_usd']
    ]
    print(top_10.to_string(index=False, max_colwidth=30))

    return df_with_costs

def main(team):
    # Setup file paths based on team number
    TEAM_DIR = DATA_DIR / f"team{team}"
    PROCESSED_FILE = TEAM_DIR / "analysis_processed.csv"
    COSTED_FILE = TEAM_DIR / "analysis_with_costs.csv"

    # Load processed data
    print(f"Loading processed data from: {PROCESSED_FILE}\n")
    df = pd.read_csv(PROCESSED_FILE, encoding='utf-8')

    # Calculate costs
    df_with_costs = calculate_costs(df, team)

    # Save results
    print(f"\n7. Saving cost analysis to: {COSTED_FILE}")
    df_with_costs.to_csv(COSTED_FILE, index=False, encoding='utf-8')
    print("   ✓ Data saved successfully")

    print("\n" + "=" * 80)
    print("Step 2 Complete: AWS costs calculated")
    print("=" * 80)

    return df_with_costs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate AWS costs for a team')
    parser.add_argument('team', type=int, help='Team number (1, 2, or 3)')
    args = parser.parse_args()

    df_with_costs = main(args.team)
