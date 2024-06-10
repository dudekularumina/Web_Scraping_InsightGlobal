import pandas as pd
import logging
from datetime import datetime, timedelta
import re
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import pytz 
from bs4 import BeautifulSoup
import atexit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql 
import requests
from Commonfields import Commonfields
import os
from urllib.parse import urljoin



driver = webdriver.Chrome() 

# driver=webdriver.Edge()

# mydb = pymysql.connect(
 
#   host="localhost",
#   user=		"root",
#   password=	"Nadmin123$",
#   database=	"narvee_hr"
# )


mydb = pymysql.connect(
    # host="69.216.19.140",
    host="50.28.107.39",
    user="narvee",
    port=3306,
    password="Atc404$",
    database="narvee_ATS"
)


# Create a cursor object
mycursor = mydb.cursor()

# Function to release ChromeDriver
def release_chromedriver():
    try:
        # Close the ChromeDriver session
        driver.quit()
        print("ChromeDriver released successfully.")
    except Exception as e:
        print(f"Error releasing ChromeDriver: {e}")

# Define CST timezone
cst_timezone = pytz.timezone('America/Chicago')

now_cst = datetime.now().astimezone(cst_timezone)
today_cst = now_cst.strftime('%Y-%m-%d %H:%M:%S')

yesterday_cst = now_cst - timedelta(days=1)
yesterday_cst = yesterday_cst.replace(hour=0, minute=0, second=0)
yesterday_cst_str = yesterday_cst.strftime('%Y-%m-%d %H:%M:%S')


# Function to check if job already exists
def job_exists(vendor, job_title, job_location):
    select_query = f"SELECT vendor, job_title, job_location FROM tbl_rec_requirement WHERE vendor = %s AND job_title = %s AND job_location = %s AND posted_on >= %s AND posted_on <= %s"
    mycursor.execute(select_query, (vendor, job_title, job_location, yesterday_cst_str, today_cst))
    if mycursor.fetchone():
        return True
    return False

os.environ['DISPLAY']=':2'

# URL='https://jobs.insightglobal.com/find_a_job/?srch=python%20developer&zip=united%20states&remote=false'

dirname=os.path.dirname(os.path.abspath(__file__))
log_directory=os.path.join(dirname, 'logfiles')
os.makedirs(log_directory, exist_ok=True)


# df=pd.read_excel(os.path.join(dirname,'c:/Users/admin/Documents/IT_skill_category_HOT_U.xlsx'))
# startno=0
# endno=len(df)

df1=pd.read_excel(os.path.join(dirname, 'c:/Users/admin/Documents/JobSites_U.xlsx'))

# job_titles_strings=[ 'python%20developer']    #, '.Net developer', 'angular developer', 'java developer', 

def insightglobal(commonfields,URL,result_all, job_titles_strings):
    counter=0

    job=commonfields
    w2_contracts = []
    for i in job_titles_strings:
        time.sleep(2)
        counter +=1
        print("Searching For String:====================",i,"======================", counter)

        for j in range(1,7):
            #skillname=df.loc[i,'SkillName']
            url = (URL).format(j, i)
            html=requests.get(url, verify=True).text
            soup=BeautifulSoup(html, 'html.parser')
            print(f'Insight Global===: {url}')  ### for debugging 
            logging.info(url) 
            time.sleep(5)

            jobelems = soup.find_all('div', class_='result')
            print("Len Of Job Elements=========================", len(jobelems))
            if len(jobelems) == 0:
                continue
            print()
            time.sleep(3)
            # try:
            for e in jobelems:
                vendor='Insight Global'
                
                print("---------------------------")
                role = e.find('div', class_='job-title')
                # print(f'ROLE----:', role.text)
                job_title=role.text
                anchor_tag = role.find('a')
                # Get the 'href' attribute from the anchor tag
                link = anchor_tag['href']
                link = urljoin(url, link)
                print("Link==================================: ", link)
                # link = str(link)
                if (link, ) not in result_all:
                    # print("===========Not in Our Database=============", link)
                    posted_on=e.find('p', class_='date').text
                    # print("Posted On:--===================-", posted_on)

                    job_info = e.find('div', 'job-info')
                    job_info_texts = job_info.find_all('p')

                    # Extracting location, category, job type, and salary
                    job_location = job_info_texts[0].text.strip()
                    category = job_info_texts[1].text.strip()
                    job_type = job_info_texts[2].text.strip()

                    # if 'Contract' in job_type :
                    # print("Job Type:----", job_type)
                    # else:
                    #     print("Skipping job element because it is not a pure Contract job")
                    #     continue

                    salary = job_info_texts[3].text.strip().split('(')[0].strip()  # Removing "(hourly estimate)"

                    # print("Location:==========================", job_location)
                    # print("Category:----", category)
                    # print("Salary:-----", salary)

                    # headers = {
                    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
                    #     }

                    # response = requests.get(link, headers=headers)

                    # # Check if the request was successful
                    # if response.status_code == 200:
                        # html_content = response.text
                        # soup = BeautifulSoup(html_content, 'html.parser')
                        
                        # Find and print job details
                    time.sleep(3)
                    driver.get(link)
                    job_details = driver.find_element(By.XPATH, '//*[@id="form1"]/div[3]/div[3]/div/div[2]/div[2]') 

                    if job_details:
                            # Extract the text from the job description div
                            job_description = job_details.text
                            # print("Job Description:--------------------", job_description)
                            print(" Job Description Fetched................")
                    else:
                        job_description = " "
                        print(f"No job details found")

                    if 'full-time' not in job_description.lower() and 'w2' not in job_description.lower() and not job_exists(vendor, job_title, job_location):
                        if "W2" not in role.text and "perm" not in job_type.lower():
                            print("=======Job not in our Database========:",link)                   
                            job['Employment_type'].append("Contract")
                            job['category_skill'].append(i.replace("%20", " "))
                            job['job_description'].append(job_description)
                            job['job_title'].append(role.text)
                            job['vendor'].append("Insight Global")
                            job['job_location'].append(job_location)
                            job['posted_on'].append(posted_on)
                            job['job_source'].append(link)
                            job['source'].append("Insight Global") 
                            job['job_status'].append("Active")
                    else:
                        print("---------W2 Position------------")
                        w2_contracts.append({
                            'job_title': role.text,
                            'vendor': "Insight Global",
                            'job_location': job_location.strip(),
                            'posted_on': posted_on,
                            'Employment_type': "Contract",
                            'job_source': link.strip(),
                            'source' :'Insight Global',
                            'category_skill': i.replace("%20", " "),
                            'job_status': 'Active'
                        }) 
                else :
                    print("Job already in our Database........", link)
            # except Exception as e:
            #     logging.error(f"Error processing job: {e}")
            #     continue



    for r in range(len(job['job_title'])):
        job['job_country'].append('United States')
        #job['job_source'].append('Simplyhired')
            
        
    insightglobal=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in job.items() ]))
    print('no. of jobs in Insight Global====================: %s', len(insightglobal)) 
    logging.info('no. of jobs in Insigth Global: %s', len(insightglobal))
    # Register the release function to be called on script exit
    mydb.close()
    mycursor.close()
    
    return(insightglobal, w2_contracts)




        

# insightglobal=insightglobal(Commonfields(),df1.loc[47, 'ContractURL'], job_titles_strings)


# dataframes=[insightglobal]

# data = pd.DataFrame(Commonfields())


# for dice in dataframes:
#     data = pd.concat([data, pd.DataFrame(dice.__dict__)], ignore_index=True)
# data=data.drop_duplicates()


# output_dir = '/Users/admin/Documents/'

# # Create the directory if it doesn't exist
# os.makedirs(output_dir, exist_ok=True)
# # import time
# current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# # Specify the path to the Excel file within the created directory
# excel_file_path = os.path.join(output_dir, f'data(insightglobal)-{current_datetime}.xlsx')

# # Write the DataFrame to an Excel file in the created directory
# insightglobal.to_excel(excel_file_path, index=False)

# print(f"Excel file saved at: {excel_file_path}")



    
