import pandas as pd
import matplotlib.pyplot as plt
from mplcursors import cursor

raw_edu = pd.read_csv('rawdata/raw_edu.csv')
raw_pop = pd.read_csv('rawdata/raw_pop.csv')
df = pd.DataFrame(columns=['country', 'students', 'population', 'relation', 'year'])

for year in range(1960, 2024):
    yearLit = str(year) + ' [YR' + str(year) + ']'
    yearData = []

    for index, row in raw_edu.iterrows():
        country = row['Country Name']
        population_row = raw_pop[raw_pop['Country Name'] == country]

        if population_row.empty:
            continue

        population = population_row.loc[population_row.index[0], yearLit]
        students = row[yearLit]

        if students == '..' or population == '..':
            continue

        population = int(float(population))
        students = int(float(students))

        if students == 0 or population == 0:
            continue

        yearData.append([country, students, population, (students / population) * 100, year])

    dYear = pd.DataFrame(yearData, columns=['country', 'students', 'population', 'relation', 'year'])
    df = dYear if df.empty else pd.concat([df, dYear], ignore_index=True, sort=False)


multi_cols = df[['country', 'year']]
df.index = pd.MultiIndex.from_tuples(multi_cols.values.tolist(), names=multi_cols.columns)
df.info()

print(df.loc['Armenia', :], "\n")
print(df.loc[('Armenia', 2005), :], "\n")

matrix = df[['students', 'population', 'relation']].corr()
print(matrix)

plt.imshow(matrix, cmap='seismic', interpolation='none', vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(matrix)), matrix.columns)
plt.yticks(range(len(matrix)), matrix.columns)

df.plot(kind='scatter', x='year', y='relation', stacked=False)
plt.title('all countries')

Armenia = df.loc['Armenia', :]
Armenia.plot(kind='scatter', x='year', y='relation', stacked=False)
plt.title('Armenia')

Russian = df.loc['Russian Federation', :]
Russian.plot(kind='scatter', x='year', y='relation', stacked=False)
plt.title('Russian')

Latvia = df.loc['Latvia', :]
Latvia.plot(kind='scatter', x='year', y='relation', stacked=False)
plt.title('Latvia')

Mexico = df.loc['Mexico', :]
Mexico.plot(kind='scatter', x='year', y='relation', stacked=False)
plt.title('Mexico')


cursor(hover=True)
plt.show()
