import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)

#1
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(1, 1, 1)
corr_matrix = data[["popularity", "acousticness", "danceability", "duration_ms", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence"]].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

plt.show()

#2
data['track_name'] = data['track_name'].fillna('')

data['track_name_length'] = data['track_name'].apply(len)
corr = data[['popularity', 'track_name_length']].corr()

print(corr)

