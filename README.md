# AutoRootCauseX 🔍⚙️

**Real-Time Root Cause Analysis for Automotive Complaints**

---

## About the Project


AutoRootCauseX is an end-to-end AI-powered platform designed to automate root cause analysis (RCA) for vehicle complaints. It scrapes **live complaint data** from the National Highway Traffic Safety Administration (NHTSA) API and uses advanced **natural language processing (NLP)** and **unsupervised clustering** techniques to detect failure patterns, trends, and geographic risks.


## Why I built this?

To solve a real pain point in automotive aftersales and warranty claims analysis. Companies spend too much time manually digging through thousands of complaints to find patterns and root causes. My goal is to automate this process using AI — combining live data scraping, natural language processing, and advanced clustering techniques to deliver actionable insights quickly.

This tool helps accelerate diagnostics, reduce recall costs, and improve vehicle quality - especially crucial for electric vehicles and emerging automotive technologies.
---

## Key Features

- **Live Data Scraping:** Fetches real-time complaint data with flexible filters (make, model, year).
- **NLP Embeddings & Clustering:** Uses SentenceTransformers and HDBSCAN for semantic clustering of complaint texts.
- **Interactive Dashboard:** Powered by Streamlit, offering rich visualizations like:
  - Time series trend charts per cluster
  - Geo heatmaps of complaint density by US states and cluster
  - UMAP projections of complaint embeddings for visual cluster exploration
- **Advanced KPIs:** Deep, research-grade KPIs such as Root Cause Density Index, Recurrence Density, Failure Trend Velocity, Geo Risk Scoring, and more.
- **Cluster Explanation:** Auto-generated human-readable summaries of common complaint themes per cluster.
- **Export Options:** Downloadable CSVs for clusters and complaints, plus PNG images of all charts.
- **Fully Online & Free:** Developed and deployed with GitHub Codespaces and Streamlit Cloud using only free resources — no paid servers or credit cards required.

---


### Project Status & Roadmap

| Feature                             | Status       | Notes                                     |
|-----------------------------------|--------------|-------------------------------------------|
| Live NHTSA Data Scraper           | ✅ Completed | Flexible vehicle filters & robust fetching |
| Text Preprocessing & Embeddings   | ✅ Completed | Clean, vectorized complaint texts         |
| Clustering (HDBSCAN + UMAP)       | ✅ Completed | Stable and interpretable clusters          |
| Streamlit Dashboard & Visualization| ✅ Completed | Interactive charts, maps, and summaries   |
| Advanced KPIs Calculation          | ✅ Completed | Industry-relevant, deep analytics          |
| Cluster Explanation (NLP-based)   | ✅ Completed | Summarizes root causes with human-readable insights |
| Export & Download Features         | ✅ Completed | CSV and PNG downloads                       |
| UI/UX Enhancements                 | 🔄 In Progress | Further polish and responsiveness           |
| GenAI-powered auto labeling & explanations | 🚧 Planned | Integrate open-source LLMs for enriched analysis |

---



## Why This Matters

Traditional root cause analysis in automotive warranty and aftersales is manual, slow, and costly. AutoRootCauseX drastically reduces time-to-insight by automating pattern detection on live data. This leads to:

- Faster identification of systemic issues
- Reduced warranty and recall costs
- Enhanced vehicle safety and customer satisfaction
- Valuable support for new vehicle technologies like EVs and autonomous systems

---

### How to Use

1. Open the project in **GitHub Codespaces** or clone the repo locally.
2. Install dependencies with:
   ```bash
   pip install -r requirements.txt
3. Run the Streamlit app:
   streamlit run app.py
4. Use the sidebar to select vehicle make, model, and year, then click Analyze.
5. Explore KPIs, charts, clusters, and download reports as needed.



## Connect with Me

I’m Sravani Talari — passionate about solving real-world problems with data and AI.

- GitHub: [sravanitalari1](https://github.com/sravanitalari1)  
- LinkedIn: [linkedin.com/in/sravanitalari](https://linkedin.com/in/sravanitalari)

Feel free to reach out if you want to collaborate or learn more about this project!

---
