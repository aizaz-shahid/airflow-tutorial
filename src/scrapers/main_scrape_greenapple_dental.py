#!/usr/bin/env python
# coding: utf-8

"""
This script runs through the Green apple dental scraper.
Default url: 'https://www.greenappledental.co.uk/jobs.php'

run is as:
nohup python3 main_scrape_greenapple_dental.py <your root password> |& tee $(date "+%Y.%m.%d-%H.%M.%S").greenappledental_logs.txt

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

sudo_password = sys.argv[1]

# Get all job details
def get_all_jobs(driver):
    jobs_dataframe = pd.DataFrame()

    jobs = driver.find_element_by_id('content').find_elements_by_class_name('jobs')

    for i in range(len(jobs)):
        try:
            job = jobs[i]
            if i % 300 == 0:
                pass# cp.change_ip(sudo_password)  # change the ip every 100 job url            
            job_details_dictionary = dict()
            table_data = job.find_elements_by_tag_name('td')

            title_details = table_data[0].text.split(':')
            job_details_dictionary[title_details[0].strip()] = [title_details[1].strip()]

            for index in range(1, len(table_data), 2):
                job_details_dictionary[table_data[index].text] = [table_data[index + 1].text]


            df = pd.DataFrame(job_details_dictionary)
            jobs_dataframe = jobs_dataframe.append(df)

        except Exception as e:
            print(str(e))

    jobs_dataframe.reset_index(drop=True, inplace=True)

    return jobs_dataframe


def main():
    program_start_time = time.time()
    driver = cw.configure_webdriver()

    try:
        parent_url = 'https://www.greenappledental.co.uk/jobs.php'
        # cp.change_ip(sudo_password)  # change the ip
        driver.get(parent_url)

        # Get all job urls        
        data = get_all_jobs(driver)

        file_name = '../data/{}-greenappledental-jobs.csv'
        file_name = sf.format_filename(file_name)
        data.to_csv(file_name, index=False,header=False)



    except Exception as e:
        print(str(e))

    finally:
        driver.close()
        # sf.ip_files_cleanup()
        
        seconds = round(time.time() - program_start_time)
        minutes = round(seconds/60, 1)
        hours = round(minutes/60, 1)
        print('DONE! ')
        print("\n\nRun time = {} seconds; {} minutes; {} hours".format(seconds, minutes, hours))


if __name__ == '__main__':
    main()
