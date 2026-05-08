import csv
import random
import uuid
import os
from datetime import datetime, timedelta

# --- CONFIGURATION ---
DAYS_BACK = 90  
BUCKET_NAME = "music-analytics-raw-dev" # Your exact GCS bucket

# Create a dynamic, timestamped filename (e.g., streaming_batch_20260508_160530.csv)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_FILENAME = f"streaming_batch_{timestamp}.csv"

# 1. Market Share & Payouts 
PLATFORMS = ["spotify", "youtube", "apple_music"]
PLATFORM_WEIGHTS = [0.45, 0.40, 0.15] 

PAYOUTS = {
    "apple_music": {"min": 0.007, "max": 0.010, "skip_rate": 0.15}, 
    "spotify": {"min": 0.003, "max": 0.005, "skip_rate": 0.25},     
    "youtube": {"min": 0.0005, "max": 0.002, "skip_rate": 0.45}     
}

# 2. Geography
COUNTRIES = ["US", "UK", "DE", "FR", "RO"]
COUNTRY_WEIGHTS = [0.55, 0.15, 0.10, 0.10, 0.10]

# 3. Artists
ARTISTS = ["art_001", "art_002", "art_003"]
ARTIST_WEIGHTS = [0.50, 0.30, 0.20]

def generate_data():
    print(f"🚀 Generating 90 days of business-grade trend data...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_BACK)
    total_rows = 0
    
    # Simulate a viral track release halfway through our timeline
    release_date = end_date - timedelta(days=45) 
    
    with open(OUTPUT_FILENAME, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "event_id", "date", "timestamp", "artist_id", 
            "track_id", "platform", "country_code", 
            "is_skip", "seconds_played", "revenue_generated"
        ])
        
        current_date = start_date
        day_counter = 0
        
        while current_date <= end_date:
            # --- DAILY VOLUME TRENDS ---
            growth_factor = 1.0 + (day_counter / DAYS_BACK) * 0.8 
            is_weekend = current_date.weekday() >= 5
            weekend_multiplier = 1.35 if is_weekend else 1.0
            
            daily_volume = int(200 * growth_factor * weekend_multiplier)
            
            for _ in range(daily_volume):
                platform = random.choices(PLATFORMS, weights=PLATFORM_WEIGHTS, k=1)[0]
                country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]
                artist = random.choices(ARTISTS, weights=ARTIST_WEIGHTS, k=1)[0]
                
                # --- TRACK RELEASE SPIKE LOGIC ---
                if artist == "art_001":
                    if current_date >= release_date:
                        track = random.choices(["t1", "t2", "t3", "t4", "t5"], weights=[0.10, 0.60, 0.10, 0.10, 0.10], k=1)[0]
                    else:
                        track = random.choices(["t1", "t2", "t3", "t4", "t5"], weights=[0.30, 0.05, 0.30, 0.20, 0.15], k=1)[0]
                else:
                    track = random.choice(["t1", "t2", "t3", "t4", "t5"])
                
                track_name = f"{artist}_{track}"
                
                # --- DYNAMIC LISTENER BEHAVIOR ---
                base_skip_prob = PAYOUTS[platform]["skip_rate"]
                
                if track_name == "art_001_t2" and current_date >= release_date:
                    is_skip = random.random() < (base_skip_prob * 0.5) 
                elif track_name == "art_003_t4":
                    is_skip = random.random() < min(0.85, base_skip_prob * 1.5) 
                else:
                    is_skip = random.random() < base_skip_prob
                    
                # --- CALCULATE REALISTIC REVENUE ---
                platform_rates = PAYOUTS[platform]
                if is_skip:
                    seconds = random.randint(5, 29)
                    rev = random.uniform(platform_rates["min"], platform_rates["max"]) * 0.05 
                else:
                    seconds = random.randint(30, 240)
                    rev = random.uniform(platform_rates["min"], platform_rates["max"])

                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                event_time = current_date.replace(hour=hour, minute=minute, second=random.randint(0, 59))

                writer.writerow([
                    str(uuid.uuid4()),
                    current_date.strftime('%Y-%m-%d'),
                    event_time.strftime('%Y-%m-%d %H:%M:%S'),
                    artist,
                    track_name,
                    platform,
                    country,
                    is_skip,
                    seconds,
                    round(rev, 5)
                ])
                total_rows += 1
            
            current_date += timedelta(days=1)
            day_counter += 1

    print(f"✅ Success! Generated {total_rows} rows into {OUTPUT_FILENAME}")
    
    # --- AUTOMATED CLOUD UPLOAD ---
    print(f"☁️ Initiating automatic upload to gs://{BUCKET_NAME}/...")
    
    # Run the gsutil command automatically
    upload_command = f"gsutil cp {OUTPUT_FILENAME} gs://{BUCKET_NAME}/"
    exit_code = os.system(upload_command)
    
    if exit_code == 0:
        print("🎉 Upload complete! The Cloud Function is now processing the file into BigQuery.")
    else:
        print("❌ Upload failed. Please check your terminal authentication (gcloud auth login).")

if __name__ == "__main__":
    generate_data()