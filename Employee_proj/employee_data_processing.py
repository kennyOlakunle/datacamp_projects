import pandas as pd
import numpy as np
# Start coding here... 

# Read in the datasets
office_addresses = pd.read_csv('datasets/office_addresses.csv')
employee_addresses = pd.read_excel('datasets/employee_information.xlsx', sheet_name='employee_addresses')
emergency_contacts = pd.read_excel('datasets/employee_information.xlsx', sheet_name='emergency_contacts', header=None)
emergency_contacts.columns = ['employee_id', 'last_name', 'first_name', 'emergency_contact', 'emergency_contact_number', 'relationship']
with open('datasets/employee_roles.json', 'r') as file:
    employee_roles = pd.read_json(file).transpose()
    
# Replace NaN values in columns starting with 'office' with the word 'Remote'
office_addresses.fillna({'office': 'Remote'}, inplace=True)

merged_df = pd.merge(employee_addresses, emergency_contacts, on='employee_id', how='outer')
merged_df = pd.merge(merged_df, office_addresses, how='left', left_on='employee_country', right_on='office_country')
employees_final = pd.merge(merged_df, employee_roles, left_on='employee_id', right_index=True, how='outer')

# Set the index to 'employee_id' and retain the specified columns
employees_final.set_index('employee_id', inplace=True)
final_columns = [
    'employee_first_name', 'employee_last_name', 'employee_country', 'employee_city', 
    'employee_street', 'employee_street_number', 'emergency_contact', 'emergency_contact_number', 
    'relationship', 'monthly_salary', 'team', 'title', 'office', 'office_country', 
    'office_city', 'office_street', 'office_street_number'
]
employees_final = employees_final[final_columns]

# Rename columns for clarity
employees_final.columns = [
    'first_name', 'last_name', 'employee_country', 'employee_city', 'employee_street', 
    'employee_street_number', 'emergency_contact', 'emergency_contact_number', 'relationship', 
    'monthly_salary', 'team', 'title', 'office', 'office_country', 'office_city', 
    'office_street', 'office_street_number'
]

# Replace None or NaN values in the 'office' column with 'Remote'
employees_final.fillna('Remote', inplace=True)

employees_final.head()