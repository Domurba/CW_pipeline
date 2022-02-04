FROM apache/airflow:2.2.3-python3.9
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt . 
RUN pip install -r requirements.txt
USER root
RUN apt-get update && apt-get install -y git
USER airflow
RUN mkdir /home/airflow/.ssh
RUN git config --global core.autocrlf true
RUN git config --global user.name "DU" 
RUN git config --global user.email DU@gmail.com
