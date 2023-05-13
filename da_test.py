import pandas as pd
import openpyxl
import xlrd

#Convert the file to csv, read the file, add new colomn name
jobs = pd.read_excel('NZ_Admin_JOBS.xlsx', engine='openpyxl')
jobs.to_csv('NZ_Admin_JOBS.csv', index=True)
jobs.columns = ['job_name', 'job_link', 'company_name', 'location', 'post_date', 'classification']
# print(jobs.head(1))

#Check missing value, Remove missiong value
missing_values_jobname = jobs['job_name'].isnull().sum()
missing_values_joblink = jobs['job_link'].isnull().sum()
    #Companyname has 22 missiong value
missing_values_companyname = jobs['company_name'].isnull().sum()
missing_values_location = jobs['location'].isnull().sum()
missing_values_postdate = jobs['post_date'].isnull().sum()
missing_values_classification = jobs['classification'].isnull().sum()

jobs['company_name'] = jobs['company_name'].fillna(value='unknown')

#Fix Capitalization for job names
for row in jobs['job_name']:
    row = row.title()

#Clean location columns
for i in range(len(jobs['location'])):
    if jobs['location'][i].startswith('location: '):
        jobs['location'][i] = jobs['location'][i][10:]

    #Delete salary in location
jobs['location'] = jobs['location'].apply(lambda x: x.split('$')[0])

#Clean classification columns 
for i in range(len(jobs['classification'])):
    if jobs['classification'][i].startswith('classification: '):
        jobs['classification'][i] = jobs['classification'][i][16:]

    #Move the Salary information to a new column called 'Salary'
salary = []
for i in range(len(jobs['classification'])):
    if '$' in jobs['classification'][i]:
        salary.append(jobs['classification'][i])
        jobs['classification'][i] = 'unknown'
    else:
        salary.append("unknown")
jobs['salary'] = salary

#Post date
for i in range(len(jobs['post_date'])):
    if jobs['post_date'][i][0].isdigit():
        jobs_date = lambda x: x.split(',')[0]
        jobs['post_date'][i] = jobs_date(jobs['post_date'][i])
    else:
        jobs['post_date'][i] = 'unknown'


print(jobs.head())
jobs.to_csv('NZ_Admin_JOBS.csv', index=True)
