"""
This script runs through the tempdent scraper
Default url: "https://www.tempdent.co.uk/jobs"

run is as:
nohup python3 scrape_tempdent_job_data.py filepath_job_url > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-tempdent.out

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

# Get all job details
def get_all_jobs(selectors, driver):
    jobs_dataframe = pd.DataFrame()

    for i in range(len(selectors)):

        try:
            job = selectors[i]

            driver.switch_to.window(driver.window_handles[-1])
            driver.get(job)

            job_details_dictionary = dict()
            job_details_dictionary['URL'] = [job]

            # Fetching job post date
            posted_date = driver.find_element_by_class_name('posted').text.split(':')
            job_details_dictionary[posted_date[0].strip()] = [posted_date[1].strip()]

            job_details_dictionary['Title'] = [driver.find_element_by_tag_name('h2').text]

            details = driver.find_element_by_class_name('central').find_element_by_tag_name('header')
            job_details = details.find_element_by_tag_name('ul').find_elements_by_tag_name('li')

            # Fetching job details in span element
            for element in job_details:
                key = element.find_element_by_tag_name('span').get_attribute('title')
                job_details_dictionary[key] = [element.text]

            job_details_dictionary['Description'] = [driver.find_element_by_id('content').text]
            df = pd.DataFrame(job_details_dictionary)

            jobs_dataframe = jobs_dataframe.append(df)
            time.sleep(random.randint(1, 4))

        except Exception as e:
            print(str(e))
            time.sleep(random.randint(1, 4))

    return jobs_dataframe


def main():
    program_start_time = time.time()
    # Update the executable path of chromedriver in config_webdriver.py if needed
    driver = cw.configure_webdriver()
    sys_argv = sys.argv

    try:
        parent_url = "https://www.tempdent.co.uk/jobs"
        driver.get(parent_url)

        # Get all job urls        
        filepath_job_url = sys_argv[1]
        print(filepath_job_url)
        job_urls = pd.read_csv(filepath_job_url).iloc[:,0]

        print('Total jobs:', len(jobs))
        print('Total unique jobs:', len(set(jobs)))
        jobs = list(set(jobs))

        if len(job_urls) != 0:
            data = get_all_jobs(job_urls, driver)
            filename = '../data/{}-tempdent-jobs.csv'
            filename = sf.format_filename(filename)
            data.to_csv(filename, index=False)
        else:
            print('No jobs')

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
