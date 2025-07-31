import pandas as pd
from datetime import datetime

def calculate_advanced_kpis(df):
    if df.empty or 'Cluster' not in df.columns:
        return {}

    kpis = {}

    # Root Cause Density Index (RCDI): Average complaints per cluster
    total_complaints = len(df)
    num_clusters = df['Cluster'].nunique()
    kpis['Root Cause Density Index'] = round(total_complaints / (num_clusters or 1), 2)

    # Repeating Complaint Ratio (RCR): Duplicate text count vs total
    duplicate_count = df.duplicated(subset=['Summary']).sum()
    kpis['Repeating Complaint Ratio (%)'] = round((duplicate_count / total_complaints) * 100, 2)

    # Mean Time to Root Cause (MTTRC): Average days from earliest to latest complaint per cluster
    df['FailureDate'] = pd.to_datetime(df['FailureDate'], errors='coerce')
    cluster_mttr = df.groupby('Cluster')['FailureDate'].agg(['min', 'max'])
    cluster_mttr['Delta'] = (cluster_mttr['max'] - cluster_mttr['min']).dt.days
    kpis['Mean Time to Root Cause (days)'] = round(cluster_mttr['Delta'].mean(), 2)

    # Geo-Failure Spread Index (GFSI): Number of unique states per cluster
    geo_spread = df.groupby('Cluster')['State'].nunique().mean()
    kpis['Geo-Failure Spread Index'] = round(geo_spread, 2)

    # VIN Concentration Score (VCS): Number of unique VINs per cluster (low = systemic issues)
    vin_score = df.groupby('Cluster')['VehicleIdentificationNumber'].nunique().mean()
    kpis['VIN Concentration Score'] = round(vin_score, 2)

    return kpis
