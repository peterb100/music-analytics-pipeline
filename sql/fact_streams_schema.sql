CREATE OR REPLACE TABLE `music_warehouse.fact_streams` (
    event_id STRING,
    date DATE,
    timestamp TIMESTAMP,
    artist_id STRING,
    track_id STRING,
    platform STRING,
    country_code STRING,
    is_skip BOOLEAN,
    seconds_played INT64,
    revenue_generated FLOAT64
)
PARTITION BY date
CLUSTER BY artist_id, platform;
