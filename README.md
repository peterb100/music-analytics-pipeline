# 🎵 The Artist Cockpit: Serverless Music Analytics Pipeline

[![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?style=for-the-badge&logo=google-bigquery&logoColor=white)](https://cloud.google.com/bigquery)

### 🎯 Overview & Business Problem
Independent artists and managers often lack real-time visibility into listener behavior (like skip rates) and actual take-home profit. Moving beyond manual data handling, I architected a **fully automated, event-driven pipeline** on Google Cloud Platform that ingests raw streaming metadata and transforms it into actionable business intelligence. 

This project demonstrates focusing on automated infrastructure, strict schema enforcement, and cost-optimized warehousing.

**📊 [View the Live Looker Studio Dashboard Here](https://lookerstudio.google.com/reporting/e1709d77-530f-470a-90a7-d9cdddffc800)**

---

### 🏗️ Pipeline Architecture

```mermaid
graph LR
    A[Python Data Gen] -->|CSV Upload| B(Cloud Storage)
    B -->|Object Finalized Event| C{Eventarc}
    C -->|Trigger| D[Cloud Function 2nd Gen]
    D -->|Insert| E[(BigQuery Warehouse)]
    E -->|Live Sync| F[Looker Studio Dashboard]
