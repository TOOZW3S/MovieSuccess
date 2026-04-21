import pandas as pd

# Load dataset
df = pd.read_csv("movies_removed_columns.csv", low_memory=False)

# Convert release_date to datetime
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

# Keep only valid dates
df = df[df["release_date"].notna()].copy()

# Extract year
df["release_year"] = df["release_date"].dt.year

# -----------------------------
# CREATE DATASETS
# -----------------------------

before_1920s = df[df["release_year"] < 1920]

movies_1920s = df[(df["release_year"] >= 1920) & (df["release_year"] <= 1929)]
movies_1930s = df[(df["release_year"] >= 1930) & (df["release_year"] <= 1939)]
movies_1940s = df[(df["release_year"] >= 1940) & (df["release_year"] <= 1949)]
movies_1950s = df[(df["release_year"] >= 1950) & (df["release_year"] <= 1959)]
movies_1960s = df[(df["release_year"] >= 1960) & (df["release_year"] <= 1969)]
movies_1970s = df[(df["release_year"] >= 1970) & (df["release_year"] <= 1979)]
movies_1980s = df[(df["release_year"] >= 1980) & (df["release_year"] <= 1989)]
movies_1990s = df[(df["release_year"] >= 1990) & (df["release_year"] <= 1999)]
movies_2000s = df[(df["release_year"] >= 2000) & (df["release_year"] <= 2009)]
movies_2010s = df[(df["release_year"] >= 2010) & (df["release_year"] <= 2019)]
current_decade = df[(df["release_year"] >= 2020) & (df["release_year"] <= 2029)]

# -----------------------------
# SAVE FILES
# -----------------------------

before_1920s.to_csv("before_1920s.csv", index=False)

movies_1920s.to_csv("1920s.csv", index=False)
movies_1930s.to_csv("1930s.csv", index=False)
movies_1940s.to_csv("1940s.csv", index=False)
movies_1950s.to_csv("1950s.csv", index=False)
movies_1960s.to_csv("1960s.csv", index=False)
movies_1970s.to_csv("1970s.csv", index=False)
movies_1980s.to_csv("1980s.csv", index=False)
movies_1990s.to_csv("1990s.csv", index=False)
movies_2000s.to_csv("2000s.csv", index=False)
movies_2010s.to_csv("2010s.csv", index=False)

current_decade.to_csv("current_decade.csv", index=False)

# -----------------------------
# PRINT COUNTS
# -----------------------------

print("before_1920s:", len(before_1920s))
print("1920s:", len(movies_1920s))
print("1930s:", len(movies_1930s))
print("1940s:", len(movies_1940s))
print("1950s:", len(movies_1950s))
print("1960s:", len(movies_1960s))
print("1970s:", len(movies_1970s))
print("1980s:", len(movies_1980s))
print("1990s:", len(movies_1990s))
print("2000s:", len(movies_2000s))
print("2010s:", len(movies_2010s))
print("current_decade:", len(current_decade))

print("Done.")
