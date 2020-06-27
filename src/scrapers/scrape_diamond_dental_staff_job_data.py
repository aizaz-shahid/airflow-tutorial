#!/usr/bin/env python
# coding: utf-8

"""
This script runs through the Diamond dental staff scraper.
Default url: 'https://www.diamonddentalstaff.co.uk/careers'

run is as:
nohup python3 scrape_diamond_dental_staff_job_data.py filepath_job_url > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-diamond-dental-staff.out

"""

import os
import sys
import random

from selenium import webdriver
import pandas as pd
import time
import datetime

from utils import standard_formatter as sf
# from utils import change_ip as cp
from utils import config_webdriver as cw
 

# Returns dataframe of jobs
def get_all_jobs(job_urls, driver):
    cols = ['job_url', 'title', 'job_post_date', 'Industry', 'Work Experience', 'Salary', 'City', 'State/Province',
            'Zip/Postal Code', 'Job Description']
    jobs_dataframe = pd.DataFrame(columns=cols)

    for i in range(len(job_urls)):
        job_url = job_urls[i]
        job_details_dictionary = dict()

        job_details_dictionary['job_url'] = [job_url]

        driver.switch_to.window(driver.window_handles[-1])
        driver.get(job_url)

        job_details_dictionary['title'] = [driver.find_element_by_tag_name('h1').text]

        job_post_date = driver.find_element_by_class_name('tem3-postDate').text
        job_post_date = job_post_date.split(' ')[2]
        job_details_dictionary['job_post_date'] = [job_post_date]

        job_details = driver.find_elements_by_class_name('tem3-TextCont')
        job_details = job_details[1:]

        for detail in job_details:
            temp = detail.text.split('\n', 1)
            key, value = temp[0], temp[1].strip()
            job_details_dictionary[key] = [value]

        df = pd.DataFrame(job_details_dictionary)
        jobs_dataframe = jobs_dataframe.append(df)
        time.sleep(random.randint(1, 4))
    jobs_dataframe.reset_index(drop=True, inplace=True)

    return jobs_dataframe



def main():
    program_start_time = time.time()
    driver = cw.configure_webdriver()
    sys_argv = sys.argv

    try:
        parent_url = 'https://www.diamonddentalstaff.co.uk/careers'
        # cp.change_ip()  # change the ip
        driver.get(parent_url)

        # Gets data source from iframe tag
        element = driver.find_element_by_name('htmlComp-iframe')
        iframe_data_src = element.get_attribute('src')
 
        # Always switch window before requesting a new url using driver
        driver.switch_to.window(driver.window_handles[-1])

        # Get all job urls        
        filepath_job_url = sys_argv[1]
        print(filepath_job_url)
        job_urls = pd.read_csv(filepath_job_url).iloc[:,0]

        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))

        if len(job_urls) != 0:
            # Get jobs dataframe
            data = get_all_jobs(job_urls, driver)

            file_name = '../data/{}-diamond-dental-staff-jobs.csv'
            file_name = sf.format_filename(file_name)
            data.to_csv(file_name, index=False)

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
