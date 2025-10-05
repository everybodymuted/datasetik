import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных с локального файла

data = pd.read_csv(r'C:\Users\golivuud\Desktop\запрет1212\торпеда\datasetik\processed_csgo_players_selected.csv')

print(data.head())
print(data.columns)

# Разведочный анализ (EDA)
print(data.info())
print(data.describe())

# Визуализация распределения рейтинга игроков
plt.figure(figsize=(10,6))
sns.histplot(data['rating'].dropna(), bins=30, kde=True)
plt.title('Распределение рейтинга профессиональных игроков CS:GO')
plt.xlabel('Рейтинг')
plt.ylabel('Количество игроков')
plt.show()

# Визуализация зависимости K/D Ratio и Impact
plt.figure(figsize=(10,6))
sns.scatterplot(x='kd_ratio', y='impact', data=data)
plt.title('Зависимость K/D Ratio от Impact')
plt.xlabel('K/D Ratio')
plt.ylabel('Impact')
plt.show()

# Предобработка данных
# Проверка на пропуски
print(data.isnull().sum())

# Для простоты заполнение пропусков в числовых столбцах медианой
num_cols = ['maps_played', 'rounds_played', 'kd_difference', 'kd_ratio', 'rating', 
            'total_kills', 'headshot_percentage', 'total_deaths', 'grenade_damage_per_round', 
            'kills_per_round', 'assists_per_round', 'deaths_per_round', 
            'teammate_saved_per_round', 'saved_by_teammate_per_round', 'kast', 'impact']

for col in num_cols:
    if col in data.columns:
        data[col] = data[col].fillna(data[col].median())

# Конструирование признаков
# Например, создадим признак эффективности: kills_per_round / deaths_per_round (где deaths_per_round > 0)
data['efficiency'] = data.apply(lambda row: row['kills_per_round'] / row['deaths_per_round'] 
                               if row['deaths_per_round'] > 0 else 0, axis=1)

# Отбор признаков для анализа
features = num_cols + ['efficiency']
data_selected = data[features]

print(data_selected.head())

# Сохраняем подготовленные данные
data_selected.to_csv('processed_csgo_players_selected.csv', index=False)