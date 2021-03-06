#!/usr/bin/env python
# coding: utf-8

"""
This script runs through the mbrdental scraper.
Default url: 'https://mbrdental.co.uk/jobs'

run is as:
nohup python3 main_scrape_mbrdental.py <your root password> |& tee $(date "+%Y.%m.%d-%H.%M.%S").mbrdental_logs.txt

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
def get_all_jobs(driver):
    load_count = 1
    dataframe = pd.DataFrame()
    try:
        while True:
            try:
                # Loading all job listings first
                if load_count % 50 == 0:
                    pass# cp.change_ip(sudo_password)  # change the ip every 5th page

                driver.find_element_by_css_selector('a[class="load_more_jobs"]').click()
                load_count += 1
                time.sleep(random.randint(1, 4))
                if load_count == 3:
                    break

            except Exception as e:
                print(str(e))
                print('load_count', load_count)
                break

                # Fetching all job listing in a list selectors
        selectors = driver.find_element_by_css_selector('ul[class="job_listings"]').find_elements_by_class_name(
            'job_listing')

        dataframe = get_all_jobs_data(selectors, driver)

    except Exception as e:
        print(str(e))

    finally:
        return dataframe


# Get all job details
def get_all_jobs_data(selectors, driver):
    cols = ['job-url', 'post-date', 'position', 'description', 'location', 'job-type', 'description_details']
    jobs_dataframe = pd.DataFrame(columns=cols)

    for i in range(len(selectors)):
        try:
            job = selectors[i]
            job_details_dictionary = dict()
            job_details_dictionary['job-url'] = [job.find_element_by_tag_name('a').get_attribute('href')]

            # Assuming that post date is always present
            job_details_dictionary['post-date'] = [job.find_element_by_tag_name('time').get_attribute('datetime')]

            # Fetch job details
            fetch_values = ['position', 'description', 'location', 'job-type']
            for fetch in fetch_values:
                try:
                    job_details_dictionary[fetch] = [job.find_element_by_class_name(fetch).text.split('\n')[0]]
                except Exception as e:
                    print(str(e))
                    pass

            if i % 300 == 0:
                pass # cp.change_ip(sudo_password)  # change the ip every 100 job url
            # Opens new window
            driver.execute_script("window.open('');")

            # Switch to new window
            driver.switch_to.window(driver.window_handles[1])
            driver.get(job_details_dictionary['job-url'][0])

            # Fetch job description
            job_details_dictionary['description_details'] = [
                driver.find_element_by_css_selector('div[class="article__body post-content"]').text]

            # Close new window
            driver.close()

            # Switch back to initial window
            driver.switch_to.window(driver.window_handles[0])
            df = pd.DataFrame(job_details_dictionary)

            jobs_dataframe = jobs_dataframe.append(df)
            time.sleep(random.randint(1, 4))


        except Exception as e:
            print(str(e))
            time.sleep(random.randint(1, 4))

    jobs_dataframe.rename(columns={'description': 'salary'}, inplace=True)
    jobs_dataframe.reset_index(drop=True, inplace=True)

    return jobs_dataframe


def main():
    program_start_time = time.time()
    driver = cw.configure_webdriver()

    try:
        parent_url = 'https://mbrdental.co.uk/jobs/'
        # cp.change_ip(sudo_password)  # change the ip
        driver.get(parent_url)

        # Get all job urls        
        jobs = get_all_jobs(driver)
        print('Total jobs:', len(jobs))

        file_name = '../data/{}-mbrdental-jobs.csv'
        file_name = sf.format_filename(file_name)
        jobs.to_csv(file_name, index=False,header=False)

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
