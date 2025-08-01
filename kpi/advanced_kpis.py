import pandas as pd
from sklearn.linear_model import LinearRegression

def failure_trend_velocity(df, date_col='FailureDate', cluster_col='Cluster'):
    df[date_col] = pd.to_datetime(df[date_col])
    df['YearMonth'] = df[date_col].dt.to_period('M')
    trend_results = {}
    
    for cluster in df[cluster_col].unique():
        cluster_df = df[df[cluster_col] == cluster]
        counts = cluster_df.groupby('YearMonth').size().reset_index(name='count')
        
        counts['MonthOrdinal'] = counts['YearMonth'].apply(lambda x: x.ordinal)
        X = counts['MonthOrdinal'].values.reshape(-1,1)
        y = counts['count'].values
        
        if len(X) < 2:
            trend_results[cluster] = 0
            continue
        
        model = LinearRegression().fit(X, y)
        slope = model.coef_[0]
        trend_results[cluster] = slope
    
    return trend_results

def recurrence_density(df, cluster_col='Cluster', vehicle_population=1000000):
    counts = df[cluster_col].value_counts().to_dict()
    density = {cluster: count / vehicle_population for cluster, count in counts.items()}
    return density

def geo_risk_scoring(df, cluster_col='Cluster', geo_col='State', vehicle_registration_by_state=None):
    if vehicle_registration_by_state is None:
        vehicle_registration_by_state = {}
    
    risk_scores = {}
    grouped = df.groupby([cluster_col, geo_col]).size()
    
    for (cluster, state), count in grouped.items():
        reg = vehicle_registration_by_state.get(state, 100000)  # fallback default
        risk_scores[(cluster, state)] = count / reg
    
    return risk_scores

def severity_weighted_impact(df, cluster_col='Cluster', severity_col='Severity'):
    if severity_col not in df.columns:
        df[severity_col] = 1
    
    weighted = df.groupby(cluster_col)[severity_col].sum().to_dict()
    return weighted
