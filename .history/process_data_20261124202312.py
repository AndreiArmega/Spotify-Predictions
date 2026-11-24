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

df["title_word_count"] = df["track_name"].str.split().str.len()
df["title_char_count"] = df["track_name"].str.len()

rf_base = [
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
        "album_type",
        "query_genre",
    ]
    if c in df.columns
]

rf_cat_cols = [c for c in ["album_type", "query_genre"] if c in rf_base]
rf_df = pd.get_dummies(
    df[rf_base], columns=rf_cat_cols, drop_first=False, dtype=int
)
rf_df["is_early_track"] = df["is_early_track"].values
rf_df.to_csv(RF_OUTPUT_CSV, index=False)

cb_base = [
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
        "artist_name",
        "album_type",
        "query_genre",
    ]
    if c in df.columns
]

cb_df = df[cb_base].copy()
cb_df["is_early_track"] = df["is_early_track"].values
cb_df.to_csv(CB_OUTPUT_CSV, index=False)

rf_feature_count = rf_df.shape[1] - 1
cb_feature_count = cb_df.shape[1] - 1
print(
    f"Saved {len(df)} rows | RF features: {rf_feature_count} | CB features:"
    f" {cb_feature_count}"
)