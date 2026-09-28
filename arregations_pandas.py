import pandas as pd

# aggregate functions = reduces a set of values into a simnle summary value
#                       used to summarize and analyze data
#                       Often used with groupby() function


df = pd.read_csv('titanic.csv', index_col='Name')

#mask_min_fare = df['Fare'] == df['Fare'].min()
#mask_avg_price = df['Fare'].mean()
# numeric_only summirizes only columns containing int or float 
#print(df.mean(numeric_only=True))
#print((df['Survived'] == 1).sum())
# if there's no [] in df, pandas will give out info about every single column

# groupby sorts rows depending on value specified in brackets
# then, among the both groups we find their average fare cost

group = df.groupby('Survived')

print(group['Fare'].mean())

