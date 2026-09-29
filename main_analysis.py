import csv
from datetime import datetime
import matplotlib.pyplot as plt

while True:                                                        ### Getting and validating desired year 
    entered_date = input("Choose a year (2014 - 2025): ")
    if len(entered_date) == 4:
        try:
            chosen_year = int(entered_date)
            if chosen_year < 2014 or chosen_year > 2025:
                print("Year out of range")
                continue
            break
        except ValueError:
            print("Invalid data, try again")
            continue    
    else:
        continue


weather_data_this_year = {}             ### Dict for all the data from CSV-file


try:
    with open("sinnes_2014_2025.csv", "r", encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')

        for line in data:               ### Validating lines
            if (
                not line.get("Tid(norsk normaltid)")
                or "Data er gyldig" in line["Tid(norsk normaltid)"]
            ):
                continue

            parts = line['Tid(norsk normaltid)'].split('.')    ### Breaking dates into parts to save as nested dicts
            d = parts[0]
            m = parts[1]
            y = parts[2]

            if y not in weather_data_this_year:
                weather_data_this_year[y] = {}
            if m not in weather_data_this_year[y]:
                weather_data_this_year[y][m] = {}

            weather_data_this_year[y][m][d] = {             ### Formating and creating all values from the file to dict
                'temp':
                    (float(line['Middeltemperatur (døgn)'].replace(',','.'))
                    if line['Middeltemperatur (døgn)'] not in ("-", " ", "")
                    else 0.0),

                'precip':
                    (float(line['Nedbør (døgn)'].replace(',','.'))
                    if line['Nedbør (døgn)'] not in ("-", " ", "")
                    else 0.0),
                'wind':
                    (float(line['Høyeste middelvind (døgn)'].replace(',','.'))
                    if line['Høyeste middelvind (døgn)'] not in ("-", " ", "")
                    else 0.0),
                'snow':
                    (float(line['Snødybde'].replace(',','.'))
                    if line['Snødybde'] not in ("-", " ", "")
                    else 0.0),
            }
except FileNotFoundError:
    print("Could not find the file")
    exit()

summerday = 0
high_summerday = 0
tropical_day = 0

for month in weather_data_this_year[str(chosen_year)]:
    for day in (weather_data_this_year[str(chosen_year)][str(month)]):
        if weather_data_this_year[str(chosen_year)][str(month)][str(day)]['temp'] >= 30.0:
            tropical_day += 1
            continue
        elif weather_data_this_year[str(chosen_year)][str(month)][str(day)]['temp'] >= 25.0:
            high_summerday += 1
            continue
        elif weather_data_this_year[str(chosen_year)][str(month)][str(day)]['temp'] >= 20.0:
            summerday += 1

print("=============================")
print(f"Days over 20°: {summerday}")
print(f"Days over 25°: {high_summerday}")
print(f"Days over 30°: {tropical_day}")
print("=============================")



