import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Search public tracks without needing user login
results = sp.search(q="genre:rock", type="track", limit=10)

with open("data.txt", "w", encoding="utf-8") as f:
    for track in results["tracks"]["items"]:
        line = f"{track['name']} | {track['artists'][0]['name']} | {track['duration_ms']}\n"
        f.write(line)

print("Done! Saved to data.txt")