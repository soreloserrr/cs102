# 2
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
import seaborn as sns
from random import choice

data = sns.load_dataset("titanic")
data.head()

survived = data[data["survived"] == 1]
died = data[data["survived"] == 0]


sns.histplot(survived["fare"], color="grey", label="Спасшиеся")
sns.histplot(died["fare"], color="red", label="Погибшие")


plt.legend()
plt.title("Распределение цены за билет у погибших и спасшихся пассажиров")
plt.show()




# 4
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
import matplotlib.pyplot as plt
import seaborn as sns
from random import choice

data = sns.load_dataset("titanic")
data = data.dropna()
data.head()

filt_data = data[(data['survived'] == 1) & (data['age'] <= 30)]

male_group = filt_data[filt_data['who'] == 'man']
female_group = filt_data[filt_data['who'] == 'woman']

male_survived_by_city = male_group.groupby('embark_town')['survived'].sum()
female_survived_by_city = female_group.groupby('embark_town')['survived'].sum()

male_city_max = male_survived_by_city.idxmax()
female_city_max = female_survived_by_city.idxmax()

print("Город, из которого спаслось больше мужчин не старше 30 лет:", male_city_max)
print("Город, из которого спаслось больше женщин не старше 30 лет:", female_city_max)