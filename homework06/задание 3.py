import pandas as pd
import random
import matplotlib.pyplot as plt

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)

#1
most_popular_musician = data['artist_name'].value_counts().idxmax()
print(f"Исполнитель с наибольшим количеством треков: {most_popular_musician}")

least_popular_artist = data['artist_name'].value_counts().idxmin()
print(f"Исполнитель с наименьшим количеством треков: {least_popular_artist}")

#2
top_20_musicians = data['artist_name'].value_counts().head(20)

fig = plt.figure(figsize=(15, 13))
ax = fig.add_subplot(1, 1, 1)
plt.bar(top_20_musicians.index, top_20_musicians.values)
plt.xticks(rotation=35, size=8)
plt.xlabel('Исполнители', size=15)
plt.ylabel('Количество треков', size=15)
plt.title('Топ-20 исполнителей', size=15)

plt.show()
