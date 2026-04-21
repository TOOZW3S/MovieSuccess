import pandas as pd

# Load original dataset
df = pd.read_csv("TMDB_movie_dataset_v11.csv", low_memory=False)

# Columns to remove
columns_to_drop = [
    "backdrop_path",
    "homepage",
    "imdb_id",
    "original_title",
    "overview",
    "poster_path",
    "tagline",
    "spoken_language",
    "spoken_languages",
    "keywords"
]

# Only drop columns that actually exist (prevents errors)
columns_to_drop = [col for col in columns_to_drop if col in df.columns]

# Drop columns
df_cleaned = df.drop(columns=columns_to_drop)

# Save new dataset
df_cleaned.to_csv("movies_removed_columns.csv", index=False)

print("Columns removed:", columns_to_drop)
print("Done. File saved as movies_removed_columns.csv")
