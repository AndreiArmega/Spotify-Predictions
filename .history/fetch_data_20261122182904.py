import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-library-read"))

results = sp.current_user_saved_tracks(limit=5)
for item in results["items"]:
    print(item["track"]["name"], "-", item["track"]["artists"][0]["name"])