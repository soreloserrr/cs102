import pandas as pd
import random
import matplotlib.pyplot as plt

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)


top_genres = data.groupby('music_genre').apply(lambda x: x.loc[x['popularity'].idxmax()])
top_genres = top_genres.sort_values('popularity', ascending=False).head(3)
labels = top_genres['music_genre'].tolist()
sizes = top_genres['popularity'].tolist()
explode = [0.1, 0, 0]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')
plt.legend(labels, loc="best")
plt.title("Топ-3 музыкальных жанра")

plt.show()