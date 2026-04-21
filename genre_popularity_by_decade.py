import os
import re
import ast
import json
import pandas as pd

# Correct folder names
FOLDERS = ["MoreThanJustUS", "OnlyUSdata"]

def parse_genres(value):
    """
    Return a list of genre names from many possible formats.
    """
    if pd.isna(value):
        return []

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "null", "[]"}:
        return []

    # Try JSON first
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            names = []
            for item in parsed:
                if isinstance(item, dict) and "name" in item:
                    names.append(str(item["name"]).strip())
                elif isinstance(item, str):
                    names.append(item.strip())
            if names:
                return names
    except Exception:
        pass

    # Try Python literal format
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            names = []
            for item in parsed:
                if isinstance(item, dict) and "name" in item:
                    names.append(str(item["name"]).strip())
                elif isinstance(item, str):
                    names.append(item.strip())
            if names:
                return names
    except Exception:
        pass

    # Try extracting "name": "Genre" patterns manually
    found_names = re.findall(r"""['"]name['"]\s*:\s*['"]([^'"]+)['"]""", text)
    if found_names:
        return [name.strip() for name in found_names if name.strip()]

    # If it looks like a simple delimited string, split it
    for sep in ["|", ","]:
        if sep in text and "name" not in text:
            parts = [part.strip(" []'\"") for part in text.split(sep)]
            parts = [part for part in parts if part]
            if parts:
                return parts

    # Last fallback: treat the whole cell as one genre if it is plain text
    cleaned = text.strip(" []'\"")
    if cleaned and "{" not in cleaned and "}" not in cleaned:
        return [cleaned]

    return []

def clean_decade_name(filename):
    return filename.replace(".csv", "")

def process_folder(folder_name):
    results = []

    if not os.path.isdir(folder_name):
        print(f"Folder not found: {folder_name}")
        return

    print(f"\nProcessing folder: {folder_name}")

    for filename in sorted(os.listdir(folder_name)):
        if not filename.endswith(".csv"):
            continue

        file_path = os.path.join(folder_name, filename)

        try:
            df = pd.read_csv(file_path, low_memory=False)
        except Exception as e:
            print(f"Could not read {file_path}: {e}")
            continue

        required_columns = ["genres", "popularity", "budget", "revenue"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Skipping {filename}: missing columns {missing_columns}")
            continue

        # Convert numeric columns
        df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")
        df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

        # Keep rows with usable popularity
        df = df[df["popularity"].notna()].copy()

        if df.empty:
            print(f"Skipping {filename}: no valid popularity values")
            continue

        # Profit = revenue - budget
        df["profit"] = df["revenue"] - df["budget"]

        # Parse genres
        df["genre_list"] = df["genres"].apply(parse_genres)

        sample_nonempty = df[df["genre_list"].map(len) > 0]
        if sample_nonempty.empty:
            print(f"Skipping {filename}: no usable genre data")
            print("First 5 raw genre values:")
            print(df["genres"].head(5).to_string(index=False))
            continue

        # Split movies with multiple genres into multiple rows
        exploded = df.explode("genre_list").copy()
        exploded = exploded[exploded["genre_list"].notna()]
        exploded["genre_list"] = exploded["genre_list"].astype(str).str.strip()
        exploded = exploded[exploded["genre_list"] != ""]

        if exploded.empty:
            print(f"Skipping {filename}: exploded genre data empty")
            continue

        grouped = (
            exploded.groupby("genre_list", as_index=False)
            .agg(
                movie_count=("genre_list", "size"),
                average_popularity=("popularity", "mean"),
                total_popularity=("popularity", "sum"),
                average_budget=("budget", "mean"),
                average_revenue=("revenue", "mean"),
                average_profit_per_movie=("profit", "mean"),
                total_profit=("profit", "sum")
            )
        )

        # Top 5 genres ranked by average popularity
        grouped = grouped.sort_values(
            by=["average_popularity", "movie_count", "total_popularity"],
            ascending=[False, False, False]
        ).head(5).copy()

        grouped["rank"] = range(1, len(grouped) + 1)
        grouped["decade"] = clean_decade_name(filename)

        grouped = grouped[
            [
                "decade",
                "rank",
                "genre_list",
                "movie_count",
                "average_popularity",
                "total_popularity",
                "average_budget",
                "average_revenue",
                "average_profit_per_movie",
                "total_profit"
            ]
        ].rename(columns={"genre_list": "genre"})

        results.append(grouped)
        print(f"Processed: {file_path}")

    if results:
        final_df = pd.concat(results, ignore_index=True)
        output_path = os.path.join(folder_name, "top5_genres_by_decade.csv")
        final_df.to_csv(output_path, index=False)
        print(f"Saved summary: {output_path}")
    else:
        print(f"No results created for {folder_name}")

def main():
    for folder in FOLDERS:
        process_folder(folder)

if __name__ == "__main__":
    main()
