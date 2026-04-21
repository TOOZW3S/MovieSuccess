import os
import pandas as pd

FOLDERS = ["MoreThanJustUS", "OnlyUSdata"]

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

        required = ["budget", "revenue"]
        if any(col not in df.columns for col in required):
            print(f"Skipping {filename}: missing budget/revenue")
            continue

        # Convert to numeric
        df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

        # Remove bad rows
        df = df[(df["budget"] > 0) & (df["revenue"] > 0)].copy()

        if df.empty:
            print(f"Skipping {filename}: no valid financial data")
            continue

        # Profit
        df["profit"] = df["revenue"] - df["budget"]

        # Metrics
        total_movies = len(df)
        total_profit = df["profit"].sum()
        avg_profit = df["profit"].mean()
        avg_budget = df["budget"].mean()

        results.append({
            "decade": clean_decade_name(filename),
            "total_movies": total_movies,
            "total_profit": total_profit,
            "average_profit_per_movie": avg_profit,
            "average_budget": avg_budget
        })

        print(f"Processed: {filename}")

    if results:
        summary_df = pd.DataFrame(results)

        # Sort decades logically (not alphabetically)
        def sort_key(x):
            if "before_1920s" in x:
                return 0
            if "current" in x:
                return 9999
            try:
                return int(x[:4])
            except:
                return 9998

        summary_df["sort"] = summary_df["decade"].apply(sort_key)
        summary_df = summary_df.sort_values("sort").drop(columns=["sort"])

        output_path = os.path.join(folder_name, "decade_summary.csv")
        summary_df.to_csv(output_path, index=False)

        print(f"Saved summary: {output_path}")
    else:
        print(f"No results for {folder_name}")

def main():
    for folder in FOLDERS:
        process_folder(folder)

if __name__ == "__main__":
    main()
