"""
This script 
- creates a VM on GCP, 
- copies the code from GCS, 
- runs the indeed scraper given a list of URLs read from GCS
- copies the output back to GCS
- removes the VM

How to run: 

bash main_jobs_indeed_gcp.sh gcp_project_id instance_name service_account gcs_bucket scraper_py_name
bash main_jobs_indeed_gcp.sh $project_id vm-indeed-01 $service_account $gcs_bucket endodontist scrape_indeed_job_data.py > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-bash-endodontist-indeed.out & 

where 
  - gcp_project_id: the GCP project ID.
  - instance_name: the name of the GCP VM instance
  - service_account: service account to give permission to create VMs and to sue GCS; name@project_id..iam.gserviceaccount.com
  - gcs_bucket: the bucket name where to push the data to and copy the code from. Only the name, no gs://
  - scraper_py_name: the name of the python file that will scrape the data from urls.
  - filepath_job_url: the file path where the job url are located 
  

You need to have gcloud SDK [1] installed to make it work on Ubuntu.
[1] https://cloud.google.com/sdk/install

"""

# array with gcp_zones
gcp_zones=("europe-north1-a" "europe-north1-b" "europe-north1-c" \
         "europe-west1-b" "europe-west1-c" "europe-west1-d" \
         "europe-west2-a" "europe-west2-b" "europe-west2-c" \
         "europe-west3-a" "europe-west3-b" "europe-west3-c" \
         "europe-west4-a" "europe-west4-b" "europe-west4-c" \
         "europe-west6-a" "europe-west6-b" "europe-west6-c" \
        #  "northamerica-northeast1-a" "northamerica-northeast1-b" "northamerica-northeast1-c" \
        #  "southamerica-east1-a", "southamerica-east1-b", "southamerica-east1-c" \ 
         "us-central1-a" "us-central1-b" "us-central1-c" "us-central1-f" \
         "us-east1-b" "us-east1-c" "us-east1-d" \
         "us-east4-a" "us-east4-b" "us-east4-c" \
         "us-west1-a" "us-west1-b" "us-west1-c" \
         "us-west2-a" "us-west2-b" "us-west2-c" \
         "us-west3-a" "us-west3-b" "us-west3-c" \
         "us-west4-a" "us-west4-b" "us-west4-c")

# seed random generator
RANDOM=$$$(date +%Y%m%d)
# pick a random entry from the gcp_zones list to check against
random_gcp_zone=${gcp_zones[$RANDOM % ${#gcp_zones[@]}]}

gcloud beta compute --project=$1 instances create $2 \
  --zone=$random_gcp_zone	 \
  --machine-type=n1-standard-1 \
  --subnet=default --network-tier=PREMIUM \
  --maintenance-policy=MIGRATE \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --service-account=$3 \
  --tags=http-server,https-server \
  --boot-disk-device-name=$2 \
  --image=debian-9-stretch-v20200521 \
  --image-project=debian-cloud \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-standard
  # --no-shielded-secure-boot \
  # --shielded-integrity-monitoring \
  # --reservation-affinity=any 
  # --shielded-vtpm \
  # --image=ubuntu-minimal-1804-bionic-v20200317 1
  # --image-project=ubuntu-os-cloud \   

# gcloud compute --project=$1 firewall-rules create default-allow-http \
#   --direction=INGRESS --priority=1000 --network=default \
#   --action=ALLOW --rules=tcp:80 \
#   --source-ranges=0.0.0.0/0 --target-tags=http-server

# gcloud compute --project=$1 firewall-rules create default-allow-https \
# --direction=INGRESS --priority=1000 --network=default \
# --action=ALLOW --rules=tcp:443 \
# --source-ranges=0.0.0.0/0 --target-tags=https-server

sleep 30
gcloud compute ssh --zone=$random_gcp_zone $2 --command "ls -la &&  sudo apt update "
gcloud compute ssh --zone=$random_gcp_zone $2 --command "echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections
sudo apt-get install -y -q"
gcloud compute ssh --zone=$random_gcp_zone $2 --command "sudo chmod 777 /var/cache/debconf/ && sudo chmod 777 /var/cache/debconf/passwords.dat"
gcloud compute ssh --zone=$random_gcp_zone $2 --command "gsutil -m cp -r gs://$4/code/src . && mkdir data"
# gcloud compute ssh --zone=$random_gcp_zone $2 --command "gsutil -m cp -r gs://$4/`date '+%Y-%m-%d'`/job-url/ ./data/"
gcloud compute ssh --zone=$random_gcp_zone $2 --command "cd src && sudo bash requirements.sh"
gcloud compute ssh --zone=$random_gcp_zone $2 --command "cd src && sudo python3 $5" #$6" #  > ../data/$(date "+%Y-%m-%d-%H-%M-%S-")nohup-$5-indeed.out
# gcloud compute ssh --zone=$random_gcp_zone $2 --command "cd src && gsutil -m mv -r ../data/*.csv gs://$4/$(date "+%Y-%m-%d")/data/"
gcloud compute ssh --zone=$random_gcp_zone $2 --command "cd src && sudo gsutil -m mv -r ../data/*.csv gs://$4/$(date "+%Y-%m-%d")/job-url/"
# gcloud compute ssh --zone=$random_gcp_zone $2 --command "cd src && sudo gsutil -m mv -r ../data/*.out gs://$4/$(date "+%Y-%m-%d")/logs/"

gcloud compute ssh --zone=$random_gcp_zone $2 --command "sleep 10"
gcloud compute instances stop $2 --zone=$random_gcp_zone
sleep 30
yes 'y' | gcloud compute instances delete $2 --zone=$random_gcp_zone
