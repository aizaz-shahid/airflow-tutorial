#!/usr/bin/env python
# coding: utf-8

"""
This script runs through the dentalrecruit scraper.
Default url: 'https://www.dentalrecruitnetwork.co.uk/jobs'

run is as:
nohup python3 scrape_dental_recruit_job_data.py filepath_job_url > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-recruit.out

"""

from selenium import webdriver
import pandas as pd
import time
import datetime
import os
import sys
import random
from utils import standard_formatter as sf
# from utils import change_ip as cp
from utils import config_webdriver as cw
 
def get_all_jobs(job_urls, driver):
    cols = ['Job URL', 'Title', 'Location', 'Sector', 'Job type', 'Salary', 'Contact', 'Contact email', 'Contact phone',
            'Published', 'Expiry date', 'Startdate', 'Job Description']
    jobs_dataframe = pd.DataFrame(columns=cols)

    for i in range(len(job_urls)):
        try:
            job_url = job_urls[i]
            job_details_dictionary = dict()

            job_details_dictionary['Job URL'] = [job_url]

            driver.switch_to.window(driver.window_handles[-1])
            driver.get(job_url)

            # Extracts job title
            job_details_dictionary['Title'] = [driver.find_element_by_tag_name('h1').text]

            # Extracts 'Location', 'Sector', 'Job type', 'Salary', 'Contact', 'Contact email', 'Contact phone',
            # 'Published', 'Expiry date', 'Startdate'
            details = driver.find_element_by_css_selector('ul[class="job-details-list clearfix"]').text.split('\n')
            for index in range(0, len(details), 2):
                job_details_dictionary[details[index].replace(':', '')] = details[index + 1]

            # Extracts job description
            job_details_dictionary['Job Description'] = [
                driver.find_element_by_css_selector('article[class="clearfix mb20"]').text]

            df = pd.DataFrame(job_details_dictionary)
            jobs_dataframe = jobs_dataframe.append(df)
            time.sleep(random.randint(1, 4))

        except Exception as e:
            print(str(e))
            time.sleep(random.randint(1, 4))

    jobs_dataframe.reset_index(drop=True, inplace=True)

    return jobs_dataframe


def main():
    program_start_time = time.time()
    driver = cw.configure_webdriver()
    sys_argv = sys.argv

    try:
        # job_title_list = ['locum+dentist']        
        parent_url = 'https://www.dentalrecruitnetwork.co.uk/jobs'
        driver.get(parent_url)

        # Get all job urls
        filepath_job_url = sys_argv[1]
        print(filepath_job_url)
        job_urls = pd.read_csv(filepath_job_url).iloc[:,0]

        print('Total jobs:', len(job_urls))
        job_urls = list(set(job_urls))
        print('Unique jobs:', len(job_urls))

        if len(job_urls) != 0:
            # Get jobs dataframe
            data = get_all_jobs(job_urls, driver, )

            file_name = '../data/{}-dental-recruit-jobs.csv'
            file_name = sf.format_filename(file_name)
            data.to_csv(file_name)
        else:
            print('No jobs found')

    except Exception as e:
        print(str(e))

    finally:
        driver.close() 
        
        seconds = round(time.time() - program_start_time)
        minutes = round(seconds/60, 1)
        hours = round(minutes/60, 1)
        print('DONE! ')
        print("\n\nRun time = {} seconds; {} minutes; {} hours".format(seconds, minutes, hours))        


if __name__ == '__main__':
    main()
