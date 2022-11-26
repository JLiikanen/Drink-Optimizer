import pandas as pd

#create DataFrame
df = pd.DataFrame({'team': ['A', 'A', 'A', 'B', 'B', 'C', 'C', 'D'],
                   'points': [5, 7, 7, 9, 12, 9, 9, 4],
                   'rebounds': [11, 8, 10, 6, 6, 5, 9, 12]})

print(df)
print(df.index)
print(df[df["points"] == 9])
