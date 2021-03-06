"""
This script runs through the BDJ scraper.
Default url: "https://www.bdjjobs.com/jobs/"

run is as:
nohup python3 scrape_bdj_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-bdj.out

"""

from selenium import webdriver
import pandas as pd
import time
import datetime
import random
import os
import sys
from utils import standard_formatter as sf
# from utils import change_ip as cp
from utils import config_webdriver as cw
# sudo_password = sys.argv[1]


def get_all_job_urls(driver):
    job_urls = []
    page_count = 0
    try:
        while True:
            jobs = driver.find_elements_by_class_name('lister__header')
            page_count += 1

            for job in jobs:
                job_urls.append(job.find_element_by_tag_name('a').get_attribute('href'))
            print('Jobs on page {}: {}'.format(page_count, len(jobs)))

            next_page = driver.find_element_by_css_selector('a[title="Next page"]').get_attribute('href')
            time.sleep(random.randint(1, 4))

            if page_count % 50 == 0:
                pass# cp.change_ip(sudo_password)  # change the ip every 5th page
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(next_page)

    except Exception as e:
        print(str(e))

    finally:
        print(page_count)
        return job_urls



def main():
    program_start_time = time.time()
    driver = cw.configure_webdriver()
    # cp.change_ip(sudo_password)

    try:
        parent_url = 'https://www.bdjjobs.com/jobs/'
        driver.get(parent_url)

        # Get all job urls
        job_urls = get_all_job_urls(driver)
        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))
        job_urls = list(set(job_urls))


        if len(job_urls) != 0:
            # Get jobs dataframe
            file_name = '../data/' + '{}-bdj-job-url.csv'
            file_name = sf.format_filename(file_name)
            pd.Series(job_urls).to_csv(file_name, index=False,header=False)
            print('\tJob urls stored for BDJ.')

        else:
            print('No jobs found')

    except Exception as e:
        print(str(e))

    finally:
        driver.close()
        # Remove the command file
        # sf.ip_files_cleanup()
        
        seconds = round(time.time() - program_start_time)
        minutes = round(seconds/60, 1)
        hours = round(minutes/60, 1)
        print('DONE! ')
        print("\n\nRun time = {} seconds; {} minutes; {} hours".format(seconds, minutes, hours))


if __name__ == '__main__':
    # main(sudo_password)
    main()
