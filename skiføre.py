

from main_analysis import chosen_year
from main_analysis import weather_data_this_year

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





















#skriv in et år, ta ifjor [11] til og med i år [05]
#hvis of bare hvis 20cm <= snødybde, i +=1
#til slutt returnerer du i
