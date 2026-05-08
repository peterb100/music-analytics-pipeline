# 🎵 Music Analytics Data Pipeline

## Overview & Business Problem
This project is an end-to-end, event-driven Data Engineering pipeline built on Google Cloud Platform (GCP). It simulates a real-world SaaS music streaming platform, ingesting daily listening events, processing them through a scalable cloud architecture, and exposing the data to a BI tool for business intelligence.

> **📊 Data Context Note:** The live Looker Studio dashboard is powered by a custom Python data generator simulating a **90-day period ending on May 8, 2026**. I engineered this synthetic dataset to reflect real-world business complexities, including:
> * Platform-specific listener behavior (e.g., high skip rates on free tiers vs. low skip rates on premium tiers).
> * Realistic revenue distribution based on actual industry platform payouts.
> * Time-series trends including weekend streaming spikes, linear audience growth, and the lifecycle of a "viral track" release.

## 🏗️ Pipeline Architecture
1. **Data Generation:** A Python script generates realistic, weighted synthetic data (simulating platforms like Spotify, Apple Music, and YouTube) and automatically pushes a timestamped CSV batch to Google Cloud Storage.
2. **Ingestion (Event-Driven):** A Cloud Function is triggered the moment the file lands in the GCS bucket, validating and loading the raw data into BigQuery.
3. **Data Warehouse (BigQuery):** Data is stored in a highly optimized `fact_streams` table.
4. **Transformation / Cleansing:** A Medallion-style approach is used. A SQL View utilizes Window Functions to handle data deduplication, exposing only clean data to the BI layer.
5. **Visualization:** Looker Studio connects to the cleansed BigQuery View to render interactive dashboards.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Cloud Provider:** Google Cloud Platform (GCP)
* **Storage:** Google Cloud Storage (GCS)
* **Compute:** Cloud Functions
* **Data Warehouse:** BigQuery
* **BI / Visualization:** Looker Studio
* **Version Control:** Git / GitHub

## 🚀 Key Engineering Features
* **Automated Ingestion:** Python script executes OS-level `gsutil` commands for 1-click generation and cloud ingestion.
* **Resilient Deduplication:** Implemented BigQuery Window Functions (`QUALIFY ROW_NUMBER()`) in a logical View layer to ensure zero duplicate records reach the dashboard, even if source files are re-uploaded.
* **Warehouse Optimization:** BigQuery table utilizes Data Definition Language (DDL) with strict typing, `PARTITION BY date` to minimize query costs, and `CLUSTER BY artist_id, platform` for high-performance dashboard filtering.
* **BI Logic:** Engineered calculated fields within Looker Studio to safely aggregate Boolean metrics (e.g., Skip Rates) for accurate reporting.

## 📂 Repository Structure
* `/src` - Contains the automated Python `data_generator.py` script.
* `/cloud_functions` - Contains the `main.py` and `requirements.txt` deployed to GCP for GCS-to-BigQuery ingestion.
* `/sql` - Contains the DDL schema for table creation (`fact_streams_schema.sql`) and the Medallion deduplication view.
* `/images` - Contains architecture diagrams and Looker Studio dashboard screenshots.

---
*Developed by Peter B.*