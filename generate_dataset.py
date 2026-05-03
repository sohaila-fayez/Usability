import pandas as pd
import random

cities = [
    "Berlin", "Paris", "London", "Madrid", "Rome", "Vienna", "Zurich",
    "Amsterdam", "Stockholm", "Oslo", "Copenhagen", "Prague", "Warsaw",
    "Budapest", "Lisbon", "Dublin", "Brussels", "Helsinki", "Athens"
]

data = []

for i in range(1000):
    city = random.choice(cities)
    rent_index = round(random.uniform(20, 120), 2)
    safety_index = round(random.uniform(30, 90), 2)
    cost_of_living = round(random.uniform(30, 100), 2)
    purchasing_power = round(random.uniform(40, 130), 2)

    quality_of_life = round(
        (purchasing_power * 0.4 + safety_index * 0.3 - rent_index * 0.2 - cost_of_living * 0.1),
        2
    )

    data.append([
        city, rent_index, safety_index,
        cost_of_living, purchasing_power, quality_of_life
    ])

df = pd.DataFrame(data, columns=[
    "City", "Rent_Index", "Safety_Index",
    "Cost_of_Living", "Purchasing_Power", "Quality_of_Life"
])

df.to_csv("city_quality.csv", index=False)

print("CSV mit 1000 Einträgen erstellt!")