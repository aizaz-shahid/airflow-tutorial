FROM puckel/docker-airflow:1.10.2

USER root
RUN groupadd --gid 999 docker \
    && usermod -aG docker airflow \
    &&pip install psycopg2 \
    && pip install psycopg2-binary
RUN apt-get update && \
    apt-get -y install sudo
RUN echo 'airflow:airflow' | chpasswd && adduser airflow sudo \
    && sudo gpasswd -a airflow docker

# RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
# RUN sudo apt-get install apt-transport-https ca-certificates gnupg
# RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
# RUN sudo apt-get update && sudo apt-get install google-cloud-sdk
# RUN sudo apt-get install openssh-server
# RUN sudo service ssh restart
# RUN gcloud auth login
# RUN gcloud config set project dentaway-01
USER airflow