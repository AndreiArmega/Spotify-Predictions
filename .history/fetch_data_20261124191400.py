import os
import time
import pandas as pd
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

OUTPUT_CSV = "dataset.csv"
TARGET_ROWS = 10000  

genres = [
    "rock", "pop", "hip-hop", "jazz", "electronic",
    "indie", "classical", "metal", "r-n-b", "country"
]
years = list(range(1990, 2026))


if os.path.exists(OUTPUT_CSV):
    existing_df = pd.read_csv(OUTPUT_CSV)
    rows = existing_df.to_dict("records")
    seen_ids = set(existing_df["track_id"].dropna().astype(str))
else:
    rows = []
    seen_ids = set()

def save_progress():
    pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False)

for year in years:
    for genre in genres:
        if len(rows) >= TARGET_ROWS:
            break

        query = f"genre:{genre} year:{year}"

      
        for offset in range(0, 50, 10):
            if len(rows) >= TARGET_ROWS:
                break

            try:
                res = sp.search(q=query, type="track", limit=10, offset=offset)
            except SpotifyException as e:
                if e.http_status == 429:
                    retry_after = 10
                    if e.headers and "Retry-After" in e.headers:
                        retry_after = int(e.headers["Retry-After"])
                    print(f"Rate limited (429). Saving {len(rows)} rows and sleeping {retry_after}s...")
                    save_progress()
                    time.sleep(retry_after + 1)
                    continue
                raise

            items = res.get("tracks", {}).get("items", [])
            if not items:
                break

            for t in items:
                tid = t.get("id")
                if not tid or tid in seen_ids:
                    continue

                album = t.get("album", {})
                rel_date = album.get("release_date", "")
                rel_year = int(rel_date[:4]) if len(rel_date) >= 4 and rel_date[:4].isdigit() else None

                rows.append({
                    "track_id": tid,
                    "track_name": t.get("name"),
                    "artist_name": t["artists"][0]["name"] if t.get("artists") else None,
                    "duration_ms": t.get("duration_ms"),
                    "explicit": int(bool(t.get("explicit"))),
                    "track_number": t.get("track_number"),
                    "disc_number": t.get("disc_number"),
                    "album_type": album.get("album_type"),
                    "total_tracks": album.get("total_tracks"),
                    "release_year": rel_year,
                    "num_artists": len(t.get("artists", [])),
                    "query_genre": genre,
                })
                seen_ids.add(tid)

            time.sleep(0.35)

        if len(rows) % 100 < 10:
            save_progress()

    if len(rows) >= TARGET_ROWS:
        break

save_progress()
print(f"Finished. Total unique rows in {OUTPUT_CSV}: {len(rows)}")