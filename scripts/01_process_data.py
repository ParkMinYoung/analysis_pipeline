#!/usr/bin/env python3
"""
Step 1: Process raw CSV data from Google Sheets
- Unmerge cells by forward-filling empty values
- Clean numeric fields (remove commas, handle missing values)
- Save processed data
"""

import pandas as pd
import numpy as np
import argparse
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

def clean_numeric_field(value):
    """Remove commas and convert to numeric"""
    if pd.isna(value) or value == '' or value == '-':
        return np.nan
    if isinstance(value, str):
        # Remove commas and quotes
        value = value.replace(',', '').replace('"', '').strip()
        if value == '' or value == '-':
            return np.nan
        try:
            return float(value)
        except ValueError:
            return np.nan
    return float(value)

def main(team):
    # Setup file paths based on team number
    TEAM_DIR = DATA_DIR / f"team{team}"
    RAW_FILE = TEAM_DIR / "analysis_raw.csv"
    PROCESSED_FILE = TEAM_DIR / "analysis_processed.csv"

    print("=" * 80)
    print(f"Step 1: Processing Team {team} Analysis Sheet Data")
    print("=" * 80)

    # Read raw CSV
    print(f"\n1. Reading raw data from: {RAW_FILE}")
    df = pd.read_csv(RAW_FILE, encoding='utf-8')
    print(f"   - Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"   - Columns: {', '.join(df.columns.tolist())}")

    # Forward fill merged cells for key columns
    print("\n2. Unmerging cells (forward fill)...")
    columns_to_fill = ['직무(업무명)', '업무세부내역', 'Platfom', 'Pipeline Name', 'Pipeline Version', 'Group']

    for col in columns_to_fill:
        if col in df.columns:
            # Count empty cells before
            empty_before = df[col].isna().sum() + (df[col] == '').sum()

            # Forward fill
            df[col] = df[col].replace('', np.nan)
            df[col] = df[col].fillna(method='ffill')

            # Count empty cells after
            empty_after = df[col].isna().sum()
            print(f"   - {col}: {empty_before} empty cells → {empty_after} empty cells")

    # Clean numeric columns
    print("\n3. Cleaning numeric fields...")
    numeric_columns = ['CPUs', 'MEM(G)', 'TIME(hr)', 'nTask(병렬)', 'SIZE(MB)']

    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric_field)
            print(f"   - {col}: converted to numeric")

    # Display summary statistics
    print("\n4. Data Summary:")
    print(f"   - Total rows: {len(df)}")
    print(f"   - Jobs (직무): {df['직무(업무명)'].nunique()} unique")
    print(f"   - Task Details (업무세부내역): {df['업무세부내역'].nunique()} unique")
    print(f"   - Groups: {df['Group'].nunique()} unique")
    print(f"   - Steps: {df['Step'].nunique()} unique")
    print(f"   - Tools: {df['tools'].nunique()} unique")

    # Show breakdown by job
    print("\n5. Breakdown by Job (직무):")
    job_counts = df.groupby('직무(업무명)').size()
    for job, count in job_counts.items():
        print(f"   - {job}: {count} steps")

    # Show breakdown by task detail
    print("\n6. Breakdown by Task Detail (업무세부내역):")
    task_counts = df.groupby(['직무(업무명)', '업무세부내역']).size()
    for (job, task), count in task_counts.items():
        print(f"   - {job} / {task}: {count} steps")

    # Save processed data
    print(f"\n7. Saving processed data to: {PROCESSED_FILE}")
    df.to_csv(PROCESSED_FILE, index=False, encoding='utf-8')
    print("   ✓ Data saved successfully")

    # Display sample of processed data
    print("\n8. Sample of processed data (first 5 rows):")
    print(df.head().to_string(max_cols=10))

    print("\n" + "=" * 80)
    print("Step 1 Complete: Data processed and saved")
    print("=" * 80)

    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process raw analysis data for a team')
    parser.add_argument('team', type=int, help='Team number (1, 2, or 3)')
    args = parser.parse_args()

    df = main(args.team)
