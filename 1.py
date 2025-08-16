import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""Задание 1"""
"""Генерируем данные"""
dates = pd.date_range(start="2024-01-01", periods=365, freq="D")
regions = np.random.choice(["Север", "Юг", "Запад", "Восток"], size=365)
clients = np.random.randint(1000, 2000, size=365)
sales = np.random.randint(10000, 20000, size=365)

df = pd.DataFrame({
    "Дата":dates,
    "Регион":regions,
    "Клиент":clients,
    "Сумма":sales
})

print(f"Общая выручка: {df['Сумма'].sum()}")
print(f"Средний чек: {df['Сумма'].mean()}")
print(f"Топ 2 регионов по продажам: {df.groupby('Регион')['Сумма'].sum().sort_values(ascending=False).head(2)}")

df["Дата"] = pd.to_datetime(df["Дата"])
df["Месяц"] = df["Дата"].dt.month
df_1 = df.groupby("Месяц")["Сумма"].sum()

df_1.plot(kind="line", marker="o", label="Динамика продаж по месяцам")
plt.ylabel("Сумма продаж")
plt.show()

df_2 = df.groupby("Регион")["Сумма"].sum()
plt.pie(df_2, labels=df_2.index, autopct="%1.1f%%")
plt.title("Распределение выручки по регионам")
plt.show()

mean_sum = df.groupby("Дата")["Сумма"].mean()
plt.hist(mean_sum, bins=20, color="red", edgecolor="black")
plt.title("Гистограмма среднего чека по дням")
plt.show()