import streamlit as st
import pandas as pd
import plotly.express as px
import io
from data.data_fetcher import fetch_complaints
from nlp.clustering import label_complaint_clusters
from utils.kpi_generator import calculate_advanced_kpis
from kpi.advanced_kpis import (
    failure_trend_velocity,
    recurrence_density,
    geo_risk_scoring,
    severity_weighted_impact,
)

def explain_cluster(summary_texts):
    summaries = summary_texts.split(" | ")
    explanation = "Common complaints include: " + ", ".join(summaries[:3])
    return explanation

def convert_fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    return buf.getvalue()

st.set_page_config(page_title="AutoRootCauseX", layout="wide")

st.title("🚘 AutoRootCauseX: GenAI Root Cause Analyzer for Vehicle Complaints")
st.markdown(
    """
    Analyze live **NHTSA vehicle complaints** to uncover root causes using state-of-the-art clustering and KPIs.
    Explore complaint trends, geographic risk, and detailed cluster explanations.
    """
)

# Sidebar Inputs
st.sidebar.header("🔍 Search Complaints")
make = st.sidebar.text_input("Vehicle Make (e.g., Ford)", "Ford")
model = st.sidebar.text_input("Vehicle Model (e.g., Escape)", "Escape")
year = st.sidebar.selectbox("Year", list(range(2015, 2025))[::-1])
limit = st.sidebar.slider("Number of complaints to fetch", min_value=20, max_value=200, value=100, step=10)

@st.cache_data(show_spinner=True)
def get_data(make, model, year, limit):
    return fetch_complaints(make, model, year, limit=limit)

@st.cache_data(show_spinner=True)
def get_clustered_data(df):
    return label_complaint_clusters(df)

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data and running analysis..."):
        raw_df = get_data(make, model, year, limit)
        if raw_df.empty:
            st.warning("No complaints found for the selected vehicle. Try a different query.")
        else:
            clustered_df, cluster_summary = get_clustered_data(raw_df)
            kpis = calculate_advanced_kpis(clustered_df)

            # Layout: KPIs + Charts
            st.subheader("📊 Key Performance Indicators (KPIs)")
            cols = st.columns(len(kpis))
            for idx, (key, value) in enumerate(kpis.items()):
                formatted_val = f"{value:.2f}" if isinstance(value, float) else str(value)
                cols[idx].metric(label=key, value=formatted_val)

            # KPIs Overview Bar Chart
            kpi_names = list(kpis.keys())
            kpi_values = list(kpis.values())
            fig_kpi = px.bar(
                x=kpi_names, y=kpi_values,
                labels={"x": "KPI", "y": "Value"},
                title="KPIs Overview",
                text_auto='.2s',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_kpi, use_container_width=True)
            st.download_button("⬇️ Download KPI Chart as PNG", convert_fig_to_bytes(fig_kpi), "kpi_chart.png", "image/png")

            # Complaint Trends Over Time
            clustered_df['FailureDate'] = pd.to_datetime(clustered_df['FailureDate'], errors='coerce')
            clustered_df['YearMonth'] = clustered_df['FailureDate'].dt.to_period('M').astype(str)
            time_series_df = clustered_df.groupby(['YearMonth', 'Cluster']).size().reset_index(name='ComplaintCount')

            st.subheader("📅 Complaint Trends Over Time by Cluster")
            fig_time_series = px.line(
                time_series_df,
                x='YearMonth',
                y='ComplaintCount',
                color='Cluster',
                markers=True,
                labels={'YearMonth': 'Year-Month', 'ComplaintCount': 'Number of Complaints', 'Cluster': 'Cluster ID'},
                title='Monthly Complaint Counts per Cluster',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_time_series.update_xaxes(tickangle=45, nticks=20)
            st.plotly_chart(fig_time_series, use_container_width=True)
            st.download_button("⬇️ Download Time Series Chart as PNG", convert_fig_to_bytes(fig_time_series), "time_series.png", "image/png")

            # Cluster Summary with explanations
            st.subheader("🧠 Cluster Summary & Explanations")
            for _, row in cluster_summary.iterrows():
                with st.expander(f"Cluster {row['Cluster']} — {row['NumComplaints']} complaints"):
                    st.markdown(f"**Example complaint summaries:** {row['Summary']}")
                    explanation = explain_cluster(row['Summary'])
                    st.info(explanation)

            # Geo Heatmap
            st.subheader("🗺️ Geo Heatmap: Complaint Density by State & Cluster")
            geo_df = clustered_df.groupby(['Cluster', 'State']).size().reset_index(name='Count')
            fig_geo = px.choropleth(
                geo_df,
                locations='State',
                locationmode="USA-states",
                color='Count',
                scope="usa",
                animation_frame='Cluster',
                color_continuous_scale="OrRd",
                title="Geographic Distribution of Complaints by Cluster"
            )
            st.plotly_chart(fig_geo, use_container_width=True)
            st.download_button("⬇️ Download Geo Heatmap as PNG", convert_fig_to_bytes(fig_geo), "geo_heatmap.png", "image/png")

            # UMAP Clustering Plot
            st.subheader("🧬 Complaint Clusters Visualization (UMAP Projection)")
            fig_umap = px.scatter(
                clustered_df,
                x="UMAP1",
                y="UMAP2",
                color=clustered_df['Cluster'].astype(str),
                hover_data=["Summary", "State"],
                title="UMAP Projection of Complaint Clusters",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_umap, use_container_width=True)
            st.download_button("⬇️ Download UMAP Plot as PNG", convert_fig_to_bytes(fig_umap), "umap_plot.png", "image/png")

            # Raw data tables in tabs
            st.subheader("📄 Data Explorer")
            tabs = st.tabs(["Cluster Summary", "All Complaints with Clusters"])
            with tabs[0]:
                st.dataframe(cluster_summary)
                csv_cluster = cluster_summary.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download Cluster Summary CSV", csv_cluster, "cluster_summary.csv", "text/csv")
            with tabs[1]:
                st.dataframe(clustered_df[['ODINumber', 'Summary', 'FailureDate', 'State', 'Cluster']])
                csv_full = clustered_df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download Full Complaint Data CSV", csv_full, "complaints.csv", "text/csv")

            st.markdown("---")
            st.caption("© 2025 AutoRootCauseX — Powered by live NHTSA data, NLP, and clustering analytics.")
