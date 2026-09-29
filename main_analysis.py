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


weather_data_this_year = {}


try:
    with open("sinnes_2014_2025.csv", "r", encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for line in data:

            if (
                not line.get("Tid(norsk normaltid)")
                or "Data er gyldig" in line["Tid(norsk normaltid)"]
            ):
                continue

            parts = line['Tid(norsk normaltid)'].split('.')
            d = parts[0]
            m = parts[1]
            y = parts[2]

            if y not in weather_data_this_year:
                weather_data_this_year[y] = {}
            if m not in weather_data_this_year[y]:
                weather_data_this_year[y][m] = {}

            weather_data_this_year[y][m][d] = {
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



