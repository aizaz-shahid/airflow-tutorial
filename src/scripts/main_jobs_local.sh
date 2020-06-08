# # run this file as: 
# # nohup bash main_jobs_local.sh sudo_password >  ./$(date "+%Y-%m-%d-%H-%M-%S-")nohup-main-jobs.out

# # sleep 90m
# start=`date +%s`
# rm -rf ../data/
# mkdir ../data

# gcs_bucket=dental-jobs-test

# # Scrape the job url 

# bash /usr/local/airflow/dependencies/requirements.sh $1
# surfshark-vpn down
# nohup python /usr/local/airflow/scrapers/scrape_bdj_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-bdj.out
# # nohup python scrape_dental_elite_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-dental-elite.out
# # nohup python scrape_dental_recruit_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-dental-recruit.out
# # nohup python scrape_diamond_dental_staff_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-diamond-dental-staff.out
# # nohup python scrape_tempdent_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-tempdent.out
# # nohup python scrape_zest_dental_job_url.py sudo_password > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-zest-dental.out
# # nohup python scrape_indeed_job_url.py sudo_password  > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-indeed.out
# surfshark-vpn down
# gsutil -m mv -r ../data/*.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/job-url/
# gsutil -m mv -r ../data/*.csv gs://$gcs_bucket/$(date "+%Y-%m-%d")/job-url/

# surfshark-vpn down
# bash requirements.sh $1
# # python main_scrape_dental_match.py $1 > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-match.out 
# # python main_scrape_greenapple_dental.py $1 > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-greenapple-dental.out
# # python main_scrape_mbrdental.py $1 > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-mbrdental.out
# # python main_scrape_medicruit.py $1 > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-medicruit.out
# # python main_scrape_brownslocum.py $1 > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-brownslocum.out
# # python main_scrape_blueskypeople.py $1 > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-blueskypeople.out
# # python main_scrape_destination_dental.py $1 > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-destination-dental.out
# gsutil -m mv -r ../data/*.csv gs://$gcs_bucket/$(date "+%Y-%m-%d")/data/
# gsutil -m mv -r ../data/*.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/


# end=`date +%s`
# runtime_seconds=$((end-start))
# let "runtime_minutes = $((runtime_seconds/60))"
# let "runtime_hours = $((runtime_minutes/60))"

# echo "\n\n"
# echo "Total run in seconds: "$runtime_seconds
# echo "Total run in minutes: "$runtime_minutes
# echo "Total run in hours: "$runtime_hours

# surfshark-vpn down
# gsutil mv ./2020*nohup-main-jobs*.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/


project_id=dentaway-01
service_account=marketing-dev-compute@dentaway-01.iam.gserviceaccount.com
gcs_bucket=dental-jobs

rm -rf ../data/
mkdir ../data

nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-bdj $service_account $gcs_bucket scrape_bdj_job_url.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-bdj.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-dental-elite $service_account $gcs_bucket scrape_dental_elite_job_url.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-dental-elite.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-dental-recruit $service_account $gcs_bucket scrape_dental_recruit_job_url.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-dental-recruit.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-dental-staff $service_account $gcs_bucket scrape_diamond_dental_staff_job_url.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-diamond-dental-staff.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-tempdent-job $service_account $gcs_bucket scrape_tempdent_job_url.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-tempdent.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-zest-dental $service_account $gcs_bucket scrape_zest_dental_job_url.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-zest-dental.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-indeed-job $service_account $gcs_bucket scrape_indeed_job_url.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-job-url-indeed.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-scrape-dental $service_account $gcs_bucket main_scrape_dental_match.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-dental-match.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-greenapple-dental $service_account $gcs_bucket main_scrape_greenapple_dental.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-greenapple-dental.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-mbrdental $service_account $gcs_bucket main_scrape_mbrdental.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-mbrdental.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-medicruit $service_account $gcs_bucket main_scrape_medicruit.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-medicruit.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-brownslocum $service_account $gcs_bucket main_scrape_brownslocum.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-brownslocum.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-blueskypeople $service_account $gcs_bucket main_scrape_blueskypeople.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-blueskypeople.out
# nohup bash /usr/local/airflow/scripts/main_jobs_gcp_single_run.sh $project_id vm-destination-dental $service_account $gcs_bucket main_scrape_destination_dental.py  >  ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-destination-dental.out
wait
echo "All tasks for indeeed complete."
wait
# gsutil -m mv -r ../data/*.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/
# gsutil -m mv -r ./2020*gcp.out gs://$gcs_bucket/$(date "+%Y-%m-%d")/logs/