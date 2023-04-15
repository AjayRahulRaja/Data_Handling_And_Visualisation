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
male.head()

# filtering female data
female = salary_per_town_categories_merge[salary_per_town_categories_merge['SEXE'] == 2]
female = female[['CODGEO', 'LIBGEO_left', 'SNHMFE14', 'SNHMFO14', 'SNHMF1814', 'SNHMH2614', 'SNHMF5014']]
female = female.rename(columns={'CODGEO':'CODGEO', 'LIBGEO_left':'LIBGEO', 'SNHMFE14':'net_salary_per_hour_employee', 'SNHMFO14':'net_salary_per_hour_worker', 'SNHMF1814':'net_salary_18_to_25', 'SNHMH2614':'net_salary_26_to_50' ,'SNHMF5014':'net_salary_more_than_50yrs'})
female = female.drop_duplicates()
female_top_10 = female.sort_values(['net_salary_per_hour_employee', 'net_salary_per_hour_worker'], ascending=False).head(10)
female.head()



# plotting the graphs
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

plt.style.use('ggplot')

fig = plt.figure(figsize=(55, 20))
grid = GridSpec(5, 8, wspace=0.05, hspace=0.325, left=0.1,
                bottom=0.1,
                right=0.9,
                top=0.9, figure=fig)

ax1 = fig.add_subplot(grid[0,0])
sns.kdeplot(male['net_salary_per_hour_worker'], shade=True, ax=ax1, label='Male')
sns.kdeplot(female['net_salary_per_hour_worker'], shade=True, ax=ax1, label='Female')
ax1.set(title='Gender wise density comparison of salary per hour (worker)')
ax1.title.set_size(13)
ax1.set_xlabel('Salary', fontsize=12)
ax1.set_ylabel('Density', fontsize=12)
plt.legend(fontsize=10)

ax2 = fig.add_subplot(grid[0,1])
plt.text(0.0, 0.6, f'\nThis graph shows the net salary of worker\nbetween different sexes and of all catagories of ages.\n\nThis graph shows the overall salary given to Men \nis greater than Women in France.')
ax2.axis('off')

ax3 = fig.add_subplot(grid[0,2])
sns.kdeplot(male['net_salary_per_hour_employee'], shade=True, ax=ax3, label='Male')
sns.kdeplot(female['net_salary_per_hour_employee'], shade=True, ax=ax3, label='Female')
ax3.set(title='Gender wise density comparison of salary per hour (employee)')
ax3.title.set_size(13)
ax3.set_xlabel('Salary', fontsize=12)
ax3.set_ylabel('Density', fontsize=12)
plt.legend(fontsize=10)

ax4 = fig.add_subplot(grid[0,3])
plt.text(0.0, 0.4, f'\nThis graph shows the Monthly salary of employees \nbetween different sexes and of all catagories of ages.\n\nBased on this graph we can understand\nthe overall salary earned by Women employees\nis greater than Men in France.\n\nComparing with the net salary of all workers, \nWomen as employee earning more than Male employees.')
ax4.axis('off')

ax5 = fig.add_subplot(grid[1,0])
sns.kdeplot(male['net_salary_18_to_25'], shade=True, ax=ax5, label='Men between 18 and 25')
sns.kdeplot(male['net_salary_26_to_50'], shade=True, ax=ax5, label='Men between 26 and 50')
sns.kdeplot(male['net_salary_more_than_50yrs'], shade=True, ax=ax5, label='Men more than 50 years')
ax5.set(title='Monthly salary for Men between different age ranges')
ax5.title.set_size(13)
ax5.set_xlabel('Salary', fontsize=12)
ax5.set_ylabel('Density', fontsize=12)
plt.legend(fontsize=10)

ax7 = fig.add_subplot(grid[1,1])
plt.text(0.0, 0.4, f'\nThis graph shows the monthly salary of Men\nbetween different sexes and of all catagories. \n\nThis graph shows the overall salary earned by \nMen around 18 and 25 earn \nrelatively more than Men aged more 50 years.')
ax7.axis('off')

ax6 = fig.add_subplot(grid[1,2])
sns.kdeplot(female['net_salary_18_to_25'], shade=True, ax=ax6, label='Women between 18 and 25')
sns.kdeplot(female['net_salary_26_to_50'], shade=True, ax=ax6, label='Women between 26 and 50')
sns.kdeplot(female['net_salary_more_than_50yrs'], shade=True, ax=ax6, label='Women more than 50 years')
ax6.set(title='Monthly salary for Women between different age ranges')
ax6.title.set_size(13)
ax6.set_xlabel('Salary', fontsize=12)
ax6.set_ylabel('Density', fontsize=12)
plt.legend(fontsize=10)

ax8 = fig.add_subplot(grid[1,3])
plt.text(0.0, 0.4, f'\nThis graph shows the monthly salary of Women\nbetween different sexes and of all catagories. \n\nThis graph shows the Women aged 18 and 25 years \nearn lesser than wommen agaed more than 50.\n\nBut larger number of women fall under the range \nbetween 18 and 25.')
ax8.axis('off')

ax9 = fig.add_subplot(grid[0,4])
male_top_10.plot(x='LIBGEO', kind='bar', stacked=False, ax=ax9)
plt.xlabel("Cities", fontsize=12)
plt.ylabel("Net Salary", fontsize=12)
ax9.set_xticklabels(ax9.get_xticklabels())
plt.title("Net Salary of Men over different ages in different cities")
ax9.title.set_size(13)
plt.legend(bbox_to_anchor=(1.015, 1.005), fontsize=10)

ax11 = fig.add_subplot(grid[0,5])
plt.text(0.0, 0.0, f'\nThis graph shows the net salary of employee\nbetween different sexes and of all catagories. \n\nThis graph shows the overall salary earned by \nWomen is greater than Men in France. \n\nComparing with the net salary of all sexes, \nWomen as employee earning more than Men.')
ax11.axis('off')

ax10 = fig.add_subplot(grid[2,4])
female_top_10.plot(x='LIBGEO', kind='bar', stacked=False, ax=ax10)
plt.xlabel("Cities", fontsize=12)
plt.ylabel("Net Salary", fontsize=12)
plt.title("Net Salary of Women over different ages in different cities")
ax10.set_xticklabels(ax10.get_xticklabels())
ax10.title.set_size(13)
plt.legend(bbox_to_anchor=(1.015, 1.005), fontsize=10)

ax12 = fig.add_subplot(grid[2,5])
plt.text(0.0, 0, f'\nThis graph shows the net salary of employee\nbetween different sexes and of all catagories. \n\nThis graph shows the overall salary earned by \nWomen is greater than Men in France. \n\nComparing with the net salary of all sexes, \nWomen as employee earning more than Men.')
ax12.axis('off')

ax16 = fig.add_subplot(grid[1,4])
plt.text(0.0, 0, ' ')
ax16.axis('off')

ax13 = fig.add_subplot(grid[2,0])
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
ax13.set(xlim=(0, 50))
ax13.set_title("15 Cities in France with the Highest Percentage Wage Gap", fontsize=13)
ax13.set_ylabel("Cities", fontsize=12)
ax13.set_xlabel("Percentage Wage Gap", fontsize=12)
plt.legend(bbox_to_anchor=(1.015, 1.005), fontsize=10)

ax14 = fig.add_subplot(grid[2,1])
plt.text(0.0, 0, f'\nThis graph shows the wage gap in all the cities in France.\nThe cities are named from 0 to 5000.\nEach number represents a city.')
ax14.axis('off')

ax15 = fig.add_subplot(grid[2,2])
plt.plot(wage_vs_gap, label=('Mean Wages', 'Wage Gap'))
plt.legend()
ax15.set_title("Wage gap in all cities in France", fontsize=13)
ax15.set_ylabel("Hourly wage gap", fontsize=12)
ax15.set_xlabel('Cities', fontsize=12)

ax15 = fig.add_subplot(grid[2,3])
plt.text(0.0, 0.6, f'\nThis graph shows the wage gap in all the cities in France.\nThe cities are named from 0 to 5000.\nEach number represents a city.')
ax15.axis('off')
