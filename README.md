# 🩺 How Likely Is Breast Cancer Really?

*A data-informed companion for moments of health anxiety.*

## 🧠 Overview

**How Likely Is Breast Cancer Really?** is an interactive web app that helps users estimate their contextual risk for breast cancer based on personal health, hormonal, lifestyle, and genetic factors. The goal is **not diagnosis**, but **perspective** — transforming moments of panic into empowered understanding using real-world data.

This project was built with empathy in mind, especially for young people who feel overwhelmed by health anxiety or “doom-Googling” symptoms without clarity.

---

## ✨ Features

✅ **Personalized risk insights**  
✅ **Contextual explanations** of contributing factors  
✅ **Visual comparison** with population-level incidence  
✅ **Actionable recommendations** based on risk level  
✅ Secure backend API powered by FastAPI  
✅ Frontend powered by Streamlit with clean UX  
✅ ETL pipelines to process large-scale epidemiological data  
✅ SQLite database with breast cancer risk baselines

---


## ⚙️ Tech Stack

| Layer        | Tools/Frameworks                      |
|--------------|----------------------------------------|
| **Frontend** | `Streamlit`, `Plotly`, `Requests`     |
| **Backend**  | `FastAPI`, `Uvicorn`, `Pydantic`      |
| **ETL**      | `Pandas`, `NumPy`, `SQLite`, `SQLAlchemy` |
| **Database** | `SQLite` with preprocessed cancer datasets |
| **Deployment** | `Render` (Backend), `Streamlit Cloud` (Frontend) |

---

## 🔍 Data Sources

- **SEER & WHO Breast Cancer Statistics**
- Synthetic + real-world processed data from:
  - [CDC](https://www.cdc.gov/)
  - [NIH](https://www.nih.gov/)
  - Public breast cancer research datasets
- All raw datasets can be found in:  
  `backend/data/raw`  
  Processed and loaded into:  
  `backend/data/processed/breast_cancer_risk.db`

---



