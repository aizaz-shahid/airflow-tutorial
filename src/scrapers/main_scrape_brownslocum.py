#!/usr/bin/env python
# coding: utf-8

"""
This script runs through the tempdent scraper.
Default url: 'https://portal.brownslocumlink.com/Jobs'

run is as:
nohup python3 main_scrape_brownslocum.py <your root password> |& tee $(date "+%Y.%m.%d-%H.%M.%S").brownslocum_logs.txt

"""

import random
import os
import sys
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
        while True:
            print('Loaded page:', page_count)
            results = driver.find_elements_by_css_selector('h2[class="results"]')
            job_urls.extend([result.find_element_by_tag_name('a').get_attribute('href') for result in results])

            next_page = driver.find_element_by_css_selector('a[title="Next Page"]').get_attribute('href')
            time.sleep(random.randint(1, 4))

            if page_count % 50 == 0:
                pass# cp.change_ip(sudo_password)  # change the ip every 5th page
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(next_page)

            page_count += 1

    except Exception as e:
        print(str(e))

    finally:
        return job_urls

    # Get all job details


def get_all_jobs(job_urls, driver):
    jobs_dataframe = pd.DataFrame()

    for i in range(len(job_urls)):
        try:
            job_url = job_urls[i]
            job_details_dictionary = dict()
            job_details_dictionary['jobURL'] = [job_url]

            if i % 300 == 0:
                pass# cp.change_ip(sudo_password)  # change the ip every 100 job url
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(job_url)

            # All the data is stored in id = 'ctl00_MainContentPlaceHolder_pageDiv'
            content = driver.find_element_by_id('ctl00_MainContentPlaceHolder_pageDiv')

            # All the span tags' id is equivalent to the column name and its text value is equivalent to the column value
            details = content.find_elements_by_tag_name('span')

            # Fetches column - value data pair 
            for value in details:
                id = value.get_attribute('id')

                # hard coded stop point as no need to scrape further
                if id == 'ctl00_MainContentPlaceHolder_lblSendToFriend':
                    break
                else:
                    job_details_dictionary[id.split('_lbl')[1]] = [value.text]

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

    try:
        parent_url = 'https://portal.brownslocumlink.com/Jobs/Results.aspx?JobResults=1'

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
            print(data)

            file_name = '../data/{}-brownslocum-jobs.csv'
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
