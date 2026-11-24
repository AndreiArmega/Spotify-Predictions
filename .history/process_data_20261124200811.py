import re
import pandas as pd

INPUT_CSV = "dataset.csv"
RF_OUTPUT_CSV = "formatted_random_forest.csv"
CB_OUTPUT_CSV = "formatted_catboost.csv"
EARLY_TRACK_CUTOFF = 3

df = pd.read_csv(INPUT_CSV)

df["track_number"] = pd.to_numeric(df["track_number"], errors="coerce")
df = df.dropna(subset=["track_number"]).copy()

df["is_early_track"] = (df["track_number"] <= EARLY_TRACK_CUTOFF).astype(int)

numeric_cols = [
    "duration_ms",
    "explicit",
    "disc_number",
    "total_tracks",
    "release_year",
    "num_artists",
]
for col in numeric_cols:
  if col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median())

df["track_name"] = df["track_name"].fillna("").astype(str)
df["artist_name"] = df["artist_name"].fillna("unknown").astype(str)
df["album_type"] = df["album_type"].fillna("unknown").astype(str)
df["query_genre"] = df["query_genre"].fillna("unknown").astype(str)

title_lower = df["track_name"].str.lower()
df["title_word_count"] = df["track_name"].str.split().str.len()
df["title_char_count"] = df["track_name"].str.len()
df["has_special_tag"] = title_lower.apply(
    lambda s: int(
        bool(
            re.search(
                r"\b(intro|outro|interlude|skit|prelude|remix|live|demo)\b", s
            )
        )
    )
)

base_features = [
    c
    for c in [
        "duration_ms",
        "explicit",
        "disc_number",
        "total_tracks",
        "release_year",
        "num_artists",
        "title_word_count",
        "title_char_count",
        "has_special_tag",
        "artist_name",
        "album_type",
        "query_genre",
    ]
    if c in df.columns
]

cat_cols = [
    c
    for c in ["artist_name", "album_type", "query_genre"]
    if c in base_features
]

rf_df = pd.get_dummies(
    df[base_features], columns=cat_cols, drop_first=False, dtype=int
)
rf_df["is_early_track"] = df["is_early_track"].values
rf_df.to_csv(RF_OUTPUT_CSV, index=False)

cb_df = df[base_features].copy()
cb_df["is_early_track"] = df["is_early_track"].values
cb_df.to_csv(CB_OUTPUT_CSV, index=False)

print(f"Saved {len(df)} rows to {RF_OUTPUT_CSV} and {CB_OUTPUT_CSV}")