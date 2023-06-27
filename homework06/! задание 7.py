import pandas as pd
import random
import matplotlib.pyplot as plt

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)

genre_means = data.groupby('music_genre').mean()

popular_genre = genre_means['popularity'].idxmax()
unpopular_genre = genre_means['popularity'].idxmin()

popular_means = genre_means.loc[popular_genre]
unpopular_means = genre_means.loc[unpopular_genre]

fig, ax = plt.subplots(figsize=(10, 5))
ax.tick_params(axis='both', which='major', labelsize=6, rotation=25)
ax.bar(popular_means.index, popular_means.values, color='red', label='Самый популярный жанр', edgecolor='black')
ax.bar(unpopular_means.index, unpopular_means.values, color='grey', label='Самый непопулярный жанр', edgecolor='black')
ax.set_ylabel('Среднее значение', size=14)
ax.set_title('Соотношение самого популярного и самого непопулярного жанров', size=16)
ax.legend(loc='best', fontsize=12)

plt.show()
