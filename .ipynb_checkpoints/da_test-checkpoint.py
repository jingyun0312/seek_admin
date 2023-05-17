import pandas as pd
import openpyxl
import xlrd
import wordninja

#Convert the file to csv, read the file, add new colomn name
jobs = pd.read_excel('NZ_Admin_JOBS.xlsx', engine='openpyxl')
# jobs.to_csv('NZ_Admin_JOBS.csv', index=True)
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

    #Remove duplicate string 

jobs_loc = []
for i in range(len(jobs['location'])):
    job_loc = jobs['location'][i].split(',')[0]  #逗号前面的内容（后面不要）
    job_loc_1 = job_loc.split(':') #清楚了逗号后面的内容之后，将逗号前面的内容用:，会分成:前后两项（是一个list）job_loc_1 有[0][1]
    # print(job_loc_1)
    job_location = ''

    for j in job_loc_1:
        # print(j) 
        job_loc_2 = wordninja.split(j) #用wordninja分好之后有空格，但是有重复项的list
        # print(job_loc_2)
        job_loc_3 = list(set(job_loc_2))#去掉重复项
        # print(job_loc_3)
        job_loc_final = ' '.join(job_loc_3)#用空格把list的内容合并
        # print(job_loc_final)
        if len(job_location) != 0:
            job_location = job_location + ": "
        job_location = job_location + job_loc_final
        
    print(job_location)
    jobs_loc.append(job_location.title())
jobs['location'] = jobs_loc

        
#Clean classification columns 
for i in range(len(jobs['classification'])):
    if jobs['classification'][i].startswith('classification: '):
        jobs['classification'][i] = jobs['classification'][i][97:]

    #Move the Salary information to a new column called 'Salary'
salary = []
for i in range(len(jobs['classification'])):
    if '$' in jobs['classification'][i]:
        salary.append(jobs['classification'][i])
        jobs['classification'][i] = 'unknown'
    else:
        salary.append("unknown")
jobs['salary'] = salary

    #Remove Duplicate
for i in range(len(jobs['classification'])):
    job_class = wordninja.split(jobs['classification'][i]) 
    job_class_updated = list(set(job_class))
    jobs['classification'][i] = ' '.join(job_class_updated)
    jobs['classification'][i] = jobs['classification'][i].title()





#Post date
for i in range(len(jobs['post_date'])):
    if jobs['post_date'][i][0].isdigit():
        jobs_date = lambda x: x.split(',')[0]
        jobs['post_date'][i] = jobs_date(jobs['post_date'][i])
    else:
        jobs['post_date'][i] = 'unknown'




#job type
job_type = []
for i in range(len(jobs['job_name'])):
    if jobs['job_name'][i].lower().find('casual') != -1:
        job_type.append('Casual')
    elif jobs['job_name'][i].lower().find('part time') != -1 or jobs['job_name'][i].lower().find('part-time') != -1:
        job_type.append('Part-time')
    elif jobs['job_name'][i].lower().find('full time') != -1 or jobs['job_name'][i].lower().find('full-time') != -1:
        job_type.append('Full-time')
    elif jobs['job_name'][i].lower().find('fixed term') != -1 or jobs['job_name'][i].lower().find('fixed-term') != -1:
        job_type.append('Fixed term')
    else:
        job_type.append('Permanent')
jobs['job_type'] = job_type

jobs.to_csv('NZ_Admin_JOBS.csv', index=True)
