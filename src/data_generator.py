import pandas as pd
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

class MusicSaaSGenerator:
    def __init__(self):
        # We define consistent artists so we can track them over time
        self.artists = [
            {'id': 'art_001', 'name': 'LoFi Boy', 'popularity': 0.8}, # Popular
            {'id': 'art_002', 'name': 'Techno Cat', 'popularity': 0.95}, # Niche
            {'id': 'art_003', 'name': 'Jazz Hands', 'popularity': 0.5}  # Average
        ]
        
        # Define tracks linked to artists
        self.tracks = self._generate_catalog()
        
        self.platforms = {
            'spotify': {'royalty': 0.0035, 'users': 'high'},
            'apple_music': {'royalty': 0.007, 'users': 'medium'},
            'youtube': {'royalty': 0.001, 'users': 'massive'}
        }

    def _generate_catalog(self):
        """Creates a fake catalog of songs for our artists"""
        tracks = []
        for artist in self.artists:
            # Each artist gets 5 songs
            for i in range(1, 6):
                tracks.append({
                    'track_id': f"{artist['id']}_t{i}",
                    'artist_id': artist['id'],
                    'title': fake.sentence(nb_words=3).replace(".", ""), # Fake song title
                    'base_streams': 1000 if artist['popularity'] > 0.6 else 200 # Hits vs Flops logic
                })
        return tracks

    def generate_daily_data(self, date_str):
        data = []
        
        for track in self.tracks:
            # Simulate platform distribution
            for platform, meta in self.platforms.items():
                
                # Random fluctuation (Some days are better than others)
                daily_variance = random.uniform(0.7, 1.3) 
                
                # Calculate number of streams based on base popularity
                stream_count = int(track['base_streams'] * daily_variance)
                if meta['users'] == 'massive': stream_count *= 2 # YouTube gets more views
                if meta['users'] == 'medium': stream_count = int(stream_count * 0.6)

                for _ in range(stream_count):
                    # Metric: Did the user skip the song?
                    is_skip = random.random() < 0.3 # 30% skip rate
                    
                    # Logic: If skipped, duration is short, else full song
                    seconds_played = random.randint(5, 29) if is_skip else random.randint(120, 240)
                    
                    # Logic: Revenue is 0 if skipped or played < 30s
                    revenue = 0 if is_skip else meta['royalty']

                    # For a "zero-padded" timestamp that BigQuery understands (ISO 8601 format).
                    hour = str(random.randint(0, 23)).zfill(2)
                    minute = str(random.randint(0, 59)).zfill(2)
                    second = str(random.randint(0, 59)).zfill(2)

                    record = {
                        'event_id': str(uuid.uuid4()),
                        'date': date_str,
                        'timestamp': f"{date_str} {hour}:{minute}:{second}",
                        'artist_id': track['artist_id'],
                        'track_id': track['track_id'],
                        'platform': platform,
                        'country_code': fake.country_code(),
                        'is_skip': is_skip,
                        'seconds_played': seconds_played,
                        'revenue_generated': round(revenue, 5)
                    }
                    data.append(record)
                    
        return pd.DataFrame(data)

# --- Execution ---
if __name__ == "__main__":
    sim = MusicSaaSGenerator()
    
    # Generate data for the last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    all_data = []
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Generating data for {date_str}...")
        
        daily_df = sim.generate_daily_data(date_str)
        all_data.append(daily_df)
        
        current_date += timedelta(days=1)
    
    # Combine all days into one big DataFrame
    final_df = pd.concat(all_data)
    
    # Save to CSV
    filename = "music_data_export.csv"
    final_df.to_csv(filename, index=False)
    
    print(f"\n✅ Success! Generated {len(final_df)} rows of data.")
    print(f"📁 Saved to: {filename}")
    
    # Quick sanity check
    print("\n--- Sample Data ---")
    print(final_df[['date', 'artist_id', 'platform', 'is_skip', 'revenue_generated']].head())
    
    print("\n--- Revenue Check ---")
    print(final_df.groupby('artist_id')['revenue_generated'].sum())