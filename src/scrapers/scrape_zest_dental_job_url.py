"""
This script runs through the zestdental scraper
Default url: "https://www.dentistjobs.co.uk/jobs/search/page:1"

run is as:
nohup python3 scrape_zest_dental_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-zest-dental.out

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

# sudo_password = sys.argv[1]


def get_job_urls(driver):
    job_urls = []
    try:
        while True:
            job_listings = driver.find_elements_by_css_selector('article[class="listing"]')
            job_urls.extend([listing.find_element_by_tag_name('a').get_attribute('href') for listing in job_listings])

            
            next_page = driver.find_element_by_css_selector('link[rel="next"]').get_attribute('href')
            time.sleep(random.randint(1, 4))
            # cp.change_ip(sudo_password)  # change the ip
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(next_page)
            print('Now scraping:', next_page)

    except Exception as e:
        print(str(e))

    finally:
        return job_urls

def main():
    program_start_time = time.time()
    # Update the executable path of chromedriver in config_webdriver.py if needed
    driver = cw.configure_webdriver()

    try:
        url = "https://www.dentistjobs.co.uk/jobs/search/page:1"
        # cp.change_ip(sudo_password)  # change the ip
        driver.get(url)

        # Get all job urls
        job_urls = get_job_urls(driver)
        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))

        if len(job_urls) != 0:
            # Get jobs dataframe
            file_name = '../data/' + '{}-zest-dental-job-url.csv'
            file_name = sf.format_filename(file_name)
            pd.Series(job_urls).to_csv(file_name, index=False,header=False)
            print('\tJob urls stored for zest-dental.')

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
