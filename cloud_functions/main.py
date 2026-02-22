import functions_framework
from google.cloud import bigquery

@functions_framework.cloud_event
def process_music_data(cloud_event):
    data = cloud_event.data
    bucket = data["bucket"]
    name = data["name"]
    uri = f"gs://{bucket}/{name}"
    
    print(f"File detected: {uri}")
    client = bigquery.Client()
    table_id = f"{client.project}.music_warehouse.fact_streams"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition="WRITE_APPEND",
    )

    try:
        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
        load_job.result()
        print(f"Successfully loaded {name} into {table_id}.")
    except Exception as e:
        print(f"Error: {e}")
