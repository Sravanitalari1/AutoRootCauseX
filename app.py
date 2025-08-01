import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Custom modules
from data.data_fetcher import fetch_complaints
from nlp.clustering import label_complaint_clusters
from utils.kpi_generator import calculate_advanced_kpis
from kpi.advanced_kpis import (
    failure_trend_velocity,
    recurrence_density,
    geo_risk_scoring,
    severity_weighted_impact,
)

# Explanation generator (simple LLM-style)
def explain_cluster(summary_texts):
    summaries = summary_texts.split(" | ")
    explanation = "Common complaints include: " + ", ".join(summaries[:3])
    return explanation

# Utility: Convert Plotly figure to PNG bytes
def convert_fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    return buf.getvalue()

# Page config
st.set_page_config(page_title="AutoRootCauseX", layout="wide")

# App title & intro
st.title("🚘 AutoRootCauseX: GenAI Root Cause Analyzer for Vehicle Complaints")
st.markdown("""
Analyze live **NHTSA vehicle complaints** to uncover root causes using advanced clustering, KPIs, and visual analytics.
""")

# Sidebar inputs
st.sidebar.header("🔍 Vehicle Selection")
make = st.sidebar.text_input("Make", "Ford")
model = st.sidebar.text_input("Model", "Escape")
year = st.sidebar.selectbox("Year", list(range(2015, 2025))[::-1])

if st.sidebar.button("Analyze"):
    with st.spinner("Fetching and analyzing complaints..."):
        raw_df = fetch_complaints(make, model, year)

        if raw_df.empty:
            st.warning("No complaints found. Try a different vehicle.")
        else:
            # NLP clustering
            clustered_df, cluster_summary = label_complaint_clusters(raw_df)

            # KPI Calculation
            kpis = calculate_advanced_kpis(clustered_df)

            # KPI Display
            st.subheader("📊 Key Performance Indicators (KPIs)")
            cols = st.columns(len(kpis))
            for idx, (k, v) in enumerate(kpis.items()):
                val = f"{v:.2f}" if isinstance(v, float) else str(v)
                cols[idx].metric(label=k, value=val)

            # KPI Bar Chart
            kpi_fig = px.bar(
                x=list(kpis.keys()),
                y=list(kpis.values()),
                labels={"x": "KPI", "y": "Value"},
                title="KPIs Overview",
                text_auto=".2s",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(kpi_fig, use_container_width=True)
            st.download_button("⬇️ Download KPI Chart", convert_fig_to_bytes(kpi_fig), "kpi_chart.png", "image/png")

            # 📅 Complaint Trends (Time Series by Cluster)
            clustered_df['FailureDate'] = pd.to_datetime(clustered_df['FailureDate'], errors='coerce')
            clustered_df['YearMonth'] = clustered_df['FailureDate'].dt.to_period('M').astype(str)
            ts_df = clustered_df.groupby(['YearMonth', 'Cluster']).size().reset_index(name='Count')

            st.subheader("📅 Complaint Trends Over Time by Cluster")
            ts_fig = px.line(
                ts_df, x='YearMonth', y='Count', color='Cluster',
                markers=True,
                labels={'YearMonth': 'Month', 'Count': 'Complaints'},
                title='Monthly Complaint Trends per Cluster',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            ts_fig.update_xaxes(tickangle=45, nticks=20)
            st.plotly_chart(ts_fig, use_container_width=True)
            st.download_button("⬇️ Download Time Series Chart", convert_fig_to_bytes(ts_fig), "time_series.png", "image/png")

            # 🧠 Cluster Summary with NLP-style explanations
            st.subheader("🧠 Cluster Summary & LLM-Style Insights")
            for _, row in cluster_summary.iterrows():
                with st.expander(f"Cluster {row['Cluster']} — {row['NumComplaints']} complaints"):
                    st.markdown(f"**Example complaints:** {row['Summary']}")
                    explanation = explain_cluster(row['Summary'])
                    st.info(explanation)

            # 🗺️ Geo Heatmap
            st.subheader("🗺️ Complaint Density by State & Cluster")
            geo_df = clustered_df.groupby(['Cluster', 'State']).size().reset_index(name='Count')
            geo_fig = px.choropleth(
                geo_df,
                locations='State',
                locationmode="USA-states",
                color='Count',
                animation_frame='Cluster',
                scope="usa",
                title="Complaint Density Across U.S. States by Cluster",
                color_continuous_scale="OrRd"
            )
            st.plotly_chart(geo_fig, use_container_width=True)
            st.download_button("⬇️ Download Geo Heatmap", convert_fig_to_bytes(geo_fig), "geo_heatmap.png", "image/png")

            # 🧬 UMAP Projection
            st.subheader("🧬 Complaint Clusters: UMAP Projection")
            umap_fig = px.scatter(
                clustered_df, x="UMAP1", y="UMAP2",
                color=clustered_df['Cluster'].astype(str),
                hover_data=["Summary", "State"],
                title="UMAP Cluster Visualization",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(umap_fig, use_container_width=True)
            st.download_button("⬇️ Download UMAP Chart", convert_fig_to_bytes(umap_fig), "umap_plot.png", "image/png")

            # 📄 Raw Data Explorer
            st.subheader("📄 Data Explorer")
            tab1, tab2 = st.tabs(["Cluster Summary", "Full Complaint Data"])

            with tab1:
                st.dataframe(cluster_summary)
                csv_cluster = cluster_summary.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download Cluster Summary", csv_cluster, "cluster_summary.csv", "text/csv")

            with tab2:
                st.dataframe(clustered_df[['ODINumber', 'Summary', 'FailureDate', 'State', 'Cluster']])
                csv_full = clustered_df.to_csv(index=False).encode('utf-8')
                st.download_button("⬇️ Download All Data", csv_full, "complaints.csv", "text/csv")

            # Footer
            st.markdown("---")
            st.caption("© 2025 AutoRootCauseX — Powered by live NHTSA data, NLP, and open-source analytics.")
