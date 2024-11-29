import pandas as pd
import random
import matplotlib.pyplot as plt

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)
data = data.drop_duplicates()
data = data[(data.artist_name != 'empty_field')]


popular_genre = data['music_genre'].value_counts().idxmax()
unpopular_genre = data['music_genre'].value_counts().idxmin()

popular_data = data[data['music_genre'] == popular_genre]
unpopular_data = data[data['music_genre'] == unpopular_genre]

most_popular_means = popular_data.mean()
least_popular_means = unpopular_data.mean()

fig, ax = plt.subplots(figsize=(10, 10))
ax.bar(most_popular_means.index, most_popular_means, color='grey', label=popular_genre)
ax.bar(least_popular_means.index, least_popular_means, color='red', label=unpopular_genre)
ax.set_ylabel('Средние значения')
ax.tick_params(axis='x', labelrotation=45)
ax.legend()
plt.show()





'''data.drop(['instance_id', 'duration_ms', 'popularity'], inplace=True, axis=1)


most_popular_indexes = data[data['music_genre'] == popular_genre].index
least_popular_indexes = data[data['music_genre'] == unpopular_genre].index

# выборка соответствующих строк
popular_data = data.loc[most_popular_indexes]
unpopular_data = data.loc[least_popular_indexes]

# вычисление средних значений по всем характеристикам
most_popular_means = popular_data.mean()
least_popular_means = unpopular_data.mean()

# создание графика
fig, ax = plt.subplots()

# добавление баров для средних значений
ax.bar(most_popular_means.index, most_popular_means, color='green', label=popular_genre)
ax.bar(least_popular_means.index, least_popular_means, color='red', label=unpopular_genre)

# настройка осей
ax.set_ylabel('Средние значения')
ax.tick_params(axis='x', labelrotation=90)

# добавление легенды и отображение графика
ax.legend()
plt.show()'''
