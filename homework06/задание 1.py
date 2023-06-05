import pandas as pd
import random

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)

print("Количество дублирующихся строк:", data.duplicated().sum())

data.drop_duplicates(inplace=True)

empty_artist_name = data[data['artist_name'] == 'empty_field']
print("Количество строк с пустым artist_name:", len(empty_artist_name))
print(empty_artist_name)

data = data[data['artist_name'] != 'empty_field']
