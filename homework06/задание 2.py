import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)

#1
genre_counts = data['music_genre'].value_counts(normalize=True)
print("Количество треков по жанрам:\n", genre_counts)

#2
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1)
genre_counts = data['music_genre'].value_counts()
colors = ['gray']*len(genre_counts.index)
max_genre = genre_counts.idxmax()
colors[list(genre_counts.index).index(max_genre)] = 'red'
sns.countplot(x='music_genre', data=data, order=genre_counts.index, palette=colors)
plt.xticks(rotation=35)
plt.title('Распределение количества треков по жанрам')
plt.xlabel('Жанр')
plt.ylabel('Количество треков')

plt.show()


#3
genre_danceability = data.groupby('music_genre')['danceability'].mean()
most_danceable_genre = genre_danceability.sort_values(ascending=False).index[0]

print(f"Самый танцевальный жанр: {most_danceable_genre}\n")

#4
ct = pd.crosstab(index=data['music_genre'], columns=data['mode'])

ct['predominant_key'] = ct.apply(lambda row: 'major' if row['Major'] > row['Minor'] else 'minor', axis=1)

ct = ct[['Major', 'Minor', 'predominant_key']]

ct.columns = ['major', 'minor', 'predominant_key']

print(ct)
