"""
This script is the main indeed script and calls main_jobs_gcp_single_run.sh to scrape jobs data. 

nohup bash main_jobs_gcp.sh >  $(date "+%Y-%m-%d-%H-%M-%S-")nohup-jobs-gcp.out
"""

project_id=t-emissary-273110
service_account=marketing-dev-compute@t-emissary-273110.iam.gserviceaccount.com
gcs_bucket=dental-jobs-01

rm -rf ../data/
mkdir ../data


nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-dental-recruit-data $service_account $gcs_bucket scrape_dental_recruit_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-recruit*.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-recruit.out

wait
echo "All tasks for indeeed complete."
wait
# gsutil -m mv -r ../data/*.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/
# gsutil -m mv -r ./2020*gcp.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/
# gsutil -m mv -r gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/* gs://dental-jobs/$(date "+%Y-%m-%d")/logs/
# gsutil -m mv -r gs://$gcs_bucket/$(date "+%Y-%m-%d")/data/* gs://dental-jobs/$(date "+%Y-%m-%d")/data/
