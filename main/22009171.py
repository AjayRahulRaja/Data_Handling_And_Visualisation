# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 14:14:08 2023

@author: Ajay
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#reading source data
population = pd.read_csv("C:/Users/Lenovo/Desktop/UK/Hertfordshire/SEM 01/Data Handling and Visualisation/infographics/Dataset/French Employment, salary, population/population.csv")
salary_per_town_categories = pd.read_csv("C:/Users/Lenovo/Desktop/UK/Hertfordshire/SEM 01/Data Handling and Visualisation/infographics/Dataset/French Employment, salary, population/net_salary_per_town_categories.csv")
name_geographic_information = pd.read_csv("C:/Users/Lenovo/Desktop/UK/Hertfordshire/SEM 01/Data Handling and Visualisation/infographics/Dataset/French Employment, salary, population/name_geographic_information.csv")
base_establissement_pre_tranche = pd.read_csv("C:/Users/Lenovo/Desktop/UK/Hertfordshire/SEM 01/Data Handling and Visualisation/infographics/Dataset/French Employment, salary, population/base_etablissement_par_tranche_effectif.csv")

#checking source data
population['CODGEO'].unique()
salary_per_town_categories.head()
salary_per_town_categories['CODGEO'].apply(lambda x: str(x).isdigit())

# salary_per_town_categories['CODGEO'] = salary_per_town_categories['CODGEO'].str.slice(1)
# the CODGEO column has the code for cities and towns in salary_per_town_categories dataframe. There are some codes begin with '0' and it is needed to be removed.
for x, val in enumerate(salary_per_town_categories['CODGEO']):
    if val[0] == '0':
        salary_per_town_categories.loc[x, 'CODGEO'] = val[1:]
    else:
        salary_per_town_categories['CODGEO']
salary_per_town_categories

#checking if the converted CODGEO value corresponds with different table
name_geographic_information[name_geographic_information['code_insee'] == 1024]

# CODGEO beginning value removal for base_establissement_pre_tranche dataframe.
for x, val in enumerate(base_establissement_pre_tranche['CODGEO']):
    if val[0] == '0':
        base_establissement_pre_tranche.loc[x, 'CODGEO'] = val[1:]
    else:
        base_establissement_pre_tranche['CODGEO']

    # merging two dataframes on 'CODGEO'
salary_per_town_categories_merge = salary_per_town_categories.merge(population, left_on='CODGEO', right_on='CODGEO', how='inner', suffixes= ('_left', '_right'))

# filtering male data
male = salary_per_town_categories_merge[salary_per_town_categories_merge['SEXE'] == 1]
male = male[['CODGEO', 'LIBGEO_left', 'SNHME14', 'SNHMO14', 'SNHM1814', 'SNHM2614', 'SNHMH5014']]
male = male.rename(columns={'CODGEO':'CODGEO', 'LIBGEO_left':'LIBGEO', 'SNHME14':'net_salary_per_hour_employee', 'SNHMO14':'net_salary_per_hour_worker', 'SNHM1814':'net_salary_18_to_25', 'SNHM2614':'net_salary_26_to_50' ,'SNHMH5014':'net_salary_more_than_50yrs'})
male = male.drop_duplicates()
male_top_10 = male.sort_values(['net_salary_per_hour_employee', 'net_salary_per_hour_worker'], ascending=False).head(10)

# filtering female data
female = salary_per_town_categories_merge[salary_per_town_categories_merge['SEXE'] == 2]
female = female[['CODGEO', 'LIBGEO_left', 'SNHMFE14', 'SNHMFO14', 'SNHMF1814', 'SNHMH2614', 'SNHMF5014']]
female = female.rename(columns={'CODGEO':'CODGEO', 'LIBGEO_left':'LIBGEO', 'SNHMFE14':'net_salary_per_hour_employee', 'SNHMFO14':'net_salary_per_hour_worker', 'SNHMF1814':'net_salary_18_to_25', 'SNHMH2614':'net_salary_26_to_50' ,'SNHMF5014':'net_salary_more_than_50yrs'})
female = female.drop_duplicates()
female_top_10 = female.sort_values(['net_salary_per_hour_employee', 'net_salary_per_hour_worker'], ascending=False).head(10)

expensive_cities = salary_per_town_categories[salary_per_town_categories['SNHM14'] >= 22]
expensive_cities_1 = expensive_cities[['LIBGEO', 'SNHM14']]
expensive_cities_2 = expensive_cities_1.sort_values('SNHM14', ascending=False).head(10)

pas_cher_cities = salary_per_town_categories[salary_per_town_categories['SNHM14'] <= 22]
pas_cher_cities_1 = pas_cher_cities[['LIBGEO', 'SNHM14']]
pas_cher_cities_2 = pas_cher_cities_1.sort_values('SNHM14', ascending=False)
pas_cher_cities_3 = pas_cher_cities_2.drop_duplicates('SNHM14').head(10)

distance = name_geographic_information[['code_insee','éloignement']]
dtype = {'CODGEO':int}
expensive_cities=expensive_cities.astype(dtype)

distance_pd_merged = pd.merge(expensive_cities, distance, how='left', left_on='CODGEO', right_on='code_insee')

expensive_cities = salary_per_town_categories[salary_per_town_categories['SNHM14'] >= 22]
expensive_cities_1 = expensive_cities[['LIBGEO', 'SNHM14']]
expensive_cities_2 = expensive_cities_1.sort_values('SNHM14', ascending=False).head(10)

pas_cher_cities = salary_per_town_categories[salary_per_town_categories['SNHM14'] <= 22]
pas_cher_cities_1 = pas_cher_cities[['CODGEO','LIBGEO', 'SNHM14']]
pas_cher_cities_2 = pas_cher_cities_1.sort_values('SNHM14', ascending=False)
pas_cher_cities_3 = pas_cher_cities_2.drop_duplicates('SNHM14').head(10)

distance = name_geographic_information[['code_insee','éloignement']]
dtype = {'CODGEO':int}
expensive_cities=expensive_cities.astype(dtype)

# distance_pd_merged = pd.merge(expensive_cities, distance, how='left', left_on='CODGEO', right_on='code_insee')
expensive_distance_pd_merged = pd.merge(expensive_cities, distance, how='left', left_on='CODGEO', right_on='code_insee')
expensive_distance_pd_merged[['LIBGEO', 'SNHM14', 'éloignement']].sort_values('SNHM14', ascending=False)
expensive_distance_pd_merged = expensive_distance_pd_merged[expensive_distance_pd_merged['LIBGEO'].isin(expensive_cities_2['LIBGEO'].values)]
expensive_distance_pd_merged[['CODGEO','LIBGEO', 'SNHM14', 'éloignement']]

dtype = {'CODGEO':int}
pas_cher_cities_3=pas_cher_cities_3.astype(dtype)

pas_cher_distance_pd_merged = pd.merge(pas_cher_cities_3, distance, how='left', left_on='CODGEO', right_on='code_insee')
pas_cher_distance_pd_merged[['LIBGEO', 'SNHM14', 'éloignement']].sort_values('SNHM14', ascending=False)

pas_cher_distance_pd_merged = pd.merge(pas_cher_cities_3, distance, how='left', left_on='CODGEO', right_on='code_insee')
pas_cher_distance_pd_merged[['LIBGEO', 'SNHM14', 'éloignement']].sort_values('SNHM14', ascending=False)

# plotting the graphs
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

plt.style.use('ggplot')

fig = plt.figure(figsize=(27, 18))

grid = GridSpec(4, 4, wspace=0.325, hspace=0.30, figure=fig)

ax1 = fig.add_subplot(grid[0, 0:3])
plt.text(0.98, 0.95, "Name: Ajay Rahul Raja", fontsize=15, fontweight="bold")
plt.text(0.98, 0.85, "Student ID: 22009171", fontsize=15, fontweight="bold")
plt.text(0.15, 0.55, "Data Handling and Visualisation - Infographics Project", fontsize=30, fontweight="bold")
plt.text(0.25, 0.25, "Which city is the best to choose in France?", fontsize=25, fontweight="bold")
plt.axis("off")

ax2 = fig.add_subplot(grid[1:3, 0:2])
salary_per_town_categories['wage_gap'] = salary_per_town_categories['SNHMH14'] - salary_per_town_categories['SNHMF14']
wage_vs_gap = pd.DataFrame({'Mean Wages':salary_per_town_categories['SNHM14'],
                            'Wage Gap':salary_per_town_categories['wage_gap']})
salary_per_town_categories['percentage_wage_gap'] = (salary_per_town_categories['wage_gap'] / salary_per_town_categories['SNHM14']) * 100

salary_per_town_categories.loc[salary_per_town_categories['percentage_wage_gap'] <= 0]
salary_data=salary_per_town_categories.sort_values(by=['percentage_wage_gap'], ascending=False).head(15)
sns.set_color_codes("pastel")
sns.barplot(x='SNHM14', y='LIBGEO', data=salary_data,
            label="Mean Wage", color="b")
sns.set_color_codes("muted")
sns.barplot(x='wage_gap', y='LIBGEO', data=salary_data,
            label="Wage Gap", color="b")
ax2.set(xlim=(0, 50))
ax2.set_title("15 Cities in France with the Highest Percentage Wage Gap", fontsize=13)
ax2.set_ylabel("Cities", fontsize=12)
ax2.set_xlabel("Percentage Wage Gap", fontsize=12)
plt.legend(bbox_to_anchor=(0.99, 0.091), fontsize=10)

ax3 = fig.add_subplot(grid[3, 0])
expensive_distance_pd_merged=expensive_distance_pd_merged.sort_values("SNHM14")
# Plotting the first data series on the left axis
plot_1 = ax3.plot(expensive_cities_2['LIBGEO'], expensive_cities_2['SNHM14'], label="Expensive cities")
plt.xticks(rotation=90)
ax3.set_xlabel('cities')
ax3.set_ylabel('net mean salary', color='red')

# Creating the second axis on the right side
ax31 = ax3.twinx()

# Plottting the second data series on the right axis
plot_2 = ax31.plot(expensive_distance_pd_merged['LIBGEO'], expensive_distance_pd_merged['éloignement'], label="Distance from Paris", color='blue')
ax31.set_ylabel('Distance', color='blue')
plt.xticks(rotation=90)
plt.legend()

plts = plot_1 + plot_2
labels = [x.get_label() for x in plts]
ax3.set(title="Less expensive cities than Paris")
ax3.title.set_size(10)
plt.legend(plts, labels, loc=0)

ax4 = fig.add_subplot(grid[3, 1])
sns.kdeplot(male['net_salary_per_hour_worker'], shade=True, ax=ax4, label='Male')
sns.kdeplot(female['net_salary_per_hour_worker'], shade=True, ax=ax4, label='Female')
ax4.set(title='Gender wise density comparison of salary per hour (worker)')
ax4.title.set_size(10)
ax4.set_xlabel('Salary', fontsize=12)
ax4.set_ylabel('Density', fontsize=12)
plt.legend(fontsize=10)

ax5 = fig.add_subplot(grid[3, 2])
female_top_10.plot(x='LIBGEO', kind='bar', stacked=False, ax=ax5)
plt.xlabel("Cities", fontsize=12)
plt.xticks(rotation=90)
plt.ylabel("Net Salary", fontsize=12)
plt.title("Net Salary of Women over different ages in different cities")
ax5.set_xticklabels(ax3.get_xticklabels())
ax5.title.set_size(10)
plt.legend(bbox_to_anchor=(1.015, 1.005), fontsize=10)

ax6 = fig.add_subplot(grid[1, 2])
plt.text(0, 0.13, "To find out which city is most suitable to live in France\nbased on the wages and cost of living.\n\nWe can infer from the analysis that Men are still earning\nmore than Women in most of the cities.\n\nParis is the captial of France and there are cities \nexpensive than paris like Croissy-sur-Seine and\ncheapest is Lamorlaye.\n\nWe can also see how many firms are ther in Paris\nwhich are actively functioning with how many employees.", fontsize=15)
ax6.axis('off')

ax7 = fig.add_subplot(grid[2, 2])
base_establissement_pre_tranche = base_establissement_pre_tranche[['LIBGEO', 'E14TS1' ,'E14TS6', 'E14TS10', 'E14TS20', 'E14TS50' ,'E14TS100', 'E14TS200', 'E14TS500']]
paris = base_establissement_pre_tranche[base_establissement_pre_tranche['LIBGEO'] == 'Paris']
paris = paris.rename(columns={'E14TS1':"More than 1 employees",
                              'E14TS6':"More than 6 employees",
                              'E14TS10':"More than 10 employees",
                              'E14TS20':"More than 20 employees",
                              'E14TS50':"More than 50 employees",
                              'E14TS100':"More than 100 employees",
                              "E14TS200":"More than 200 employees",
                              "E14TS500":"More than 500 employees"})
paris["employees betweeen 1 to 20"] = paris["More than 20 employees"]+paris["More than 10 employees"]+paris["More than 6 employees"]+paris["More than 1 employees"]
paris = paris.drop(columns=["More than 20 employees", "More than 10 employees", "More than 6 employees", "More than 1 employees"])
paris = paris.set_index("LIBGEO")
paris_values = [180, 456, 812, 1658]
plt.pie(paris_values, autopct="%1.1f%%", labels=None, shadow=True, startangle=90)
ax7.set_title("Percentage of firms in Paris \nclassified on the basis of number of employees", fontsize=13)
plt.legend(labels=["More than 500 employees", "More than 200 employees", "More than 100 employees", "employees more than 50"], bbox_to_anchor=(1.05, 0.75), fontsize=10)

plt.show()
