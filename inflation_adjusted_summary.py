import os
import pandas as pd

FOLDERS = ["MoreThanJustUS", "OnlyUSdata"]

# Manual dollar value by decade relative to current decade dollars
# Interpretation:
# if dollar_value = 0.20, then $1 in that decade is about $5 today
DOLLAR_VALUE_MAP = {
    "before_1920s": 0.06,
    "1920s": 0.07,
    "1930s": 0.08,
    "1940s": 0.12,
    "1950s": 0.20,
    "1960s": 0.30,
    "1970s": 0.50,
    "1980s": 0.80,
    "1990s": 0.77,
    "2000s": 0.55,
    "2010s": 0.42,
    "current_decade": 1.00
}

def normalize_decade_label(decade_value):
    """
    Convert values like:
    us_1920s -> 1920s
    us_current_decade -> current_decade
    1920s -> 1920s
    """
    text = str(decade_value).strip().lower()

    if text.startswith("us_"):
        text = text[3:]

    return text

def process_folder(folder_name):
    input_path = os.path.join(folder_name, "decade_summary.csv")

    if not os.path.exists(input_path):
        print(f"Missing file: {input_path}")
        return

    df = pd.read_csv(input_path)

    # Normalize the decade names for matching
    df["normalized_decade"] = df["decade"].apply(normalize_decade_label)

    # Manually insert dollar value
    df["dollar_value"] = df["normalized_decade"].map(DOLLAR_VALUE_MAP)

    # Inflation multiplier to convert old dollars to current-decade dollars
    df["inflation_multiplier"] = 1 / df["dollar_value"]

    # Adjusted columns
    df["adjusted_budget"] = df["average_budget"] * df["inflation_multiplier"]
    df["adjusted_average_profit"] = df["average_profit_per_movie"] * df["inflation_multiplier"]
    df["adjusted_total_profit"] = df["total_profit"] * df["inflation_multiplier"]

    # Keep original columns plus new ones
    df = df[
        [
            "decade",
            "total_movies",
            "total_profit",
            "average_profit_per_movie",
            "average_budget",
            "dollar_value",
            "adjusted_budget",
            "adjusted_average_profit",
            "adjusted_total_profit"
        ]
    ]

    output_path = os.path.join(folder_name, "decade_summary_inflation_adjusted.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(df.head())

def main():
    for folder in FOLDERS:
        process_folder(folder)

if __name__ == "__main__":
    main()
