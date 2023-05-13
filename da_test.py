import pandas as pd
import openpyxl
import xlrd

#Convert the file to csv, read the file, add new colomn name
jobs = pd.read_excel('NZ_Admin_JOBS.xlsx', engine='openpyxl')
jobs.to_csv('NZ_Admin_JOBS.csv', index=True)
jobs.columns = ['job_name', 'job_link', 'company_name', 'location', 'post_date', 'classification']
print(jobs.head(1))

#Check missing value, Remove missiong value
missing_values_jobname = jobs['job_name'].isnull().sum()
missing_values_joblink = jobs['job_link'].isnull().sum()
    #Companyname has 22 missiong value
missing_values_companyname = jobs['company_name'].isnull().sum()
missing_values_location = jobs['location'].isnull().sum()
missing_values_postdate = jobs['post_date'].isnull().sum()
missing_values_classification = jobs['classification'].isnull().sum()

jobs = jobs['company_name'].fillna(value='unknown')
print(jobs.head(1))