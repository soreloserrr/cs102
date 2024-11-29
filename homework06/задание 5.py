import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)


fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(1, 1, 1)
sns.boxplot(x='music_genre', y='popularity', data=data)

plt.show()
