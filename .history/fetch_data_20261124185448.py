import time
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

rows = []
query = "genre:rock"

# Example: fetch up to 100 items (10 pages of 10) safely
for offset in range(0, 100, 10):
    results = sp.search(q=query, type="track", limit=10, offset=offset)
    items = results["tracks"]["items"]
    if not items:
        break

    for t in items:
        rows.append({
            "track_name": t["name"],
            "artist_name": t["artists"][0]["name"],
            "duration_ms": t["duration_ms"],
            "explicit": int(t["explicit"]),
            "track_number": t["track_number"],
            "disc_number": t["disc_number"],
            "album_type": t["album"]["album_type"],
            "total_tracks": t["album"]["total_tracks"],
            "release_year": int(t["album"]["release_date"][:4]),
            "num_artists": len(t["artists"]),
        })

    time.sleep(0.3)

df = pd.DataFrame(rows)
df.to_csv("dataset.csv", index=False)
print(f"Saved {len(df)} rows to dataset.csv")