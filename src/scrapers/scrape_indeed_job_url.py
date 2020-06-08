"""
This script runs through the indeed scraper and extracts the url of the jobs given a search term or file with search terms.
It saved the job url to ../data

Note: To check existing search terms or to add new ones, visit "../data/scraping_jobs_search_term.csv"

run is as:
nohup python3 scrape_indeed_job_url.py <your root password> "['Dental and Maxillofacial Radiology', 'Oral Microbiology']" |& tee $(date "+%Y.%m.%d-%H.%M.%S").indeed_logs.txt
nohup python scrape_indeed_job_url.py password  > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-indeed.out
"""

from selenium import webdriver
import pandas as pd
import time
import datetime
import random
import os
import sys
from utils import config_webdriver as cw
from utils import standard_formatter as sf
# from utils import change_ip as cp


sys_argv = sys.argv


def get_all_job_urls(driver):
    job_urls = []
    page_count = 0
    try:
        while True:
            jobs = driver.find_elements_by_css_selector('a[data-tn-element="jobTitle"]')
            page_count += 1
            for job in jobs:
                job_urls.append(job.get_attribute('href'))
            print('\tJobs on page {}: {}'.format(page_count, len(jobs)))
            next_page = driver.find_element_by_css_selector('link[rel="next"]').get_attribute('href')
            time.sleep(random.randint(1, 4))

            if page_count % 50 == 0:
                pass#   cp.change_ip(sudo_password)  # change the ip
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(next_page)

    except Exception as e:
        print(str(e))

    finally:
        print('\tTotal pages:', page_count)
        return job_urls



def main(job_title_list):
    program_start_time = time.time()

    # Update the executable path of chromedriver in config_webdriver.py if needed
    driver = cw.configure_webdriver()
    # cp.change_ip(sudo_password)  # change the ip

    try:
        for i in range(len(job_title_list)):

            job_url_list = []

            parent_url = 'https://www.indeed.co.uk/jobs?q=' + job_title_list[i] + '&l=United+Kingdom'
            print('\n\nSearch term:', job_title_list[i])
            start = time.time()
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(parent_url)

            # Get all job urls
            job_url_list = get_all_job_urls(driver)
            job_url_list = list(set(job_url_list))
            print('\tTotal jobs for {}: {}'.format(job_title_list[i], len(set(job_url_list))))
            print('\tTotal unique jobs for {}: {}'.format(job_title_list[i], len(set(job_url_list))))

            if len(job_url_list) != 0:
                # Get jobs dataframe
                file_name = '../data/' + '{}-indeed-job-url-' + job_title_list[i].replace('+', '-') + '.csv'
                file_name = sf.format_filename(file_name)
                pd.Series(job_url_list).to_csv(file_name, index=False,header=False)
                print('\tJob urls stored for:', job_title_list[i])

            else:
                print('No jobs found for search term', job_title_list[i])

            seconds = round(time.time() - start)
            minutes = round(seconds/60, 1)
            hours = round(minutes/60, 1)
            print("\tRun time for {} = {} seconds; {} minutes; {} hours.\n\n\n".format(job_title_list[i], seconds, minutes, hours))
            

    except Exception as e:
        print(str(e))

    finally:
        driver.close()
        # sf.ip_files_cleanup()

        seconds = round(time.time() - program_start_time)
        minutes = round(seconds/60, 1)
        hours = round(minutes/60, 1)
        print('DONE! ')
        print("\n\nRun time for all job searches on indeed = {} seconds; {} minutes; {} hours".format(seconds, minutes, hours))


if __name__ == '__main__':
    try:
        # sudo_password = sys_argv[1]
        if len(sys_argv) == 2:
            job_title_list = eval(sys_argv[1])
            job_title_list = list(map(lambda x: x.lower().replace(' ', '+'), job_title_list))
        else:
            job_search_terms = pd.read_csv('scraping_jobs_search_term.csv')
            job_title_list = job_search_terms['search_term'].apply(lambda x: x.lower().replace(' ', '+')).tolist()

        main(job_title_list)

    except Exception as e:
        print(str(e))
