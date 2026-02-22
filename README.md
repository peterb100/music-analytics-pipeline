### 🏗️ Pipeline Architecture
```mermaid
graph LR
    A[Python Data Gen] -->|CSV Upload| B(Cloud Storage)
    B -->|Object Finalized Event| C{Eventarc}
    C -->|Trigger| D[Cloud Function 2nd Gen]
    D -->|Insert| E[(BigQuery Warehouse)]
    E -->|Live Sync| F[Looker Studio Dashboard]
