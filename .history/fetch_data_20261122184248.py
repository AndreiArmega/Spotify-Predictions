import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

try:
    features = sp.audio_features(["0eAuGrXyGFYwur9ARUe7LJ"])
    print(features)
except spotipy.exceptions.SpotifyException as e:
    print(f"Blocked by Spotify (HTTP {e.http_status}): {e.msg}")