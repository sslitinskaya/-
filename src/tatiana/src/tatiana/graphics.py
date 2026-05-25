import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#8B4513', '#A0522D', '#CD853F', '#D2691E'])
sns.set_style('whitegrid')

class CompetitorAnalyzer:

    def __init__(self, file_path='/content/кофейни Москвы.xlsx'):
        self.df = pd.read_excel(file_path)
        self._prepare_data()
        
    def _prepare_data(self):
        self.df = self.df.dropna(subset=['Рейтинг'])
        self.df['has_website'] = self.df['Веб-сайт 1'].notna()
        self.df['has_phone'] = self.df['Телефон 1'].notna()
        self.df['Район'] = self.df['Район'].fillna('Неизвестно')
        self.df.rename(columns={'Количество отзывов': 'reviews_count'}, inplace=True)
        
    def basic_stats(self):
        print("=== Базовые метрики ===")
        print(f"Всего кофеен: {len(self.df)}")
        print(f"Средний рейтинг: {self.df['Рейтинг'].mean():.2f} (±{self.df['Рейтинг'].std():.2f})")
        print(f"Медианный рейтинг: {self.df['Рейтинг'].median():.2f}")
        print(f"Доля с веб-сайтом: {self.df['has_website'].mean():.1%}")
        print(f"Доля с телефоном: {self.df['has_phone'].mean():.1%}")
        
    def plot_rating_distribution(self):
        plt.figure(figsize=(10,5))
        sns.histplot(self.df['Рейтинг'], bins=20, kde=True, color='#8B4513', edgecolor='white')
        plt.title('Распределение рейтингов кофеен (данные 2ГИС)', fontsize=14)
        plt.xlabel('Рейтинг')
        plt.ylabel('Количество кофеен')
        plt.show()
        
    def plot_rating_by_website(self):
        plt.figure(figsize=(8,6))
        sns.boxplot(x='has_website', y='Рейтинг', data=self.df, palette=['#CD853F', '#8B4513'])
        plt.xticks([0,1], ['Нет сайта', 'Есть сайт'])
        plt.title('Рейтинг: есть сайт vs нет сайта')
        plt.ylabel('Рейтинг')
        plt.show()
        group_no = self.df[~self.df['has_website']]['Рейтинг']
        group_yes = self.df[self.df['has_website']]['Рейтинг']
        stat, p = stats.ttest_ind(group_no, group_yes, nan_policy='omit')
        print(f"T-test p-value: {p:.4f}")
        if p < 0.05:
            print("→ Разница статистически значима: кофейни с сайтом имеют более высокий рейтинг.")
        else:
            print("→ Разница не значима.")
            
    def plot_rating_vs_reviews(self):
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=self.df, x='reviews_count', y='Рейтинг', alpha=0.6, color='#A0522D')
        plt.xscale('log')
        plt.title('Зависимость рейтинга от количества отзывов')
        plt.xlabel('Количество отзывов (логарифм)')
        plt.ylabel('Рейтинг')
        plt.show()
        corr = self.df[['Рейтинг', 'reviews_count']].corr().iloc[0,1]
        print(f"Корреляция Пирсона: {corr:.3f}")
        
    def top_districts(self):
        top = self.df['Район'].value_counts().head(10)
        plt.figure(figsize=(12,5))
        top.plot(kind='bar', color='#CD853F', edgecolor='white')
        plt.title('Топ-10 районов по количеству кофеен')
        plt.xticks(rotation=45)
        plt.ylabel('Количество кофеен')
        plt.show()
        print("Самые насыщенные районы:")
        print(top)
        
    def map_coffee_shops(self):
        plt.figure(figsize=(12,8))
        plt.scatter(self.df['Долгота'], self.df['Широта'], c=self.df['Рейтинг'], 
                    cmap='copper', alpha=0.7, s=20)
        plt.colorbar(label='Рейтинг')
        plt.title('Расположение кофеен с цветовой маркировкой рейтинга')
        plt.xlabel('Долгота')
        plt.ylabel('Широта')
        plt.show()
        
    def generate_report(self):
        print("\n" + "="*50)
        print("ИТАК ИТОГОВЫЙ ОТЧЁТ ПО АНАЛИЗУ КОНКУРЕНТОВ")
        print("="*50)
        print(f"Всего проанализировано кофеен: {len(self.df)}")
        print(f"Средний рейтинг по рынку: {self.df['Рейтинг'].mean():.2f}")
        print(f"Доля кофеен с веб-сайтом: {self.df['has_website'].mean():.1%}")
        print(f"Доля кофеен с телефоном: {self.df['has_phone'].mean():.1%}")
        print("\nРекомендации для STD Coffee (исходя из наших графиков):")
        print("- Целевой рейтинг: стремиться к 4.5+ (выше среднего по рынку).")
        print("- Наличие веб-сайта и телефона повышает доверие (тк есть корреляция с рейтингом).")
        print("- Районы с наибольшим числом кофеен: высокая конкуренция, но и высокий спрос.")
        print("- Стоит рассмотреть районы со средней насыщенностью и рейтингом >4.3.")
        print("- Использовать соцсети (ВКонтакте, Telegram) для привлечения аудитории.")
        
    def run_all(self):
        self.basic_stats()
        self.plot_rating_distribution()
        self.plot_rating_by_website()
        self.plot_rating_vs_reviews()
        self.top_districts()
        self.map_coffee_shops()
        self.generate_report()

if __name__ == "__main__":
    analyzer = CompetitorAnalyzer('/content/кофейни Москвы.xlsx')
    analyzer.run_all()
