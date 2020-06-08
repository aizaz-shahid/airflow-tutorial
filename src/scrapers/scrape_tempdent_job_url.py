"""
This script runs through the tempdent scraper
Default url: "https://www.tempdent.co.uk/jobs"

run is as:
nohup python3 scrape_tempdent_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-tempdent.out

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


# sudo_password = sys.argv[1]


# Get all urls
def get_all_job_urls(driver, next_page):
    load_count = 1
    job_urls = []

    try:
        while True:
            print('Loaded page:', load_count)
            if load_count % 50 == 0:
                pass# cp.change_ip(sudo_password)  # change the ip every 5th page
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(next_page)
            job_listings = driver.find_elements_by_class_name('list-item')

            # Getting all job urls on current page
            for job in job_listings:
                job_urls.append(job.find_element_by_tag_name('a').get_attribute('href'))

                # Getting current page element
            current_page = driver.find_element_by_class_name('pagination').find_element_by_css_selector(
                'li[class="active"]')

            # Getting next page element
            next_page_element = current_page.find_element_by_xpath('./following-sibling::li')
            next_page = next_page_element.find_element_by_tag_name('a').get_attribute('href')

            time.sleep(random.randint(1, 4))
            load_count += 1

    except Exception as e:
        print(str(e))

    finally:
        return job_urls



def main():
    program_start_time = time.time()
    # Update the executable path of chromedriver in config_webdriver.py if needed
    driver = cw.configure_webdriver()
    # cp.change_ip(sudo_password)  # change the ip

    try:
        parent_url = "https://www.tempdent.co.uk/jobs"
        driver.get(parent_url)

        # Get all job urls
        job_urls = list(set(get_all_job_urls(driver, parent_url)))
        print('Total jobs:', len(job_urls))
        print('Total unique jobs:', len(set(job_urls)))
        job_urls = list(set(job_urls))

        if len(job_urls) != 0:
            # Get jobs dataframe
            file_name = '../data/' + '{}-tempdent-job-url.csv'
            file_name = sf.format_filename(file_name)
            pd.Series(job_urls).to_csv(file_name, index=False,header=False)
            print('\tJob urls stored for tempdent.')
        else:
            print('No jobs')

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
