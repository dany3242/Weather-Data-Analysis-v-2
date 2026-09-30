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

#tar en "0" forran måneder og datoer som er ensiffrede
def fix_date_number (before_number):
    after_number = "0"
    if before_number < 10:
        after_number = "0" + str(before_number)
        return after_number
    else:
        after_number = str(before_number)
        return after_number

#det er disse som skal måles mot hverandre for å finne lengste oppholdsperiode
temporary_rain_counter =[]
longest_rainless_period = []


ammount_of_months = len(weather_data_this_year[entered_date])
for month in range(1,ammount_of_months+1):   
    
    month_counter = fix_date_number(month)
    ammount_of_days = len(weather_data_this_year[entered_date][month_counter])

    for day_counter in range(1,ammount_of_days+1):

        day_counter = fix_date_number(day_counter)

        try:
            #legger til datoer til midlertidig liste om det ikke regner den dagen
            if (weather_data_this_year[entered_date][month_counter][day_counter]['precip']) ==0:
                temporary_rain_counter.append(month_counter +"." + day_counter) 
            #hvis det regner en dag sammenlignes den forrige lengste perioden med nåværende. Den lengste forblir og temp.raincouter blir satt=[]
            else:
                if len(temporary_rain_counter)>len(longest_rainless_period):
                    longest_rainless_period = temporary_rain_counter
                temporary_rain_counter = []
        except KeyError:
            print("det skejdde en feil i lesingen av regndata")
            continue


print(f"den lengste regnløse perioden i {entered_date} varte i {len(longest_rainless_period)} dagern\n Den varte fra: {longest_rainless_period[0]} til {longest_rainless_period[-1]}")

#print("Data for 15/04/2022: ")
#print(weather_data_this_year['2022']['04']['15'])
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


"""  ===============SKISEASON=============== """

try:
    skisesong_1 = chosen_year -1            #define lower bound
    skisesong_2 = chosen_year                   #define upper bound
except IndexError:
    pass


def counter(i):
    """

    :rtype: str
    """
    if i <= 9:
        i = str(0) + str(i)
    else:
        i = str(int(i)*10)[0] + str(i)[1]
    return i


list1 = []
list2 = []



def skisesong():
    skisesong_1 = chosen_year -1
    skisesong_2 = chosen_year
    i = 11; j = 1
    k = 0; b = 0
    for m in weather_data_this_year:
        try:
            for n in weather_data_this_year[f'{skisesong_1}'][f'{counter(i)}']:
                list1.append(weather_data_this_year[f'{skisesong_1}'][f'{counter(i)}'][n]['snow'])
                if 20 <= int(weather_data_this_year[f'{skisesong_1}'][f'{counter(i)}'][n]['snow']):
                 k+=1
            i += 1
            if i == 13:
                break
        except KeyError:
            continue

    for a in weather_data_this_year:
        for z in weather_data_this_year[f'{skisesong_2}'][f'{counter(j)}']:
            if 20 <= int(weather_data_this_year[f'{skisesong_2}'][f'{counter(j)}'][z]['snow']):
                b += 1
        j += 1
        if j == 6:
            break
    return k+b


print("Number of days of ski-season: ", skisesong(),"\n")
