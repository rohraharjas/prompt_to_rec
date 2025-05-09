import pandas as pd

df = pd.read_csv('df.csv')
genres = df['genres']

import ast

unique_genres = set()

for item in genres:
    try:
        genre_list = ast.literal_eval(item)  # Safely parse the string into a Python list
        unique_genres.update(genre_list)
    except Exception as e:
        print(f"Skipping invalid item: {item} ({e})")

print(unique_genres)
