# AutoRootCauseX 🔍⚙️  
**AI-Powered Real-Time Root Cause Analysis System for Automotive Safety Complaints**

[🚀 Live App](https://n7csqgfinj8j9snbsmvtk8.streamlit.app) | [📂 GitHub Repo](https://github.com/Sravanitalari1/AutoRootCauseX)

---

## 📌 Project Overview
**AutoRootCauseX** is an end-to-end, real-time root cause analysis (RCA) system that scrapes safety complaints data from [NHTSA](https://www.nhtsa.gov/) and uses GenAI-powered NLP clustering to discover early signs of failure patterns in Electric & Gasoline Vehicles.

---

## 🧠 Key Capabilities

| Feature | Status | Notes |
|--------|--------|-------|
| 🔄 Real-time data scraping from NHTSA | ✅ Complete | Scrapes by Make, Model, Year |
| 🧼 Data cleaning & preprocessing | ✅ Complete | Basic filters and summaries |
| 🧠 Complaint text clustering (NLP) | ✅ Complete | SentenceTransformer + HDBSCAN |
| 📊 RCA KPI dashboard | 🔄 In Progress | Building advanced KPIs |
| 🧾 Root Cause Summarization (GenAI) | 🔄 In Progress | To be powered by open-source LLMs |
| 📤 Export insights to CSV/PDF | 🚧 Planned | Batch reports for business teams |
| 💡 KPI alerts & trend monitoring | 🚧 Planned | For early issue detection |
| 🌐 Fully hosted & free | ✅ Complete | Built on GitHub Codespaces + Streamlit Cloud |

---

## 🎯 KPIs (In Progress — Coming Next)

We are building **deep-research-level KPIs** tailored for RCA analysts and safety engineers:

- **Failure Trend Velocity** (per component per region)
- **Latent Complaint Cluster Growth Rate**
- **First-Time Component Mention (FTCM)**
- **Severity-Weighted Complaint Score**
- **Geo-Sentiment Risk Zones**
- **Recurring VIN Pattern Detection**
- **Cluster Novelty Score (emerging issue signal)**

> ✅ Let us know if you'd like to prioritize specific KPIs in your portfolio demo.

---

## 📁 Project Structure

```bash
AutoRootCauseX/
│
├── app.py                     # Main Streamlit application
├── data/
│   └── data_fetcher.py        # NHTSA live complaint scraper
├── nlp/
│   └── clustering.py          # Embedding & complaint clustering
├── requirements.txt           # All packages needed
└── README.md                  # This file
