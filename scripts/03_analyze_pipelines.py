#!/usr/bin/env python3
"""
Step 3 & 4: Analyze pipeline structure and calculate costs per analysis pipeline
- Group steps by pipeline (직무 + 업무세부내역)
- Calculate total costs, time, and resources per pipeline
- Generate detailed reports
"""

import pandas as pd
import numpy as np
import argparse
from pathlib import Path
import json

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"

def analyze_pipeline_structure(df):
    """Analyze the structure of each pipeline"""

    print("=" * 80)
    print("Step 3: Analyzing Pipeline Structure")
    print("=" * 80)

    # For Assembly, ignore pipeline name differences
    # For Microbiome, keep pipeline name to distinguish different methods
    # Create a custom grouping key
    def get_pipeline_key(row):
        job = row['직무(업무명)']
        task = row['업무세부내역']
        pipeline = row['Pipeline Name']

        # For Assembly, ignore pipeline name (combine all)
        if job == 'Assembly':
            return (job, task, 'combined')
        # For Microbiome, use pipeline name to distinguish
        else:
            return (job, task, pipeline)

    df['pipeline_key'] = df.apply(get_pipeline_key, axis=1)
    pipelines = df.groupby('pipeline_key')

    pipeline_summary = []

    for (job, task, pipeline_key), group in pipelines:
        # Count groups and steps
        n_groups = group['Group'].nunique()
        n_steps = len(group)

        # Get unique tools
        tools_list = group['tools'].dropna().unique().tolist()
        n_tools = len(tools_list)

        # Get pipeline names (may be multiple for combined Assembly pipelines)
        pipeline_names = group['Pipeline Name'].dropna().unique()
        if pipeline_key == 'combined':
            pipeline_name = ', '.join(pipeline_names) if len(pipeline_names) > 1 else pipeline_names[0]
        else:
            pipeline_name = pipeline_key

        # Get platforms and versions (may be multiple)
        platforms = group['Platfom'].dropna().unique()
        platform_str = ', '.join(sorted(set(platforms)))

        versions = group['Pipeline Version'].dropna().unique()
        version = versions[0] if len(versions) > 0 else 'N/A'

        # Resource summary
        total_cpu = group['CPUs'].sum()  # Sum of all CPUs used
        total_mem = group['MEM(G)'].sum()  # Sum of all memory used
        total_time = group['TIME(hr)'].sum()
        total_storage = group['SIZE(MB)'].sum() / 1024  # Convert to GB

        # Cost summary
        total_cost = group['total_cost_usd'].sum()
        compute_cost = group['compute_cost_usd'].sum()
        storage_cost = group['storage_cost_usd'].sum()

        # Group breakdown
        groups_info = group.groupby('Group').agg({
            'Step': 'count',
            'total_cost_usd': 'sum',
            'TIME(hr)': 'sum',
        }).to_dict('index')

        pipeline_summary.append({
            '직무(업무명)': job,
            '업무세부내역': task,
            'Platform': platform_str,
            'Pipeline Name': pipeline_name,
            'Pipeline Version': version,
            'n_groups': n_groups,
            'n_steps': n_steps,
            'n_tools': n_tools,
            'tools_list': ', '.join(tools_list[:10]) + ('...' if n_tools > 10 else ''),
            'total_cpu': total_cpu,
            'total_mem_gb': total_mem,
            'total_time_hr': total_time,
            'total_storage_gb': total_storage,
            'total_cost_usd': total_cost,
            'compute_cost_usd': compute_cost,
            'storage_cost_usd': storage_cost,
            'cost_per_hour': total_cost / total_time if total_time > 0 else 0,
            'groups_breakdown': groups_info,
        })

    pipeline_df = pd.DataFrame(pipeline_summary)

    print(f"\n1. Total Pipelines Analyzed: {len(pipeline_df)}")

    print("\n2. Pipeline Overview:")
    overview = pipeline_df[['직무(업무명)', '업무세부내역', 'Platform', 'n_groups', 'n_steps',
                             'total_time_hr', 'total_cost_usd']].copy()
    overview['total_cost_usd'] = overview['total_cost_usd'].round(2)
    overview['total_time_hr'] = overview['total_time_hr'].round(2)
    print(overview.to_string(index=False, max_colwidth=40))

    print("\n3. Resource Requirements by Pipeline:")
    resources = pipeline_df[['직무(업무명)', '업무세부내역', 'total_cpu', 'total_mem_gb',
                              'total_storage_gb']].copy()
    resources['total_storage_gb'] = resources['total_storage_gb'].round(2)
    print(resources.to_string(index=False, max_colwidth=40))

    return pipeline_df

def generate_detailed_reports(df, pipeline_df, team):
    """Generate detailed cost reports for each pipeline"""

    # Setup team-specific reports directory
    TEAM_REPORTS_DIR = REPORTS_DIR / f"team{team}"
    TEAM_REPORTS_DIR.mkdir(exist_ok=True)

    print("\n" + "=" * 80)
    print(f"Step 4: Generating Detailed Cost Reports for Team {team}")
    print("=" * 80)

    # Group by pipeline
    for idx, pipeline in pipeline_df.iterrows():
        job = pipeline['직무(업무명)']
        task = pipeline['업무세부내역']

        # Filter data for this pipeline
        pipeline_data = df[
            (df['직무(업무명)'] == job) &
            (df['업무세부내역'] == task)
        ].copy()

        # Generate report filename
        filename = f"{job}_{task}".replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
        filename = filename.replace('/', '_')[:100]  # Limit length
        report_file = TEAM_REPORTS_DIR / f"{filename}_report.txt"

        # Create report
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"PIPELINE COST ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"직무 (Job): {job}\n")
            f.write(f"업무세부내역 (Task Detail): {task}\n")
            f.write(f"Platform: {pipeline['Platform']}\n")
            f.write(f"Pipeline: {pipeline['Pipeline Name']} v{pipeline['Pipeline Version']}\n")
            f.write(f"\n")

            # Overview
            f.write("-" * 80 + "\n")
            f.write("OVERVIEW\n")
            f.write("-" * 80 + "\n")
            f.write(f"Number of Groups: {pipeline['n_groups']}\n")
            f.write(f"Number of Steps: {pipeline['n_steps']}\n")
            f.write(f"Number of Tools: {pipeline['n_tools']}\n")
            f.write(f"\n")

            # Resource summary
            f.write("-" * 80 + "\n")
            f.write("RESOURCE REQUIREMENTS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total CPUs: {pipeline['total_cpu']:.0f}\n")
            f.write(f"Total Memory: {pipeline['total_mem_gb']:.0f} GB\n")
            f.write(f"Total Compute Time: {pipeline['total_time_hr']:.2f} hours\n")
            f.write(f"Total Storage: {pipeline['total_storage_gb']:.2f} GB\n")
            f.write(f"\n")

            # Cost summary
            f.write("-" * 80 + "\n")
            f.write("COST SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Cost: ${pipeline['total_cost_usd']:.2f}\n")
            f.write(f"  - Compute Cost: ${pipeline['compute_cost_usd']:.2f} ({pipeline['compute_cost_usd']/pipeline['total_cost_usd']*100:.1f}%)\n")
            f.write(f"  - Storage Cost: ${pipeline['storage_cost_usd']:.2f} ({pipeline['storage_cost_usd']/pipeline['total_cost_usd']*100:.1f}%)\n")
            f.write(f"Cost per Hour: ${pipeline['cost_per_hour']:.2f}\n")
            f.write(f"\n")

            # Group breakdown
            f.write("-" * 80 + "\n")
            f.write("COST BREAKDOWN BY GROUP\n")
            f.write("-" * 80 + "\n")

            group_summary = pipeline_data.groupby('Group').agg({
                'Step': 'count',
                'tools': lambda x: ', '.join(x.unique()),
                'TIME(hr)': 'sum',
                'total_cost_usd': 'sum',
            }).reset_index()
            group_summary.columns = ['Group', 'Steps', 'Tools', 'Time (hr)', 'Cost (USD)']
            group_summary = group_summary.sort_values('Cost (USD)', ascending=False)

            for _, row in group_summary.iterrows():
                f.write(f"\n{row['Group']}:\n")
                f.write(f"  Steps: {row['Steps']}\n")
                f.write(f"  Time: {row['Time (hr)']:.2f} hours\n")
                f.write(f"  Cost: ${row['Cost (USD)']:.2f}\n")
                f.write(f"  Tools: {row['Tools']}\n")

            # Detailed step breakdown
            f.write("\n" + "-" * 80 + "\n")
            f.write("DETAILED STEP-BY-STEP BREAKDOWN\n")
            f.write("-" * 80 + "\n\n")

            for _, row in pipeline_data.iterrows():
                f.write(f"Group: {row['Group']}\n")
                f.write(f"Step: {row['Step']}\n")
                f.write(f"Tool: {row['tools']} v{row['version']}\n")
                f.write(f"Resources: {row['CPUs']:.0f} CPUs, {row['MEM(G)']:.0f} GB RAM, "
                       f"{row['SIZE(MB)']:.0f} MB storage\n")
                f.write(f"Runtime: {row['TIME(hr)']:.2f} hours × {row['nTask(병렬)']:.0f} parallel tasks\n")
                f.write(f"Instance: {row['instance_type']} @ ${row['instance_hourly_rate']:.4f}/hr\n")
                f.write(f"Cost: ${row['total_cost_usd']:.4f} "
                       f"(compute: ${row['compute_cost_usd']:.4f}, storage: ${row['storage_cost_usd']:.4f})\n")
                f.write(f"\n")

            f.write("=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")

        print(f"   ✓ Generated: {report_file.name}")

    # Generate summary report
    summary_file = TEAM_REPORTS_DIR / "00_SUMMARY_ALL_PIPELINES.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("BIOINFORMATICS PIPELINE COST SUMMARY\n")
        f.write(f"Team {team} Analysis - AWS Batch Cost Analysis\n")
        f.write("=" * 80 + "\n\n")

        f.write("OVERVIEW\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Pipelines: {len(pipeline_df)}\n")
        f.write(f"Total Groups: {pipeline_df['n_groups'].sum()}\n")
        f.write(f"Total Steps: {pipeline_df['n_steps'].sum()}\n")
        f.write(f"Total Cost: ${pipeline_df['total_cost_usd'].sum():.2f}\n")
        f.write(f"  - Compute Cost: ${pipeline_df['compute_cost_usd'].sum():.2f}\n")
        f.write(f"  - Storage Cost: ${pipeline_df['storage_cost_usd'].sum():.2f}\n")
        f.write(f"Total Compute Time: {pipeline_df['total_time_hr'].sum():.2f} hours\n")
        f.write(f"Total Storage: {pipeline_df['total_storage_gb'].sum():.2f} GB\n")
        f.write(f"Total CPUs: {int(pipeline_df['total_cpu'].sum())}\n")
        f.write(f"Total Memory: {int(pipeline_df['total_mem_gb'].sum())} GB\n")
        f.write(f"\n")

        f.write("COST BY JOB TYPE\n")
        f.write("-" * 80 + "\n")
        job_summary = pipeline_df.groupby('직무(업무명)').agg({
            'total_cost_usd': 'sum',
            'compute_cost_usd': 'sum',
            'storage_cost_usd': 'sum',
            'n_groups': 'sum',
            'n_steps': 'sum',
            'total_time_hr': 'sum',
            'total_storage_gb': 'sum',
        }).round(2)
        f.write(job_summary.to_string())
        f.write("\n\n")

        f.write("ALL PIPELINES RANKED BY COST\n")
        f.write("-" * 80 + "\n")
        f.write("Rank | Job | Task Detail | Cost (USD) | Time (hr) | Groups | Steps | Total CPU | Total Mem (GB) | Storage (GB)\n")
        f.write("-" * 80 + "\n")
        ranked = pipeline_df.sort_values('total_cost_usd', ascending=False)
        for idx, (_, row) in enumerate(ranked.iterrows(), 1):
            job = row['직무(업무명)'][:10]
            task = row['업무세부내역'][:25]
            cost = row['total_cost_usd']
            time_hr = row['total_time_hr']
            n_groups = int(row['n_groups'])
            n_steps = int(row['n_steps'])
            total_cpu = int(row['total_cpu'])
            total_mem = int(row['total_mem_gb'])
            storage = row['total_storage_gb']
            f.write(f"{idx:4} | {job:10} | {task:25} | ${cost:9.2f} | {time_hr:9.1f} | {n_groups:6} | {n_steps:5} | {total_cpu:9} | {total_mem:14} | {storage:11.1f}\n")
        f.write("\n")

        f.write("DETAILED PIPELINE INFORMATION\n")
        f.write("=" * 80 + "\n\n")

        for idx, row in ranked.iterrows():
            f.write(f"[{ranked.index.get_loc(idx) + 1}] {row['직무(업무명)']} - {row['업무세부내역']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Pipeline: {row['Pipeline Name']} v{row['Pipeline Version']}\n")
            f.write(f"Platform: {row['Platform']}\n")
            f.write(f"\n")
            f.write(f"Structure:\n")
            f.write(f"  Groups: {int(row['n_groups'])}\n")
            f.write(f"  Steps:  {int(row['n_steps'])}\n")
            f.write(f"  Tools:  {int(row['n_tools'])}\n")
            f.write(f"\n")
            f.write(f"Resources:\n")
            f.write(f"  Total CPU:      {int(row['total_cpu'])} cores\n")
            f.write(f"  Total Memory:   {int(row['total_mem_gb'])} GB\n")
            f.write(f"  Total Time:     {row['total_time_hr']:.1f} hours\n")
            f.write(f"  Total Storage:  {row['total_storage_gb']:.1f} GB\n")
            f.write(f"\n")
            f.write(f"Cost:\n")
            f.write(f"  Total:   ${row['total_cost_usd']:.2f}\n")
            f.write(f"  Compute: ${row['compute_cost_usd']:.2f} ({row['compute_cost_usd']/row['total_cost_usd']*100:.1f}%)\n")
            f.write(f"  Storage: ${row['storage_cost_usd']:.2f} ({row['storage_cost_usd']/row['total_cost_usd']*100:.1f}%)\n")
            f.write(f"  Per Hour: ${row['cost_per_hour']:.2f}/hr\n")
            f.write(f"\n")

            # Group breakdown
            if row['groups_breakdown']:
                f.write(f"Group Breakdown:\n")
                groups_sorted = sorted(row['groups_breakdown'].items(),
                                      key=lambda x: x[1]['total_cost_usd'],
                                      reverse=True)
                for group_name, group_info in groups_sorted:
                    f.write(f"  {group_name}:\n")
                    f.write(f"    Steps: {group_info['Step']}, ")
                    f.write(f"Time: {group_info['TIME(hr)']:.1f}h, ")
                    f.write(f"Cost: ${group_info['total_cost_usd']:.2f}\n")

            f.write("\n")

        f.write("=" * 80 + "\n")

    print(f"\n   ✓ Generated summary: {summary_file.name}")

    # Save pipeline summary as CSV
    pipeline_csv = TEAM_REPORTS_DIR / "pipeline_summary.csv"
    pipeline_df.drop('groups_breakdown', axis=1).to_csv(pipeline_csv, index=False, encoding='utf-8')
    print(f"   ✓ Saved pipeline summary: {pipeline_csv.name}")

    return pipeline_df

def main(team):
    # Setup file paths based on team number
    TEAM_DIR = DATA_DIR / f"team{team}"
    TEAM_REPORTS_DIR = REPORTS_DIR / f"team{team}"
    COSTED_FILE = TEAM_DIR / "analysis_with_costs.csv"

    print(f"Loading cost data from: {COSTED_FILE}\n")
    df = pd.read_csv(COSTED_FILE, encoding='utf-8')

    # Analyze pipeline structure
    pipeline_df = analyze_pipeline_structure(df)

    # Generate detailed reports
    generate_detailed_reports(df, pipeline_df, team)

    print("\n" + "=" * 80)
    print("Analysis Complete!")
    print("=" * 80)
    print(f"\nReports saved to: {TEAM_REPORTS_DIR}")
    print("\nKey files:")
    print("  - 00_SUMMARY_ALL_PIPELINES.txt: Overall summary")
    print("  - pipeline_summary.csv: Pipeline data in CSV format")
    print("  - *_report.txt: Detailed reports for each pipeline")

    return df, pipeline_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze pipelines and generate reports for a team')
    parser.add_argument('team', type=int, help='Team number (1, 2, or 3)')
    args = parser.parse_args()

    df, pipeline_df = main(args.team)
