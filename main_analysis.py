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


raw_temperature = []            ### Lists for future values from dataset
raw_precipitation = []
raw_wind = []
raw_snow_depth = []
raw_date = []


try:
    with open("sinnes_2014_2025.csv", "r", encoding='utf-8') as f:      ### Opening, reading and cofirming existence of given CSV file 
        data = csv.DictReader(f, delimiter=";")


        for line in data:                                              ### Iterating through dataset and saving needed values to lists
            if str(chosen_year) in line['Tid(norsk normaltid)']:
                raw_temperature.append(line['Middeltemperatur (døgn)'])
                raw_precipitation.append(line['Nedbør (døgn)'])
                raw_wind.append(line['Høyeste middelvind (døgn)'])
                raw_snow_depth.append(line['Snødybde'])
                raw_date.append(datetime.strptime(line['Tid(norsk normaltid)'], "%d.%m.%Y").astimezone())    ### Got all the info for the given year


except FileNotFoundError:
    print("Could not find the file")

