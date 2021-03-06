"""
This script runs through the Dental Elite scraper.
Default url: "https://www.dentalelite.co.uk/jobs/"

run is as:
nohup python3 scrape_dental_elite_job_data.py filepath_job_url > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-elite.out

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
def get_all_jobs(job_urls, driver):
    cols = ['Job URL', 'Ref', 'Title', 'Position Type', 'Location', 'posted', 'Salary', 'Description']
    jobs_dataframe = pd.DataFrame(columns=cols)

    for i in range(len(job_urls)):
        try:
            job_url = job_urls[i]
            job_details_dictionary = dict()

            job_details_dictionary['Job URL'] = [job_url]

            driver.switch_to.window(driver.window_handles[-1])
            driver.get(job_url)

            selector = driver.find_element_by_css_selector('div[class="job-details"]')
            job_details_dictionary['Ref'] = [
                selector.find_element_by_css_selector('div[class="ref"]').text.split(' ', 1)[1]]

            job_details_dictionary['Title'] = [selector.find_element_by_css_selector('div[class="title"]').text]

            info_row = selector.find_element_by_css_selector('div[class="info-row"]').find_elements_by_tag_name('div')

            for i in info_row:
                info = i.text.split(':')
                job_details_dictionary[info[0].strip()] = [info[1].strip()]

            job_details_dictionary['Description'] = [selector.find_element_by_css_selector('div[class="details"]').text]

            job_details_dictionary['Salary'] = [
                selector.find_element_by_css_selector('div[class="value"]').text.strip()]

            df = pd.DataFrame(job_details_dictionary)

            jobs_dataframe = jobs_dataframe.append(df)
            time.sleep(random.randint(1, 4))

        except Exception as e:
            print(str(e))
            time.sleep(random.randint(1, 4))

    return jobs_dataframe


def main():
    program_start_time = time.time()
    driver = cw.configure_webdriver()
    sys_argv = sys.argv

    try:
        parent_url = 'https://www.dentalelite.co.uk/jobs/'
        driver.get(parent_url)

        # Get all job urls
        filepath_job_url = sys_argv[1]
        print(filepath_job_url)
        job_urls = pd.read_csv(filepath_job_url).iloc[:,0]

        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))
        job_urls = list(set(job_urls))

        if len(job_urls) != 0:
            # Get jobs dataframe
            data = get_all_jobs(job_urls, driver)
            file_name = '../data/{}-dental-elite-jobs.csv'
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
