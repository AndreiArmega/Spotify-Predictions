import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Search for 5 tracks (2026 API max limit is 10 per search call)
results = sp.search(q="year:2024", type="track", limit=5)

with open("track_dump.txt", "w", encoding="utf-8") as f:
    for i, track in enumerate(results["tracks"]["items"], start=1):
        f.write(f"=== TRACK {i} ===\n")
        f.write(json.dumps(track, indent=2))
        f.write("\n\n")

print("Dumped all track attributes to track_dump.txt")