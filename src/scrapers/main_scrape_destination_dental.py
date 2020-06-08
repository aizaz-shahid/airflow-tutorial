#!/usr/bin/env python
# coding: utf-8

# In[13]:
"""
This script runs through the Destination Dental scraper.
Default url: 'https://destinationdental.co.uk/find-a-job'

run is as:
nohup python3 main_scrape_destination_dental.py <your root password> |& tee $(date "+%Y.%m.%d-%H.%M.%S").destinationdental_logs.txt

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


# Get all urls
def get_all_job_urls(driver):
    job_urls = []
    page_count = 1

    try:
        # while True:
        while page_count < 5:
            try:
                if driver.find_element_by_css_selector('a[class="load_more_jobs"][style="display: none;"]'):
                    print('Pages loaded:', page_count)
                    break

            except Exception as e:
                print(str(e))
                page_count += 1
                print('Loading page:', page_count)
                time.sleep(random.randint(1, 4))
                if page_count % 20 == 0:
                    pass# cp.change_ip(sudo_password)  # change the ip every 5th page
                driver.find_element_by_css_selector('a[class="load_more_jobs"]').click()

        selectors = driver.find_elements_by_class_name('job_listing-clickbox')
        job_urls = [link.get_attribute('href') for link in selectors]

    except Exception as e:
        print(str(e))

    finally:
        return job_urls

    # Get all job details


def get_all_jobs(job_urls, driver):
    cols = ['Job URL', 'Title', 'job-type', 'location', 'date-posted', 'job-company', 'jmfe-custom-field-wrap',
            'Job Description', 'position-filled', 'listing-expired']
    jobs_dataframe = pd.DataFrame(columns=cols)

    for i in range(len(job_urls)):
        try:
            job_url = job_urls[i]
            job_details_dictionary = dict()

            job_details_dictionary['Job URL'] = [job_url]

            if i % 300 == 0:
                pass# cp.change_ip(sudo_password)  # change the ip every 100 job url
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(job_url)

            # Extracts job title
            job_details_dictionary['Title'] = [driver.find_element_by_tag_name('h1').text]

            # Extracts job-type, location, date-posted, job-company, jmfe-custom-field-wrap (salary), position-filled, 
            # listing-expired
            details = driver.find_element_by_css_selector('ul[class="job-listing-meta meta"]')
            details = details.find_elements_by_tag_name('li')

            for detail in details:
                class_name = detail.get_attribute('class').split(' ')[0]

                if class_name not in job_details_dictionary:
                    job_details_dictionary[class_name] = [detail.text]
                else:
                    job_details_dictionary[class_name][0] += ', ' + detail.text

            # Extracts job description
            job_details_dictionary['Job Description'] = [
                driver.find_element_by_class_name('job_listing-description').text]

            df = pd.DataFrame(job_details_dictionary)
            jobs_dataframe = jobs_dataframe.append(df)
            time.sleep(random.randint(1, 4))


        except Exception as e:
            print(str(e))
            time.sleep(random.randint(1, 4))

    jobs_dataframe.rename(columns={'jmfe-custom-field-wrap': 'salary'}, inplace=True)
    jobs_dataframe.reset_index(drop=True, inplace=True)

    return jobs_dataframe


def main():
    program_start_time = time.time()
    driver = cw.configure_webdriver()

    try:
        parent_url = 'https://destinationdental.co.uk/find-a-job/'
        # cp.change_ip(sudo_password)  # change the ip
        driver.get(parent_url)

        # Get all job urls        
        job_urls = get_all_job_urls(driver)
        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))
        job_urls = list(set(job_urls))

        if len(job_urls) != 0:
            # Get jobs dataframe
            data = get_all_jobs(job_urls, driver)

            file_name = '../data/{}-destination-dental-jobs.csv'
            file_name = sf.format_filename(file_name)
            data.to_csv(file_name, index=False,header=False)

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
