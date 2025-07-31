# AutoRootCauseX 🔍⚙️

**Real-Time Root Cause Analysis for Automotive Complaints**

---

## Why I Built This

I created AutoRootCauseX to solve a real pain point in automotive aftersales and warranty claims analysis. Companies spend too much time manually digging through thousands of complaints to find patterns and root causes. My goal is to automate this process using AI — combining live data scraping, natural language processing, and advanced clustering techniques to deliver actionable insights quickly.

---

## What It Does

- Scrapes up-to-date vehicle complaint data directly from NHTSA’s official API — no static or outdated datasets.
- Cleans and processes complaint text for analysis.
- Uses state-of-the-art sentence embeddings and unsupervised clustering (HDBSCAN) to identify groups of similar failure complaints.
- Provides an interactive dashboard built with Streamlit where users can explore data, run root cause analysis, and see preliminary KPIs.
- Deploys fully online using free tools like GitHub Codespaces and Streamlit Cloud — no paid servers or complex setup needed.

---

## Current Progress

| Feature                         | Status             | Notes                          |
|--------------------------------|--------------------|--------------------------------|
| Real-time data scraper          | ✅ Completed       | Works with flexible vehicle filters (make, model, year) |
| Data preprocessing             | ✅ Completed       | Basic cleaning and filtering   |
| NLP-based clustering           | ✅ Completed       | SentenceTransformer + HDBSCAN  |
| Streamlit interactive dashboard| ✅ Completed       | Displays data and clusters     |
| Advanced KPIs and metrics      | 🔄 In Progress     | Designing deep, meaningful KPIs focused on real-world RCA needs |
| GenAI-based root cause summaries| 🔄 In Progress     | Working on integrating open-source LLM models for auto-labeling and explanation |
| Export options (CSV, PDF)       | 🚧 Planned         | To enable easy sharing of reports |
| Additional UI/UX polishing      | 🚧 Planned         | Improve visuals and user experience |

---



## Why This Matters

This project is designed for automotive engineers, warranty analysts, and data scientists working to speed up diagnostics, reduce recall costs, and improve vehicle quality — especially in the growing electric vehicle segment.

By automating root cause analysis, companies can catch emerging issues earlier and act faster, improving safety and customer satisfaction.

---

## What’s Next

- Add detailed KPIs like failure trend velocity, recurrence density, and geo-risk scoring.
- Integrate GenAI to summarize clusters with natural language insights.
- Build export features for sharing reports with business teams.
- Refine the UI to make it intuitive for non-technical users.

---

## Connect with Me

I’m Sravani Talari — passionate about solving real-world problems with data and AI.

- GitHub: [sravanitalari1](https://github.com/sravanitalari1)  
- LinkedIn: [linkedin.com/in/sravanitalari](https://linkedin.com/in/sravanitalari)

Feel free to reach out if you want to collaborate or learn more about this project!

---

## License

MIT License — free to use and adapt.


1. Open this project in GitHub Codespaces (or clone locally).
2. Install dependencies:
