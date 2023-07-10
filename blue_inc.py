#loading libraries
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#path to file
json_file_path = 'loan_data_json.json'

# opening the file
with open(json_file_path, 'r') as file:
    bluebank_df = json.load(file)

#transfroming the json data into a data frame
loandata = pd.DataFrame(bluebank_df)

#infor about the data
loandata.info()
#finding the unique information of a colum
loandata['purpose'].unique()

#describe
loandata.describe()
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()

#using EXP() to get the annual income
income=np.exp(loandata['log.annual.inc'])
loandata['annualincome'] = income


#applying for loops to loan data to 

def categorize_fico(fico):
    if fico >= 300 and fico <= 399:
        ficocat = 'Very poor'
    elif fico >= 400 and fico < 599:
        ficocat = 'Poor'
    elif fico >= 600 and fico < 659:
        ficocat = 'Fair'
    elif fico >= 660 and fico < 779:
        ficocat = 'Good'
    elif fico >= 780:
        ficocat = 'Excellent'
    else:
        ficocat = 'Unknown'
    return ficocat

fico_categories = []

for fico in loandata['fico']:
    category = categorize_fico(fico)
    fico_categories.append(category)
loandata['Fico Category'] = fico_categories

#for intrest rates,
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'

#number of loan/rows by fico play with matplotlib
#bar graph
catplot = loandata.groupby(['Fico Category']).size()
catplot.plot.bar(color = 'red', width = 0.1)
plt.show()

purposeplot = loandata.groupby(['purpose']).size()
purposeplot.plot.bar(color = 'green')
plt.show()

#scatter plot
ypoint = loandata['annualincome']
xpoint = loandata['dti']
plt.scatter(xpoint,ypoint)
plt.show()

#writing to csv
loandata.to_csv('loan_cleaned.csv', index = True)

