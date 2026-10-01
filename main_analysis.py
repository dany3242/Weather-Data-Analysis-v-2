import csv
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator



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

dates = []
temperatures = []
prescis = []
wind = []
snow = []

year_data = weather_data_this_year[str(chosen_year)]

for month in sorted(year_data, key=int):
    for day in sorted(year_data[month], key=int):
        measurements = year_data[month][day]

        dates.append(f"{day}/{month}")
        temperatures.append(measurements["temp"])
        prescis.append(measurements["precip"])
        wind.append(measurements["wind"])
        snow.append(measurements["snow"])

total_annual_growth = 0

for temp in temperatures:                
    if temp > 5:
        total_annual_growth += (temp - 5)
    else:
        continue

print("=============================")
print(f"Total growth: {(total_annual_growth):.2f}mm")
print("=============================")


plt.figure(figsize=(30, 30, "cm"))
plt.subplot(2,2,1)
plt.fill_between(dates, temperatures, color="green")
plt.grid()
plt.ylabel("Temperature")
plt.xlabel("Date")

plt.subplot(2,2,2)
plt.fill_between(dates, wind, color="lightblue")
plt.grid()
plt.ylabel("Wind")
plt.xlabel("Date")

plt.subplot(2,2,3)
plt.fill_between(dates, prescis)
plt.grid()
plt.ylabel("Percipitation")
plt.xlabel("Date")

plt.subplot(2,2,4)
plt.fill_between(dates, snow, color="lightgray")
plt.grid()
plt.ylabel("Snow")
plt.xlabel("Date")

for axis in plt.gcf().axes:
    axis.xaxis.set_major_locator(MaxNLocator(nbins=6))


"""
Graf til plante vekst, men trenger liste på linje 89 for å fungere hvis vi vil være fancy.

plt.style.use('dark_background')
plt.figure(figsize=(15, 5))
plt.title("Plants growth period", fontsize=20)
plt.fill_between(dates, total_annual_growth, color="lightgreen")
plt.ylabel("Plant growth")
plt.xlabel("Date")
"""

for axis in plt.gcf().axes:
    axis.xaxis.set_major_locator(MaxNLocator(nbins=12))

    
plt.show()