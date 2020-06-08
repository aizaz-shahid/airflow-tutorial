"""
This script runs through the Dental Match scraper
Default url: "https://dental-match.co.uk/services/JobAdvert?publicSearch=&radius=48"

run is as:
nohup python main_scrape_dental_match.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-match.out 

"""

import json, os, time
import requests
import pandas as pd
import datetime
import sys
from utils import standard_formatter as sf
# from utils import change_ip as cp


# sudo_password = sys.argv[1]

if __name__ == '__main__':

    start_time = time.time()

    url = 'https://dental-match.co.uk/services/JobAdvert?publicSearch=&radius=48'
    filename = "../data/{}-dental-match-jobs"
    filename = sf.format_filename(filename)

    try:
        # cp.change_ip(sudo_password)
        data = requests.get(url).json()
        saveFile = open(filename + '.txt', 'w')
        saveFile.write(json.dumps(data))
        saveFile.close()

        f = open(filename + '.txt', 'r')
        raw_data = f.read()
        f.close()

        json_data = pd.read_json(raw_data)
        normalized_data = pd.io.json.json_normalize(json_data['list'])
        columns = ['link', 'title', 'jobAdvert.applicantType', 'jobAdvert.id', 'jobAdvert.positionType',
                   'jobAdvert.salary', 'jobAdvert.startDate', 'jobAdvert.status',
                   'jobAdvert.address.town', 'jobAdvert.address.areaCode', 'jobAdvert.workingHours',
                   'jobAdvert.code', 'jobAdvert.description', 'jobAdvert.salaryRange.from',
                   'jobAdvert.salaryRange.to', 'jobAdvert.salaryRange.period',
                   'jobAdvert.address.googleAddress.neighbourhood']

        normalized_data = normalized_data[columns]
        normalized_data.to_csv(filename + '.csv', index=False,header=False)
        os.system('rm {}.txt'.format(filename))

    except Exception as e:
        print(str(e))

    finally:
        pass# sf.ip_files_cleanup()

    seconds = round(time.time() - start_time)
    minutes = round(seconds/60, 1)
    hours = round(minutes/60, 1)
    print('DONE! ')
    print("\n\nRun time = {} seconds; {} minutes; {} hours".format(seconds, minutes, hours))

