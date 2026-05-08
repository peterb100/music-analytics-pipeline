import functions_framework
from google.cloud import bigquery

# Initialize BigQuery Client (It automatically detects your GCP environment)
bq_client = bigquery.Client()

# Configuration: Dynamically grab the project ID from the client
PROJECT_ID = bq_client.project 
DATASET_ID = "music_warehouse"
TABLE_ID = "fact_streams"
TABLE_REFERENCE = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

@functions_framework.cloud_event
def process_music_data(cloud_event):
    """Triggered by a change to a Cloud Storage bucket."""
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"Processing file: gs://{bucket_name}/{file_name}")

    # Set up BigQuery Load Job configuration
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1, # Skips the header row
        autodetect=False,    # Using strict schema below instead of auto-detect
        schema=[
            bigquery.SchemaField("event_id", "STRING"),
            bigquery.SchemaField("date", "DATE"),
            bigquery.SchemaField("timestamp", "TIMESTAMP"),
            bigquery.SchemaField("artist_id", "STRING"),
            bigquery.SchemaField("track_id", "STRING"),
            bigquery.SchemaField("platform", "STRING"),
            bigquery.SchemaField("country_code", "STRING"),
            bigquery.SchemaField("is_skip", "BOOLEAN"),
            bigquery.SchemaField("seconds_played", "INT64"),
            bigquery.SchemaField("revenue_generated", "FLOAT64"),
        ],
    )

    uri = f"gs://{bucket_name}/{file_name}"

    try:
        # Start the load job
        load_job = bq_client.load_table_from_uri(
            uri, TABLE_REFERENCE, job_config=job_config
        )
        
        # Wait for the job to complete
        load_job.result()  
        
        destination_table = bq_client.get_table(TABLE_REFERENCE)
        print(f"✅ Loaded {load_job.output_rows} rows.")
        print(f"Table now contains {destination_table.num_rows} total rows.")

    except Exception as e:
        print(f"❌ Error loading data to BigQuery: {e}")
        raise e