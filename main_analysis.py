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
    with open("sinnes_2014_2025_med_makstemperatur.csv", "r", encoding='utf-8') as f:
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
                'maxtemp':
                    (float(line['Maksimumstemperatur (døgn)'].replace(',','.'))
                    if line['Maksimumstemperatur (døgn)'] not in ("-"," ","")
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


def fix_date_number (before_number):
    before_number = int(before_number)
    after_number = "0"
    if before_number < 10:
        after_number = "0" + str(before_number)
        return after_number
    else:
        after_number = str(before_number)
        return after_number

temporary_rain_counter =[]
longest_rainless_period = []

ammount_of_months = len(weather_data_this_year[entered_date])
for month in range(1,ammount_of_months+1):   
    
    month_counter = fix_date_number(month)
    ammount_of_days = len(weather_data_this_year[entered_date][month_counter])

    for day_counter in range(1,ammount_of_days+1):
        day_counter = fix_date_number(day_counter)
        try:
            if (weather_data_this_year[entered_date][month_counter][day_counter]['precip']) ==0:
                temporary_rain_counter.append(month_counter +"." + day_counter) 
            else:
                if len(temporary_rain_counter)>len(longest_rainless_period):
                    longest_rainless_period = temporary_rain_counter
                temporary_rain_counter = []
        except KeyError:
            print("Counld not find key")
            continue

print(f"The longest period with no downfall in {entered_date}")
print(f"it lasted for {len(longest_rainless_period)} days")
print(f"It lasted from: {longest_rainless_period[0]} to {longest_rainless_period[-1]}")

summerday = 0
high_summerday = 0
tropical_day = 0

for month in weather_data_this_year[entered_date]:
    month = fix_date_number(month)
    for day in (weather_data_this_year[entered_date][month]):
        day = fix_date_number(day)
        if weather_data_this_year[entered_date][month][day]['maxtemp'] >= 30:
            tropical_day += 1
            continue
        elif weather_data_this_year[entered_date][month][day]['maxtemp'] >= 25:
            high_summerday += 1
            continue
        elif weather_data_this_year[entered_date][month][day]['maxtemp'] >= 20:
            summerday += 1

print("=============================")
print(f"Days with max temerature over 20°: {summerday}")
print(f"Days with max temerature over 25°: {high_summerday}")
print(f"Days with max temerature over 30°: {tropical_day}")
print("=============================")


"""  ===============SKISEASON=============== """

try:
    skisesong_1 = chosen_year -1            #define lower bound
    skisesong_2 = chosen_year                   #define upper bound
except IndexError:
    pass

def skisesong():
    skisesong_1 = str(chosen_year - 1)
    skisesong_2 = str(chosen_year)
    k = 0
    b = 0
    

    if skisesong_1 in weather_data_this_year:
        for i in [11, 12]:
            month_str = fix_date_number(i)

            if month_str in weather_data_this_year[skisesong_1]:
                for n in weather_data_this_year[skisesong_1][month_str]:
                    if 20 <= float(weather_data_this_year[skisesong_1][month_str][n]['snow']):
                        k += 1
                        

    if skisesong_2 in weather_data_this_year:
        for j in range(1, 6):
            month_str = fix_date_number(j)
            if month_str in weather_data_this_year[skisesong_2]:
                for z in weather_data_this_year[skisesong_2][month_str]:
                    if 20 <= float(weather_data_this_year[skisesong_2][month_str][z]['snow']):
                        b += 1
                        
    return k + b

print("Number of days of ski-season: ", skisesong(),"\n")
