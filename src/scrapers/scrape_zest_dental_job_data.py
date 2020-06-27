"""
This script runs through the zestdental scraper
Default url: "https://www.dentistjobs.co.uk/jobs/search/page:1"

run is as:
nohup python3 scrape_zest_dental_job_data.py filepath_job_url > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-zest-dental.out

"""

from selenium import webdriver
import pandas as pd
import time
import datetime
import os
import sys
import random
from utils import config_webdriver as cw
from utils import standard_formatter as sf
# from utils import change_ip as cp
 

def get_jobs(driver, job_urls):
    jobs_dataframe = pd.DataFrame()

    for i in range(len(job_urls)):
        try:
            job = job_urls[i]
            job_details_dictionary = dict() 

            driver.switch_to.window(driver.window_handles[-1])
            driver.get(job)

            job_details_dictionary['url'] = [job]
            job_details_dictionary['heading'] = [driver.find_element_by_tag_name('h1').text]

            sub_header = driver.find_element_by_css_selector('div[class="sub-header"]')
            sub_header_details = [s.text for s in sub_header.find_elements_by_tag_name('span')]

            job_details_dictionary['title'] = [sub_header_details[0]]
            job_details_dictionary['location'] = [sub_header_details[1]]
            job_details_dictionary['reference'] = [sub_header_details[2].split('Reference:')[1].strip()]

            job_details_dictionary['job_summary'] = [driver.find_element_by_css_selector(
                'div[class="background--brand-secondary color--white padded--1 radius"]').text]
            description = driver.find_elements_by_tag_name('p')
            job_details_dictionary['description'] = [[d.text for d in description]]

            jobs_dataframe = jobs_dataframe.append(pd.DataFrame(job_details_dictionary))
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
        url = "https://www.dentistjobs.co.uk/jobs/search/page:1"
        driver.get(url)

        # Get all job urls        
        filepath_job_url = sys_argv[1]
        print(filepath_job_url)
        job_urls = pd.read_csv(filepath_job_url).iloc[:,0]

        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))

        if len(job_urls) != 0:
            data = get_jobs(driver, job_urls)
            file_name = '../data/{}-zest-dental-jobs.csv'
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
