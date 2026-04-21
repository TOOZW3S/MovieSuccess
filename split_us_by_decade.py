import pandas as pd

# Load cleaned dataset (columns already removed)
df = pd.read_csv("movies_removed_columns.csv", low_memory=False)

# Convert release_date to datetime
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

# Keep valid dates only
df = df[df["release_date"].notna()].copy()

# Extract year
df["release_year"] = df["release_date"].dt.year

# -----------------------------
# FILTER U.S. MOVIES
# -----------------------------
country_text = df["production_countries"].fillna("").astype(str)

df_us = df[
    country_text.str.contains(
        r'"US"|United States of America|United States',
        case=False,
        regex=True
    )
].copy()

# -----------------------------
# SPLIT INTO DECADES
# -----------------------------

us_before_1920s = df_us[df_us["release_year"] < 1920]

us_1920s = df_us[(df_us["release_year"] >= 1920) & (df_us["release_year"] <= 1929)]
us_1930s = df_us[(df_us["release_year"] >= 1930) & (df_us["release_year"] <= 1939)]
us_1940s = df_us[(df_us["release_year"] >= 1940) & (df_us["release_year"] <= 1949)]
us_1950s = df_us[(df_us["release_year"] >= 1950) & (df_us["release_year"] <= 1959)]
us_1960s = df_us[(df_us["release_year"] >= 1960) & (df_us["release_year"] <= 1969)]
us_1970s = df_us[(df_us["release_year"] >= 1970) & (df_us["release_year"] <= 1979)]
us_1980s = df_us[(df_us["release_year"] >= 1980) & (df_us["release_year"] <= 1989)]
us_1990s = df_us[(df_us["release_year"] >= 1990) & (df_us["release_year"] <= 1999)]
us_2000s = df_us[(df_us["release_year"] >= 2000) & (df_us["release_year"] <= 2009)]
us_2010s = df_us[(df_us["release_year"] >= 2010) & (df_us["release_year"] <= 2019)]
us_current_decade = df_us[(df_us["release_year"] >= 2020) & (df_us["release_year"] <= 2029)]

# -----------------------------
# SAVE FILES
# -----------------------------

us_before_1920s.to_csv("us_before_1920s.csv", index=False)

us_1920s.to_csv("us_1920s.csv", index=False)
us_1930s.to_csv("us_1930s.csv", index=False)
us_1940s.to_csv("us_1940s.csv", index=False)
us_1950s.to_csv("us_1950s.csv", index=False)
us_1960s.to_csv("us_1960s.csv", index=False)
us_1970s.to_csv("us_1970s.csv", index=False)
us_1980s.to_csv("us_1980s.csv", index=False)
us_1990s.to_csv("us_1990s.csv", index=False)
us_2000s.to_csv("us_2000s.csv", index=False)
us_2010s.to_csv("us_2010s.csv", index=False)

us_current_decade.to_csv("us_current_decade.csv", index=False)

# -----------------------------
# PRINT COUNTS
# -----------------------------

print("US before 1920s:", len(us_before_1920s))
print("US 1920s:", len(us_1920s))
print("US 1930s:", len(us_1930s))
print("US 1940s:", len(us_1940s))
print("US 1950s:", len(us_1950s))
print("US 1960s:", len(us_1960s))
print("US 1970s:", len(us_1970s))
print("US 1980s:", len(us_1980s))
print("US 1990s:", len(us_1990s))
print("US 2000s:", len(us_2000s))
print("US 2010s:", len(us_2010s))
print("US current decade:", len(us_current_decade))

print("Done.")
