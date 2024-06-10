from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
import logging
import os
import atexit
import spacy
nlp = spacy.load('en_core_web_sm')
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
import time


dirname = os.path.dirname(__file__)
#dirname = os.path.dirname(__file__)
# from fuzzywuzzy import fuzz


mydb = pymysql.connect(
    # host="69.216.19.140",
    host="50.28.107.39",
    user="narvee",
    port=3306,
    password="Atc404$",
    database="narvee_ATS"
)


# mydb = pymysql.connect(
 
#   host="localhost",
#   user=		"root",
#   password=	"Nadmin123$",
#   database=	"narvee_hr"
# )



today = date.today()
Today= today.strftime("%Y-%m-%d")
yesterday = today - timedelta(days = 2)
Yesterday = yesterday.strftime("%Y-%m-%d")


# Define the directory path
log_directory = os.path.join(dirname, 'logfiles')

# Create the directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging after ensuring the directory exists
logging.basicConfig(filename=os.path.join(log_directory, 'log-US-{d}.log'.format(d=Today)),
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# +
### skills category excel
# df=pd.read_excel(os.path.join(dirname,'IT_skill_category.xlsx'))
# df=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/IT_skill_category_HOT.xlsx'))

# startno=0
# endno=len(df)

##DateFilter
start_date = Yesterday
end_date = Today

## Job Sites Excel
# df1=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/JobSites1.xlsx'))

# +

## Skills from Job_description
df2=pd.read_excel(os.path.join(dirname,'/Users/admin/Documents/listofskills.xlsx'))
# -

# df2.head()

## import common fields dictionary
from Commonfields import Commonfields

# Create a cursor object
mycursor = mydb.cursor()

import pytz
from datetime import datetime, timedelta
cst_timezone = pytz.timezone('America/Chicago')
now_cst = datetime.now().astimezone(cst_timezone)
today_cst = now_cst.strftime('%Y-%m-%d')
yesterday_cst = now_cst - timedelta(days=2)
#yesterday_cst = yesterday_cst.replace(hour=0, minute=0, second=0)
yesterday_cst_str = yesterday_cst.strftime('%Y-%m-%d')

# Query to retrieve all distinct job sources for today and yesterday
#select_query_all = f"SELECT DISTINCT job_source FROM tbl_rec_requirement WHERE posted_on >= '{yesterday_cst_str}' AND posted_on <= '{today_cst}'"
# select_query_all = f"SELECT  job_source FROM tbl_rec_requirement WHERE (posted_on >= '{yesterday_cst_str} 00:00:00' AND posted_on <= '{today_cst} 23:59:59')"
select_query_all=f"SELECT  job_source FROM tbl_rec_requirement WHERE source='Insight Global'"

mycursor.execute(select_query_all)

# Fetch all the rows
result_all = mycursor.fetchall() 
print(len(result_all))
start_date_1 = now_cst.strftime("%Y-%m-%d 00:00:00")
end_date_1 = now_cst.strftime("%Y-%m-%d 23:59:00")

select_query_both = f"""SELECT DISTINCT t.technologyarea
    FROM technologies t
    JOIN consultant_info c ON t.id = c.techid
    WHERE c.consultantflg = 'sales'
    AND c.status != 'InActive'
    AND NOT EXISTS (
        SELECT 1
        FROM submission sub
        WHERE sub.consultantid = c.consultantid
        AND sub.flg = 'sales'
        AND sub.createddate BETWEEN '{start_date_1}' AND '{end_date_1}'
    )
    ORDER BY t.technologyarea ASC;

"""
logging.info('Successfully Done ')
# Execute the query
mycursor.execute(select_query_both)



# job_titles_strings  = ['.Net', 'AS400%20cobol%20developer', 'Cloud%20Engineer', 'Cyber%20Security', 'Data%20Engineer', 'Devops%20Engineer', 'Embedded%20software%20developer', 'ETL%20Developer', 'Front%20End%20Developer', 'Full%20Stack%20Developer', 'Java%20Full%20Stack%20Developer', 'Kinaxis%20Rapid%20Response', 'Mainframe%20Developer%20with%20COBOL', 'Oracle%20SCM%20Cloud', 'Project%20Manager', 'RPA%20Developer', 'Salesforce%20Developer', 'SAP%20EAM%20Functional%20Lead', 'Scrum%20Master', 'SDET', 'Sr.%20Full%20Stack%20Java%20Developer', 'Test%20Engineer%20with%20QA', 'Workday%20Enhancements%20&%20Support']

time.sleep(5)
job_titles_strings = [item[0].replace(" ", "%20").strip() for item in mycursor.fetchall()]

print("Unique Tech Count:",len(job_titles_strings))

mycursor.close()



extra_technologies = [
    "Appian%20BPM%20Developer",
    "Camunda",
    "Oracle%20HCM",
    "IBM%20BPM",
    "Okta",
    "Sail%20Point",
    "Qualys",
    "Netsparker",
    "Sonar%20Qube",
    'Cloud%20Web%20Application%20Firewall',
    'DNS%20Attacks%20Detection%20Software',
    'Cloud%20flare', 'Akamai', 
    'application%20security%20tools', 
    'Check%20Marx', 
    'HCL%20AppScan',
    'Burp%20Suite'
    'SAP%20Functional%20Consultant%20SD%20&%20WM'
]

job_titles_strings.extend(extra_technologies)


# job_titles_strings =  [' ','Java%20Develoepr','Python%20Developer']
# job_titles_strings =  ['Java','Azure%20Devops%20Developer', 'Mainframe%20Developer', 'Sr.%20Java%20Developer', 'frontend%20UI%20Developer', 'Lead%20PHP%20Developer', 'Kronos']
# job_titles_strings = ['Appian%20bpm%20Developer', 'Camunda%20BPM', 'Oracle%20HCM', 'IBM%20BPM', 'Okta', 'Sailpoint', 'Qualys']
# job_titles_strings = ['ETL%20Developer', 'Front%20End%20Developer']
# job_titles_strings = ['Cloud%20Web%20Application%20Firewall', 'DNS%20Attacks%20Detection%20Software', 'Cloud%20flare', 'Akamai', 'FASTLY', 'application%20security%20tools', 'Check%20Marx', 'HCL%20AppScan', 'Sonar%20Qube', 'Burp%20Suite']

# Convert the time to CST
cst_timezone = pytz.timezone('America/Chicago')  # CST timezone
cst_time = datetime.now().astimezone(cst_timezone).strftime('%Y-%m-%d %H:%M:%S')


# job_titles_strings=['python%20developer'] 

#=====================================================================================================
#Insight Global


df1=pd.read_excel(os.path.join(dirname, 'c:/Users/admin/Documents/JobSites_U.xlsx'))

from insightglobal import insightglobal
# insightglobal=pd.DataFrame()
logging.info('Insight Global started')
source='InsightGlobal'
insightglobal, w2_contracts= insightglobal(Commonfields(),df1.loc[47, 'ContractURL'],result_all,  job_titles_strings)

# #######################linkedin['posted_on'] = linkedin['posted_on'].apply(lambda x: cst_time)
logging.info('Insight Global Execution done')







logging.info('Concatenation of DataFrames started')
dataframes=[ insightglobal]#   simply  techfetch  ,recruitnet  , indeed,    indeed    linkedin    timesjobs     adzuna   ,  ,  ,      prodapt  monster  naukri   , ,  careerbuilder experis  snaprecruit   dice   monster   ,postjobfree, ,   randstatUSA,careerbuilder,careerjet, joblift,      juju idealist     , , ,judge  idealist,matrixiers,    ,       , jobboard, resumelibrary       timesjobs   resumelibrary   jooble       apexsystems
data=pd.concat(dataframes,ignore_index=True,sort=False) 

data = data.drop_duplicates(subset=['job_source'])

data = data.drop_duplicates(subset=['job_title', 'vendor', 'job_location'])

# +
dictionary=Commonfields()


logging.info('Extracting Email,Phone')
from DataCleaning import extract_email,extract_mobile_number

data

for c in range(len(data)):
    #print(c)
    dictionary['job_industry'].append('IT industry')
    desc=data.iloc[c,5]
    #desc=data.iloc[c,8]
    #print(desc)
    try:
        email= extract_email(desc)
        dictionary['email'].append(email)
    except:
        dictionary['email'].append('None')
    try:
        phone= extract_mobile_number(desc)
        dictionary['phone'].append(phone)
    except:
        dictionary['phone'].append('None')

data['email']=dictionary['email']
data['phone']=dictionary['phone']
data['job_industry']=dictionary['job_industry']

# +
logging.info('Data Cleaning started')
from DataCleaning import clean_posted,date_format,clean_text,clean_phone, extract_job_title_from_text

data = data.dropna(axis=0, subset=['posted_on'])
data['posted_on'] = data['posted_on'].apply(lambda x: clean_posted(x))

data['posted_on'] = data['posted_on'].apply(lambda x: date_format(x))

data['job_description'] = data['job_description'].apply(clean_text)

 
data['job_title'] = data['job_title'].apply(extract_job_title_from_text)
#data=data.drop_duplicates()
logging.info('length of data after dropping the duplicates %s ',len(data))


# -

fd=pd.DataFrame(columns=data.columns)
Technology=list(df2.loc[0:24,'Technology'])
#Technology

data['job_title'] = data['job_title']
#if 'job_title' in data.columns and data['job_title'].dtype == 'O':

for i in range(len(Technology)):
    fd1=data.set_index('job_title')
    fd1=fd1.filter(like=Technology[i],axis=0)
    fd1=fd1.reset_index()
    fd = pd.concat([fd1, fd.dropna(axis=1, how='all')], ignore_index=True, sort=False)

fd['job_title'] = fd['job_title']   # .str.title()

# fd

# fd=fd.drop_duplicates()

fd['Employment_type']=fd['Employment_type'].apply(lambda x: 'Contract')
fd['phone']=fd['phone'].apply(lambda x: clean_phone(x))

# API_ENDPOINT = "http://narveetech.com/usit/requirements_api?api_key=9010096292ce32bb78bce7fe6cbaedc8&username=lekhana.pmk@gmail.com&password=Lekhana123$"


logging.info('Execution End')


#data1=data[['job_title','vendor','job_location','posted_on','job_description','Employment_type','job_skills','job_source','email','phone','category_skill','source', 'isexist']]

#data1 =data1.fillna('')

# Create a cursor object
mycursor = mydb.cursor()

# Query to retrieve all distinct vendors from the 'vendor' table
select_query_all = "SELECT DISTINCT company FROM vendor;"
mycursor.execute(select_query_all)

# Fetch all the distinct vendors
distinct_vendors = set([row[0].lower() for row in mycursor.fetchall()])



# Initialize the 'isexist' column in the DataFrame with the default value '0'
data['isexist'] = 0

# Loop through vendors and update 'isexist' column
for i, row in data.iterrows():
    vendor_lower = str(row['vendor']).lower()  # Convert to lowercase for case-insensitive comparison

    # Check if the vendor name is a substring of any vendor name from the database
    isexist_value = 0
    for db_vendor in distinct_vendors:
        if vendor_lower in db_vendor.lower():
            isexist_value = 1
            break
    
    data.at[i, 'isexist'] = isexist_value


from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Define the SQL query to fetch vendor data
query = '''
    SELECT company, vendortype  
    FROM vendor 
    WHERE vendortype IN ('Current Primary Vendor', 'Future Primary Vendor', 'Primary Vendor');
'''

# Execute the query and fetch vendor data
# cursor = mydb.cursor()
mycursor.execute(query)
vendor_data = mycursor.fetchall()

# Convert the fetched data into a DataFrame
df_vendor_type = pd.DataFrame(vendor_data, columns=['company', 'vendortype'])

# Define a function to get vendor type for a given vendor using fuzzy matching
def get_vendortype(vendor, df, threshold=90):
    # Extract the list of companies from the DataFrame
    companies = df['company'].tolist()
    
    # Find the best match in the list of companies
    match, score = process.extractOne(vendor, companies, scorer=fuzz.token_set_ratio)
    
    # Check if the match score is above the threshold
    if score >= threshold:
        vendortype = df[df['company'] == match].iloc[0]['vendortype']
        return vendortype
    else:
        return None

# Assuming 'data' is your DataFrame that contains the vendors to check
# Add a new column 'vendor_type' by applying the get_vendortype function to each row
data['vendor_type'] = data['vendor'].apply(lambda vendor: get_vendortype(vendor, df_vendor_type))

# Check for vendors without a found type and print them
missing_vendors = data[data['vendor_type'].isnull()]['vendor']
if not missing_vendors.empty:
    for vendor in missing_vendors:
        print(f"Vendor type not found for vendor: {vendor}.")


data1=data[['job_title','vendor','job_location','posted_on','job_description','Employment_type','job_skills','job_source','email','phone','category_skill','source', 'isexist', 'received_from', 'vendor_type', 'job_status']]

data1 =data1.fillna('')


# Create the directory if it does not exist
output_directory = os.path.join(dirname, 'Alljobsscraped')
os.makedirs(output_directory, exist_ok=True)

# Get the current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

data1.to_excel(os.path.join(output_directory, 'HL-Main_US-{s}-{d}.xlsx'.format(s=source, d=current_datetime)), index=False)


sql = "INSERT INTO tbl_rec_requirement (job_title,vendor,job_location,posted_on,job_description,Employment_type,job_skills,job_source,email,phone,category_skill,source, isexist,received_from, vendor_type,job_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for i, row in data1.iterrows():
    # Ensure 'isexist' is a valid integer value
    isexist_value = int(row['isexist']) if pd.notna(row['isexist']) and str(row['isexist']).strip() != '' else 0

    # Handle NaN values in the entire row before inserting into MySQL
    row = row.apply(lambda x: '' if pd.isna(x) else x)

    # Convert 'isexist' to integer before inserting into MySQL
    row['isexist'] = isexist_value

    mycursor.execute(sql, tuple(row))

    # The connection is not autocommitted by default, so we must commit to save our changes
    mydb.commit() 
for contract in w2_contracts:
    # Insert each contract into the table    
    insert_query = """
        INSERT INTO    tbl_rec_fulltime (job_title, vendor, job_location, posted_on, Employment_type, source, job_source, category_skill, job_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """  #          tbl_dice_recs
    values = (
        contract['job_title'],
        contract['vendor'],
        contract['job_location'],
        contract['posted_on'],
        contract['Employment_type'],
        contract['source'],
        contract['job_source'],
        contract['category_skill'],
        contract['job_status']
    )

    mycursor.execute(insert_query, values)
    mydb.commit()



# Close the database connection
mydb.close()
mycursor.close()






def print_success_with_stars():
    name = "SUCCESS"
    characters = {
        'S': [' ****', '*    ', ' *** ', '    *', '*   *', '**** '],
        'U': ['*   *', '*   *', '*   *', '*   *', '*   *', ' *** '],
        'C': [' *** ', '*   *', '*    ', '*    ', '*   *', ' *** '],
        'E': ['**** ', '*    ', '***  ', '*    ', '*    ', '**** ']
    }

    for i in range(6):
        for char in name:
            print(characters.get(char, ['     '])[i], end='   ')
        print()


if __name__ == "__main__":
    print_success_with_stars()



