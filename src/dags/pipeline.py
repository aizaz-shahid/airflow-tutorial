# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.incubator.apache.org/tutorial.html)
"""
from datetime import timedelta
from airflow import AirflowException
import datetime
import pandas as pd
import json
from airflow.models import Variable
import airflow
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.state import State
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.sensors.file_sensor import FileSensor

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

def task_callback(context):
    result = context['task_instance'].xcom_pull()
    if result == '1':
        context['task_instance'].state=State.FAILED

dag = DAG(
    'dentaway_ETL',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
)

# t1_url = BashOperator(
#     task_id='bdj_url',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/bdj_url_scraper.sh ',
#     dag=dag,
# )
# t2_url = BashOperator(
#     task_id='dental_elite_url',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/dental_elite_url_scraper.sh ',
#     dag=dag,
# )
# t3_url = BashOperator(
#     task_id='dental_recruit_url',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/dental_recruit_url_scraper.sh ',
#     dag=dag,
# )
# t4_url = BashOperator(
#     task_id='diamond_dental_url',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/diamond_dental_url_scraper.sh ',
#     dag=dag,
# )
t5_url = BashOperator(
    task_id='indeed_url',
    depends_on_past=False,
    bash_command='/home/airflow/gcs/data/indeed_url_scraper.sh ',
    dag=dag,
)
# t6_url = BashOperator(
#     task_id='tempdent_url',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/tempdent_url_scraper.sh ',
#     dag=dag,
# )
# t7_url = BashOperator(
#     task_id='zest_dental_url',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/zest_dental_url_scraper.sh ',
#     dag=dag,
# )
# t8 = BashOperator(
#     task_id='bluesky_people',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/bluesky_people_scraper.sh ',
#     dag=dag,
# )
# t9 = BashOperator(
#     task_id='browns_locum',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/browns_locum_scraper.sh ',
#     dag=dag,
# )
# t10 = BashOperator(
#     task_id='dental_match',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/dental_match_scraper.sh ',
#     dag=dag,
# )
# t11 = BashOperator(
#     task_id='destination_dental',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/destination_dental_scraper.sh ',
#     dag=dag,
# )
# t12 = BashOperator(
#     task_id='greenapple_dental',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/greenapple_dental_scraper.sh ',
#     dag=dag,
# )
# t13 = BashOperator(
#     task_id='mbr_dental',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/mbr_dental_scraper.sh ',
#     dag=dag,
# )
# t14 = BashOperator(
#     task_id='medicruit',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/medicruit_scraper.sh ',
#     dag=dag,
# )

file_check_command = """
    gsutil -q stat gs://dental-jobs/{{params.date}}/job-url/{{params.filename}}; echo $?
"""
# t1_check_file = BashOperator(
#     task_id="bdj_file_check",
#     depends_on_past=False,
#     bash_command = file_check_command,
#     params = {"filename":"*bdj*.csv","date":str(datetime.datetime.now().date())},
#     xcom_push=True,
#     on_failure_callback = task_callback,
#     on_success_callback = task_callback,
#     dag=dag
# )
# t2_check_file = BashOperator(
#     task_id="dental_elite_file_check",
#     depends_on_past=False,
#     bash_command = file_check_command,
#     params = {"filename":"*dental-elite*.csv","date":str(datetime.datetime.now().date())},
#     xcom_push=True,
#     on_failure_callback = task_callback,
#     on_success_callback = task_callback,
#     dag=dag
# )
# t3_check_file = BashOperator(
#     task_id="dental_recruit_file_check",
#     depends_on_past=False,
#     bash_command = file_check_command,
#     params = {"filename":"*dental-recruit*.csv","date":str(datetime.datetime.now().date())},
#     xcom_push=True,
#     on_failure_callback = task_callback,
#     on_success_callback = task_callback,
#     dag=dag
# )
# t4_check_file = BashOperator(
#     task_id="diamond_dental_file_check",
#     depends_on_past=False,
#     bash_command = file_check_command,
#     params = {"filename":"*diamond-dental-staff*.csv","date":str(datetime.datetime.now().date())},
#     xcom_push=True,
#     on_failure_callback = task_callback,
#     on_success_callback = task_callback,
#     dag=dag
# )

job_title_list = json.loads(Variable.get("search_terms").replace("'",'"'))
t5_check_file=[]
for i,x in enumerate(job_title_list):
    t5_check_file.append(BashOperator(
        task_id="indeed_{}_file_check".format(x),
        depends_on_past=False,
        bash_command = file_check_command,
        params = {"filename":"*"+x.replace('_','-')+"*.csv","date":str(datetime.datetime.now().date())},
        xcom_push=True,
        on_failure_callback = task_callback,
        on_success_callback = task_callback,
        dag=dag
    ))

# def setSearchTerms(context):
#     for i,x in enumerate(list(Variable.get("search_terms"))):
#         print(i,x)
#         d2 = DummyOperator(task_id='generate_data_{0}'.format(i),dag=dag)
#         # d2.execute(context)
#         get_search_terms>>d2

def getSearchTerms():
    job_search_terms = pd.read_csv('/home/airflow/gcs/data/scraping_jobs_search_term.csv')
    job_list=[]
    job_list = job_search_terms['search_term'].apply(lambda x: x.lower().replace(' ', '_')).tolist()
    Variable.set("search_terms", job_list)
    

get_search_terms = PythonOperator(
    task_id='get_search_terms',
    dag=dag,
    python_callable=getSearchTerms
    # on_success_callback=setSearchTerms
)


# t6_check_file = BashOperator(
#     task_id="tempdent_file_check",
#     depends_on_past=False,
#     bash_command = file_check_command,
#     params = {"filename":"*tempdent*.csv","date":str(datetime.datetime.now().date())},
#     xcom_push=True,
#     on_failure_callback = task_callback,
#     on_success_callback = task_callback,
#     dag=dag
# )
# t7_check_file = BashOperator(
#     task_id="zest_dental_file_check",
#     depends_on_past=False,
#     bash_command = file_check_command,
#     params = {"filename":"*zest-dental*.csv","date":str(datetime.datetime.now().date())},
#     xcom_push=True,
#     on_failure_callback = task_callback,
#     on_success_callback = task_callback,
#     dag=dag
# )

# t1_data = BashOperator(
#     task_id='bdj_data',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/bdj_data_scraper.sh ',
#     dag=dag,
# )
# t2_data = BashOperator(
#     task_id='dental_elite_data',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/dental_elite_data_scraper.sh ',
#     dag=dag,
# )
# t3_data = BashOperator(
#     task_id='dental_recruit_data',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/dental_recruit_data_scraper.sh ',
#     dag=dag,
# )
# t4_data = BashOperator(
#     task_id='diamond_dental_data',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/diamond_dental_data_scraper.sh ',
#     dag=dag,
# )
t5_data=[]
for i,x in enumerate(job_title_list):
    t5_data.append(BashOperator(
        task_id='indeed_{}_data'.format(x),
        depends_on_past=False,
        bash_command='/home/airflow/gcs/data/indeed_data_scraper.sh vm-indeed-'+x.replace('_','-')+' '+x.replace('_','-')+'.csv ',
        dag=dag,
    ))

# t6_data = BashOperator(
#     task_id='tempdent_data',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/tempdent_data_scraper.sh ',
#     dag=dag,
# )
# t7_data = BashOperator(
#     task_id='zest_dental_data',
#     depends_on_past=False,
#     bash_command='/home/airflow/gcs/data/zest_dental_data_scraper.sh ',
#     dag=dag,
# )

# t1_url >> t1_check_file >> t1_data
# t2_url >> t2_check_file >> t2_data
# t3_url >> t3_check_file >> t3_data
# t4_url >> t4_check_file >> t4_data
get_search_terms >> t5_url >> t5_check_file
for i,x in enumerate(job_title_list):
    t5_check_file[i] >> t5_data[i]
# t6_url >> t6_check_file >> t6_data
# t7_url >> t7_check_file >> t7_data
