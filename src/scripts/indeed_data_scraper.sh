"""
This script is the main indeed script and calls main_jobs_gcp_single_run.sh to scrape jobs data. 

nohup bash main_jobs_gcp.sh >  $(date "+%Y-%m-%d-%H-%M-%S-")nohup-jobs-gcp.out
"""

project_id=t-emissary-273110
service_account=marketing-dev-compute@t-emissary-273110.iam.gserviceaccount.com
gcs_bucket=dental-jobs-01

rm -rf ../data/
mkdir ../data
echo $2
nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id $1 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*$2 >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-$2-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-02 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*locum-dentist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-locum-dentist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-03 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*associate-dentist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-associate-dentist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-04 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-nurse.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-nurse-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-05 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*locum-dental-nurse.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-locum-dental-nurse-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-06 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-hygienist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-hygienist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-07 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*locum-dental-hygienist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-locum-dental-hygienist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-08 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-therapist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-therapist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-09 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-technician.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-technician-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-10 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-orthodontic-therapist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-orthodontic-therapist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-11 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-specialist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-specialist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-12 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*dental-public-health.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-public-health-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-13 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*endodontist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-endodontist-indeed.out & 
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-14 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*orthodontist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-orthodontist-indeed.out &
# nohup bash /home/airflow/gcs/data/scrape_data_gcp_single_run.sh $project_id vm-indeed-15 $service_account $gcs_bucket scrape_indeed_job_data.py ../data/job-url/`date '+%Y-%m-%d'`*periodontist.csv >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-periodontist-indeed.out



wait
echo "All tasks for indeeed complete."
wait
# gsutil -m mv -r ../data/*.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/
# gsutil -m mv -r ./2020*gcp.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/
# gsutil -m mv -r gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/* gs://dental-jobs/$(date "+%Y-%m-%d")/logs/
# gsutil -m mv -r gs://$gcs_bucket/$(date "+%Y-%m-%d")/data/* gs://dental-jobs/$(date "+%Y-%m-%d")/data/
