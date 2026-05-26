import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

def load_data():
    info_url = 'https://code.s3.yandex.net/datasets/rest_info.csv'
    price_url = 'https://code.s3.yandex.net/datasets/rest_price.csv'
    
    info = pd.read_csv(info_url)
    price = pd.read_csv(price_url)
    return info, price

rest_info, rest_price = load_data()
print("Данные успешно загружены!")

merged_df = rest_info.merge(rest_price, on='id')

coffee_places = merged_df[merged_df['category'] == 'кофейня'].copy()
print(f"Найдено кофеен: {len(coffee_places)}")
print(f"Доступные районы: {coffee_places['district'].unique()}")


chain_ratings = coffee_places[coffee_places['chain'] == 1]['rating'].dropna()
non_chain_ratings = coffee_places[coffee_places['chain'] == 0]['rating'].dropna()
t_stat, p_value = stats.ttest_ind(chain_ratings, non_chain_ratings, nan_policy='omit')
print("Анализ рейтинга: Сетевые and Несетевые")
print(f"Средний рейтинг сетевых: {chain_ratings.mean():.3f}")
print(f"Средний рейтинг несетевых: {non_chain_ratings.mean():.3f}")
print(f"T-тест p-value: {p_value:.3f}")
if p_value < 0.05:
    print("Вывод: Статистически значимая разница в рейтингах существует")
else:
    print("Вывод: Статистически значимой разницы в рейтингах не обнаружено")

district_analysis = coffee_places.groupby('district').agg(
    total_coffee_shops=('id', 'count'),
    chain_coffee_shops=('chain', 'sum'),
    non_chain_coffee_shops=('chain', lambda x: (x == 0).sum())
).reset_index()

print("\Анализ по административным округам")
print(district_analysis.head())

coffee_places.sample(500)[['name', 'address', 'rating', 'chain', 'price']]

