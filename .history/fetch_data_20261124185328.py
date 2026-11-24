import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

rows = []
genres = ["rock", "pop", "jazz"]  # Target classes for classification

for genre in genres:
    results = sp.search(q=f"genre:{genre}", type="track", limit=20000)
    for t in results["tracks"]["items"]:
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
            "target_genre": genre
        })

df = pd.DataFrame(rows)
df.to_csv("dataset.csv", index=False)
print(df.head())