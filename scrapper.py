# Import libraries

import os
import requests
import random
import time
import html5lib
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# directory path
path = r'D:\webscrapping_projects\company_data'

# File name
file_name = 'company_data.csv'


if os.path.exists(os.path.join(path,file_name)):
    # If filepath already exists then read the file and set page number value equal to maximum page_number value 
    print(f'{os.path.join(path,file_name)} filepath is available')
    df = pd.read_csv(os.path.join(path,file_name))
    page_no = df['page_no'].max()

else:
    if not os.path.exists(path):
        directory = os.makedirs(path)
    df = pd.DataFrame()
    page_no = 1

# There are 500 webpages available so itering over each page using for loop 
for i in range(page_no,501):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    url = f'https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page={i}'
    webpage = requests.get(url,headers = header)
    if webpage.status_code == 200:

        soup = BeautifulSoup(webpage.text,'html5lib')
        # Initalize  the empty list to store data.
        comp_name = []
        rate      = []
        comp_type = []
        desc      = []
        review    = []
        salary    = []
        interview = []
        job       = []
        benefit   = []
        photo     = []


        for j in soup.find_all('div',class_ = 'companyCardWrapper'):
            company_name = j.find('h2').text.strip()
            rating = j.find('div',class_='rating_text rating_text--md').text.strip()
            company_type = j.find('span',class_ = 'companyCardWrapper__interLinking').text.strip()

            try:
                rated_for= j.find('div',class_ = 'companyCardWrapper__ratingComparisonWrapper').text.strip()

            except:
                rated_for = 'missing'
                print(f'{company_name} is not rated by employees')

            list_1 = j.find_all('span',class_ = 'companyCardWrapper__ActionCount')
            reviews    = list_1[0].text.strip()
            salaries   = list_1[1].text.strip()
            interviews = list_1[2].text.strip()
            jobs       = list_1[3].text.strip()
            benefits   = list_1[4].text.strip()
            photos     = list_1[5].text.strip()

            comp_name.append(company_name)
            rate.append(rating)
            comp_type.append(company_type)
            desc.append(rated_for)
            review.append(reviews)
            salary.append(salaries)
            interview.append(interviews)
            job.append(jobs)
            benefit.append(benefits)
            photo.append(photos)

        # Create tempory dataframe to store the data from webpage
        temp_df = pd.DataFrame({'Company Name':comp_name,
                                'Rating':rate,
                                'Company Type':comp_type,
                                'Rated For':desc,
                                'Reviews':review,
                                'Salaries':salary,
                                'Interviews':interview,
                                'Jobs':job,
                                'Benefits':benefit,
                                'Photos':photo,
                                'page_no': i})
        

        df = pd.concat([df,temp_df],ignore_index = True)

        file = df.to_csv(os.path.join(path,file_name),index = False)
        print(f'page_number {i} is comppleted')

        time.sleep(np.random.choice(range(2,5)))


    else:
        
        print(f"Invalid response. Status code: {webpage.status_code}")