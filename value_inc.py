# -*- coding: utf-8 -*-
import pandas as pd

#loading up the data from the working path
value_data = pd.read_csv('transaction2.csv',delimiter=';')

#summary of the data
value_data.info()


#loading individual colum
cost_per_item = value_data['CostPerItem']
Selling_price= value_data['SellingPricePerItem']
Num_items= value_data['NumberOfItemsPurchased']

#testing
CostPerTransaction = cost_per_item * Num_items
SalesPerTransaction = Num_items * Selling_price
Profit = SalesPerTransaction - CostPerTransaction

#add new colum
value_data['CostPerTransaction'] = CostPerTransaction
value_data['SalesPerTransaction'] = SalesPerTransaction
value_data['ProfitPertransaction'] = value_data['SalesPerTransaction'] - value_data['CostPerTransaction']
value_data['Markup'] = (value_data['SalesPerTransaction'] - value_data['CostPerTransaction'])/value_data['CostPerTransaction']

#rounding up
value_data['Markup'] = round(value_data['Markup'],2)

#date
value_data['OrderdDate'] = pd.to_datetime(value_data['Year'].astype(str) + '-' + value_data['Month'].astype(str) + '-' + value_data['Day'].astype(str))
value_data['OrderdDate'] = value_data['OrderdDate'].dt.date

#spliting data
split_col= value_data['ClientKeywords'].str.split(',' , expand = True)

#creating a new coulmns from the split data
value_data['ClientAgeGroup'] = split_col[0]
value_data['ClientType'] = split_col[1]
value_data['ContractLenght'] = split_col[2]

#cleaning the new columns
value_data['ClientAgeGroup'] = value_data['ClientAgeGroup'].str.replace('[' , '')
value_data['ContractLenght'] = value_data['ContractLenght'].str.replace(']' , '')
value_data['ClientAgeGroup'] = value_data['ClientAgeGroup'].str.replace("'" , '')
value_data['ContractLenght'] = value_data['ContractLenght'].str.replace("'" , '')
value_data['ClientType'] = value_data['ClientType'].str.replace("'" , '')
#
value_data['ItemDescription'] = value_data['ItemDescription'].str.lower()

#join new data files

#loading the new data
value_data_season = pd.read_csv('value_inc_seasons.csv',delimiter=';')

#mergin data
value_data = pd.merge(value_data, value_data_season, on = 'Month')

#dropping old columns
value_data = value_data.drop('ClientKeywords', axis = 1)
value_data = value_data.drop('Day', axis = 1)
value_data = value_data.drop(['Year' , 'Month'], axis = 1)

#export
value_data.to_csv('Value_Inc_Cleaned.csv', index = False)