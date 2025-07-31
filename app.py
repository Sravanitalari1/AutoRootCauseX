import streamlit as st
import pandas as pd
from data.data_fetcher import fetch_complaints
from nlp.clustering import label_complaint_clusters
from utils.kpi_generator import calculate_advanced_kpis

st.set_page_config(page_title="AutoRootCauseX", layout="wide")

st.title("🚘 AutoRootCauseX: GenAI Root Cause Analyzer for Vehicle Complaints")
st.markdown("Uncover deep patterns and KPIs from live **NHTSA complaints** using clustering + LLMs.")

# Sidebar: Input
st.sidebar.header("🔍 Search Complaints")
make = st.sidebar.text_input("Vehicle Make (e.g., Ford)", "Ford")
model = st.sidebar.text_input("Vehicle Model (e.g., Escape)", "Escape")
year = st.sidebar.selectbox("Year", list(range(2015, 2025))[::-1])

if st.sidebar.button("Analyze"):
    with st.spinner("🔄 Fetching data and running analysis..."):
        raw_df = fetch_complaints(make, model, year)
        if raw_df.empty:
            st.warning("No data found for this selection.")
        else:
            clustered_df, cluster_summary = label_complaint_clusters(raw_df)
            kpis = calculate_advanced_kpis(clustered_df)

            # Display KPIs
            st.subheader("📊 Root Cause KPIs")
            for key, value in kpis.items():
                st.metric(label=key, value=value)

            # Show Cluster Table
            st.subheader("🧠 Cluster Summary")
            st.dataframe(cluster_summary)

            # Show Raw Data with Cluster IDs
            st.subheader("📄 All Complaints with Cluster IDs")
            st.dataframe(clustered_df[['ODINumber', 'Summary', 'FailureDate', 'State', 'Cluster']])
