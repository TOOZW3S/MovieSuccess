# Movie Success Analysis

This project analyzes movie financial performance and genre trends using the TMDB movie dataset.

## Original Dataset

The raw dataset comes from Kaggle:

[Full TMDB Movies Dataset 2024 (1M Movies)](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)

Expected local file path:

```text
Dataset/TMDB_movie_dataset_v11.csv
```

The `Dataset/` directory is ignored by Git because the raw CSV is large.

## Project Contents

- `movie_success_analysis.ipynb` combines the filtering, summary generation, genre analysis, inflation adjustment, and matplotlib visualizations in one notebook.
- `remove_columns.py` removes unused columns from the raw dataset.
- `split_by_decade.py` splits the cleaned dataset into decade-level CSVs.
- `split_us_by_decade.py` filters U.S. movies and splits them by decade.
- `decade_summary.py` summarizes profit and budget by decade.
- `genre_popularity_by_decade.py` ranks top genres by average popularity.
- `genre_profit_by_decade.py` ranks top genres by total profit.
- `inflation_adjusted_summary.py` applies manual inflation adjustments to decade summaries.

## Running the Notebook

From the project root:

```powershell
jupyter notebook movie_success_analysis.ipynb
```

The notebook reads the dataset from `Dataset/TMDB_movie_dataset_v11.csv`. By default, `EXPORT_OUTPUTS = False`, so running the notebook will not overwrite generated CSV outputs unless you change that setting.

