#!/usr/bin/env python
# coding: utf-8

"""
This script runs through the Diamond dental staff scraper.
Default url: 'https://www.diamonddentalstaff.co.uk/careers'

run is as:
nohup python3 scrape_diamond_dental_staff_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-diamond-dental-staff.out

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

# sudo_password = sys.argv[1]
 
# Returns a list of job urls on the website across all the pages
def get_all_job_urls(driver):
    job_urls = []
    page_count = 0
    try:
        while True:
            if page_count % 50 == 0:
                pass # cp.change_ip(sudo_password)  # change the ip every 5th page          
            jobs = driver.find_elements_by_class_name('jobdetail')
            page_count += 1
            for job in jobs:
                job_urls.append(job.get_attribute('href'))
            print(f'Jobs on page {page_count}: {len(jobs)}')
            driver.find_element_by_xpath('//*[@id="zr-joblist-next-15987000000333059"]/a').click()

    except Exception as e:
        print(str(e))

    finally:
        return job_urls


def main(sudo_password):
    program_start_time = time.time()
    driver = cw.configure_webdriver()

    try:
        parent_url = 'https://www.diamonddentalstaff.co.uk/careers'
        driver.get(parent_url)

        # Gets data source from iframe tag
        element = driver.find_element_by_name('htmlComp-iframe')
        iframe_data_src = element.get_attribute('src')

        # Always switch window before requesting a new url using driver
        driver.switch_to.window(driver.window_handles[-1])

        # Get all job urls
        driver.get(iframe_data_src)
        job_urls = get_all_job_urls(driver)
        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))

        if len(job_urls) != 0:
            # Get jobs dataframe
            file_name = '../data/' + '{}-diamond-dental-staff-job-url.csv'
            file_name = sf.format_filename(file_name)
            pd.Series(job_urls).to_csv(file_name, index=False,header=False)
            print('\tJob urls stored for diamond-dental-staff.')

        else:
            print('No jobs found')

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
