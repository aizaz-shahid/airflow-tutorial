"""
This script runs through the indeed scraper. It reads the indeed job URLs given as argument for the file path
and it scrapes the data and writes it in the ../data/ folder. 

run is as:
nohup python3 scrape_indeed_job_data.py filepath_job_url |& tee $(date "+%Y.%m.%d-%H.%M.%S").indeed_logs.out

"""

from selenium import webdriver
import pandas as pd
import time, datetime
import random, os, sys
from utils import config_webdriver as cw
from utils import standard_formatter as sf
# from utils import change_ip as cp

sys_argv = sys.argv


 
def get_all_jobs(job_urls, driver, search_term):

    from tqdm import tqdm

    cols = ['job_url', 'title', 'recruiter', 'location', 'job_type', 'salary', 'job_description', 'posted']
    jobs_dataframe = pd.DataFrame(columns=cols)

    print('Scraping jobs on indeed for {} ...'.format(search_term))


    for i in tqdm(range(len(job_urls))):
        try:
 
            job_url = job_urls[i]
            job_details_dictionary = dict()
            job_details_dictionary['job_url'] = [job_url]

            driver.switch_to.window(driver.window_handles[-1])
            driver.get(job_url)

            # Extracts job title
            job_details_dictionary['title'] = [driver.find_element_by_tag_name('h3').text]

            # Fetches only company name
            job_details_dictionary['recruiter'] = [
                driver.find_element_by_class_name('jobsearch-CompanyInfoWithoutHeaderImage').text.split('\n')[0]]

            job_details = driver.find_elements_by_css_selector(
                'div[class="jobsearch-JobMetadataHeader-itemWithIcon icl-u-textColor--secondary icl-u-xs-mt--xs"]')

            # Extracts location/job_type/salary
            for detail in job_details:
                class_name = detail.find_element_by_tag_name('div').get_attribute('class')

                if class_name == 'icl-IconFunctional icl-IconFunctional--location icl-IconFunctional--md':
                    job_details_dictionary['location'] = [detail.text]

                elif class_name == 'icl-IconFunctional icl-IconFunctional--jobs icl-IconFunctional--md':
                    job_details_dictionary['job_type'] = [detail.text]

                elif class_name == 'icl-IconFunctional icl-IconFunctional--salary icl-IconFunctional--md':
                    job_details_dictionary['salary'] = [detail.text]

            job_details_dictionary['job_description'] = [driver.find_element_by_id('jobDescriptionText').text]

            job_details_dictionary['posted'] = [
                driver.find_element_by_class_name('jobsearch-JobMetadataFooter').text.strip()]

            df = pd.DataFrame(job_details_dictionary)
            jobs_dataframe = jobs_dataframe.append(df, sort=False)
            time.sleep(random.randint(1, 4))

        except Exception as e:
            print(str(e))
            time.sleep(random.randint(1, 4))

    return jobs_dataframe

    

if __name__ == '__main__':

    try:
        program_start_time = time.time()
        driver = cw.configure_webdriver()
        driver.switch_to.window(driver.window_handles[-1])

        filepath_job_url = sys_argv[1]
        print(filepath_job_url)
        search_term = filepath_job_url.split('url')[-1].split('.')[0][1:]
        job_urls = pd.read_csv(filepath_job_url).iloc[:,0]

        if len(job_urls) != 0:
            print('Total jobs for {}: {}'.format(search_term, len(job_urls)))
            data = get_all_jobs(job_urls, driver, search_term)

            file_name = '../data/' + '{}-indeed-jobs-' + search_term + '.csv'
            file_name = sf.format_filename(file_name)
            data.to_csv(file_name, index=False)
            print('Data stored for: {}. shape = {}'.format(search_term, data.shape))
        else:
            print('No jobs found for file with urls {}', search_term) 
    
    except Exception as e:
        print(str(e))
    
    finally:
        driver.close()

        seconds = round(time.time() - program_start_time)
        minutes = round(seconds/60, 1)
        hours = round(minutes/60, 1)
        print('DONE! ')
        print("\n\nRun time for all job searches on indeed for {} = {} seconds; {} minutes; {} hours".format(search_term, seconds, minutes, hours))


