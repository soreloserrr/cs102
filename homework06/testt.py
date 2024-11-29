import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

random.seed(13)

data = pd.read_csv('music_genre.csv').sample(n=20000, random_state=13)

data = data.drop_duplicates()
data = data[(data.artist_name != 'empty_field')]

corrM = data.corr()
corrM