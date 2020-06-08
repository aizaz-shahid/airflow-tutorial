"""
This script runs through the blueskypeople scraper.
Default url: "https://blueskypeople.co.uk/dental-jobs-search/page/1/?job_search&job_sector&job_type&job_city"

run is as:
nohup python main_scrape_blueskypeople.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-blueskypeople.out

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

# sys_argv = sys.argv


# Get all job details
def get_all_jobs(driver, url, page_number):
    jobs_dataframe = pd.DataFrame()
    try:
        while True:
            print('Currently scraping:', url.format(page_number))
            jobs = driver.find_elements_by_class_name('cool-jobrow')
            print('No. of jobs on current page:', len(jobs))

            if len(jobs) == 0:
                break

            else:
                for i in range(len(jobs)):
                    job = jobs[i]
                    job_details_dictionary = dict()

                    try:
                        header_details = job.find_element_by_class_name('cool-job-header').find_elements_by_tag_name(
                            'div')

                        for detail in header_details:
                            job_details_dictionary[detail.get_attribute('class')] = [detail.text]

                        try:
                            description_url = job.find_element_by_css_selector('a[title="View"]').get_attribute('href')
                            job_details_dictionary['job-url'] = [description_url]

                            # Opens new window
                            driver.execute_script("window.open('');")

                            # Switch to new window
                            driver.switch_to.window(driver.window_handles[1])
                            if i % 300 == 0:
                                pass#   cp.change_ip(sudo_password)  # change the ip every 100 job url
                            driver.get(description_url)

                            # Fetch job description
                            job_details_dictionary['description_details'] = [
                                driver.find_element_by_class_name('post_content_holder').text]
                        except Exception as e:
                            print(str(e))
                        finally:
                            # Close new window
                            driver.close()

                            # Switch back to initial window
                            driver.switch_to.window(driver.window_handles[0])

                        time.sleep(random.randint(1, 4))

                        jobs_dataframe = jobs_dataframe.append(pd.DataFrame(job_details_dictionary))

                    except Exception as e:
                        print(str(e))
                        time.sleep(random.randint(1, 4))

            page_number += 1

            # Converting url into desired format to iterate over multiple pages
            if 'page/{}/' not in url:
                url_split = url.split('?', 1)
                url_split[0] += 'page/{}/?'
                url = ''.join(url_split)

            if page_number % 50 == 0:
                # cp.change_ip(sudo_password)  # change the ip every 5th page
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url.format(page_number))

    except Exception as e:
        print(str(e))

    finally:
        return jobs_dataframe


def main(url, page_number):
    program_start_time = time.time()
    # cp.change_ip(sudo_password)  # change the ip
    # Update the executable path of chromedriver in config_webdriver.py if needed
    driver = cw.configure_webdriver()

    try:
        # Get all jobs
        data = get_all_jobs(driver, url, page_number)

        # Adding timestamp in place of date for uniqueness as it's yet to decide how to name search specific files
        filename = '../data/{}-blueskypeople-jobs.csv'
        filename = sf.format_filename(filename)
        data.to_csv(filename, index=False,header=False)

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
    try:
        page_number = 1
        # sudo_password = sys_argv[1]
        if len(sys_argv) == 3:
            url = sys_argv[2]
            if '/page/' in url:
                url_split = url.split('?', 1)
                current_page_number = url_split[0].split('/page/')[1].split('/', 1)[0]
                url = url.replace(current_page_number, '{}')
                print('Current page number:', current_page_number)
                page_number = int(current_page_number)
                print('Current url:', url)

        else:
            url = "https://blueskypeople.co.uk/dental-jobs-search/page/{}/?job_search&job_sector&job_type&job_city"
            print('Using default url:', url)
            print('Using default page_number:', page_number)

        main(url, page_number)

    except Exception as e:
        print(str(e))
