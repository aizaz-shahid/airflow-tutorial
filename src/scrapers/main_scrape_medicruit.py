#!/usr/bin/env python
# coding: utf-8

"""
This script runs through the Medicruit scraper.
Default url: 'https://www.medicruit.co.uk/dental-jobs'

run is as:
nohup python3 main_scrape_medicruit.py <your root password> |& tee $(date "+%Y.%m.%d-%H.%M.%S").medicruit_logs.txt

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

def get_all_jobs(driver, total_pages, url):
    cols = ['post-date', 'title', 'location', 'uid', 'job-type', 'job-url', 'description']
    jobs_dataframe = pd.DataFrame(columns=cols)

    for page_number in range(1, total_pages + 1):
        try:
            print('Jobs on page:', str(page_number))
            if page_number % 50 == 0:
                pass # cp.change_ip(sudo_password)  # change the ip every 5th page            

            driver.switch_to.window(driver.window_handles[-1])
            driver.get(url + str(page_number))

            job_urls = driver.find_element_by_class_name('positions').find_elements_by_class_name('position')

            for i in range(len(job_urls)):
                job = job_urls[i]
                # if i % 100 == 0:
                #     cp.change_ip(sudo_password)  # change the ip every 100 job url
                job_details_dictionary = dict()
                job_details_dictionary['post-date'] = [
                    driver.find_element_by_css_selector('div[itemprop="datePosted"]').get_attribute('innerHTML')]
                details = job.find_element_by_class_name('position-heading').text.split(' - ')
                job_details_dictionary['title'] = [details[0]]
                job_details_dictionary['location'] = [details[1]]
                job_details_dictionary['uid'] = [details[2].split(' ')[1]]
                job_details_dictionary['job-type'] = [
                    job.find_element_by_css_selector('div[itemprop="title"]').text.split('|')[0]]
                job_details_dictionary['job-url'] = [
                    job.find_element_by_class_name('position-more-info').get_attribute('href')]
                job_details_dictionary['description'] = [job.find_element_by_class_name('position-description').text]
                jobs_dataframe = jobs_dataframe.append(pd.DataFrame(job_details_dictionary))

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
        url = 'https://www.medicruit.co.uk/dental-jobs/?position-type=&location=&work-type=-1&position-date=-1&page='
        # cp.change_ip(sudo_password)  # change the ip

        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url + str(1))

        pages = driver.find_element_by_class_name('pagination')
        total_pages = int(pages.find_elements_by_tag_name('a')[-1].get_attribute('href').split('page=')[1])
        print('Total pages:', str(total_pages))

        data = get_all_jobs(driver, total_pages, url)

        file_name = '../data/{}-medcruit-jobs.csv'
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
