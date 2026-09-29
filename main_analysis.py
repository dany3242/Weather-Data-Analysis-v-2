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


weather_data_this_year = {}


try:
    with open("sinnes_2014_2025.csv", "r", encoding='utf-8') as f:
        data = csv.DictReader(f, delimiter=';')
        for line in data:                                                       # linje for linje

            if (
                not line.get("Tid(norsk normaltid)")                             
                or "Data er gyldig" in line["Tid(norsk normaltid)"]             # denne if-en sjekker om
            ):                                                                  # verdien i tid kolonnen kvalifiserer?
                continue

            parts = line['Tid(norsk normaltid)'].split('.')                     # wow kult
            d = parts[0]
            m = parts[1]
            y = parts[2]

            if y not in weather_data_this_year:                                 # hva gjør denne?
                weather_data_this_year[y] = {}
            if m not in weather_data_this_year[y]:                              # ..og denne?
                weather_data_this_year[y][m] = {}

            weather_data_this_year[y][m][d] = {
                'temp':
                    (float(line['Middeltemperatur (døgn)'].replace(',','.'))    # her floater du strengen fra csv filen,
                    if line['Middeltemperatur (døgn)'] not in ("-", " ", "")    # endrer ',' til '.'
                    else 0.0),                                                  # men hva skjekker denne? virket bakvendt 
                                                                                # logisk for meg sånn som d står XD
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

print("Data for 15/04/2022: ")
print(weather_data_this_year['2022']['04']['15'])

datoer = []
temperaturer = []
nedbør = []
vind = []
snø = []

year_data = weather_data_this_year[str(chosen_year)]

for month in sorted(year_data, key=int):
    for day in sorted(year_data[month], key=int):
        measurements = year_data[month][day]

        datoer.append(f"{day}/{month}")
        temperaturer.append(measurements["temp"])
        nedbør.append(measurements["precip"])
        vind.append(measurements["wind"])
        snø.append(measurements["snow"])

total_årlig_vekst = []

for temp in temperaturer:                
    if temp > 5:
        total_årlig_vekst.append(temp - 5)
    else:
        total_årlig_vekst.append(0)


plt.figure(figsize=(15, 5, "cm"))
plt.subplot(2,2,1)
plt.fill_between(datoer, temperaturer, color="green")
plt.grid()
plt.ylabel("Temp")
plt.xlabel("Dato")

plt.subplot(2,2,2)
plt.fill_between(datoer, vind, color="lightblue")
plt.ylabel("Vindstyrke")
plt.xlabel("Dato")

plt.subplot(2,2,3)
plt.fill_between(datoer, nedbør)
plt.ylabel("Nedbør")
plt.xlabel("Dato")

plt.subplot(2,2,4)
plt.fill_between(datoer, snø, color="lightgray")
plt.grid()
plt.ylabel("Snømengde")
plt.xlabel("Dato")

for axis in plt.gcf().axes:
    axis.xaxis.set_major_locator(MaxNLocator(nbins=6))

plt.style.use('dark_background')
plt.figure(figsize=(15, 5))
plt.title("Når på året plantene faktisk vokser", fontsize=20)
plt.fill_between(datoer, total_årlig_vekst, color="lightgreen")
plt.ylabel("Total plantevekst ")
plt.xlabel("Dato")

for axis in plt.gcf().axes:
    axis.xaxis.set_major_locator(MaxNLocator(nbins=12))

    
plt.show()