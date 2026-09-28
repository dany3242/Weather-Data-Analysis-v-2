import csv
from datetime import datetime
import matplotlib.pyplot as plt

while True:
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


with open("sinnes_2014_2025.csv", "r", encoding='utf-8') as f:
    df = csv.DictReader(f, delimiter=";")

    for line in df:
        if str(chosen_year) in line['Tid(norsk normaltid)']:
            print(line['Middeltemperatur (døgn)'])




"""
chosen_date = datetime.strptime(entered_date, '%d.%m.%Y')
chosen_date = datetime.date(chosen_date)
            """