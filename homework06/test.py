import pandas as pd
import random
import seaborn as sns
import matplotlib.pyplot as plt

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)

duration_bins = [0, 180000, 300000, float('inf')]
duration_labels = ['Короткая', 'Средняя', 'Длинная']
data['duration_ms'] = pd.cut(data['duration_ms'], bins=duration_bins, labels=duration_labels)
duration_counts = data['duration_ms'].value_counts()
plt.pie(duration_counts, labels=duration_counts.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4}, labeldistance=1.2, pctdistance=0.8)
plt.title('Соотношение треков по длительности')
plt.show()
