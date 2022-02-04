# Codewars coding exercise solutions pipeline

###### Makes asynchronous API requests, scrapes the Codewars website for solutions, stores data into Postgres database, creates directories, stores files with those solutions and analyses data with Spark.
###### Requests are only made to entires non-existent in the DB, so subsequent runs of the program are FAST!

# Prerequisites
[Docker](https://docs.docker.com/get-docker/)  
[Python 3.9+](https://www.python.org/)  
[Docker-compose](https://docs.docker.com/compose/install/)  

# Before starting, you have the option to change the default container values. If you choose to, please read the last section of this README document.


# Runing project (in the project directory)
1. Build project infrastructure (Postgres, pgAdmin, Spark, Airflow)
  ```sh
  docker-compose -f ./docker/Docker-compose.yaml build
  docker-compose -f ./docker/Docker-compose.yaml up
  ```

2. Scraping requires cookie values, if none are set, scraping is skipped.

Create a ".env" file in the "./main/AIRFLOW/plugins" directory with the format:

COOKIE=choosen_value  
TOKEN=choosen_value  
AUTH=choosen_value  

If you changed the default Postgres container variables, paste them below the cookie values 

POSTGRES_USER=choosen_value  
POSTGRES_PASSWORD=choosen_value  
POSTGRES_CONTAINER_NAME=choosen_value

3. Install requirements
  ```sh
  pip install -r requirements.txt
  ```

4. Run main.py. Press ENTER for default username.
  ```sh
  py main/main.py
  ```

5. Analyse data stored in Postgres using Spark from
  ```sh
  http://localhost:8888/notebooks
  ```

6. For Airflow ETL pipeline configuration, you need to:  
- Create a ".env" file in "./main/AIRFLOW/dags" and paste YOUR git repository ssh url  

  ```sh
  GIT_REPO_SHH_URL=git@github.com:USERNAME/REPO.git
  ```

7. Check that your git SSH keys are locted in the "~/.ssh" folder  
- **Docker creates a bind mount, so Airflow has permission to push**

7. Start the DAG from webserver
  ```sh
  http://localhost:8080/
  ```

6. When done, stop project infrastructure
  ```sh
  docker-compose -f ./docker/Docker-compose.yaml down
  ```

- Remove volumes (Optional)
  ```sh 
  docker volume prune
  ```

- Shutdown Windows Subsystem for Linux (optional)
  ```sh 
  wsl --shutdown
  ```
# Links to services
###### pgAdmin
  ```sh
  http://localhost:5050/
  ```
- Default email: **example@email.com**  
- Default password: **admin**  

###### AIRFLOW 
  ```sh
  http://localhost:8080/
  ```
- Default username: **airflow**
- Default password: **airflow**

###### Postgres Server info
- Default host name (Docker container name): **postgres**
- Default port: **5432**
- Default server name (value of the "POSTGRES_USER" variable): **postgres**
- Default username: **postgres**
- Defaul password: **postgres**
###### Jupyter notebook for Spark
  ```sh
  http://localhost:8888/notebooks
  ```
- If prompted for a token, it will appear in the terminal where you ran docker-compose, e.g.  
http://127.0.0.1:8888/lab?token=bf3a23263e3ff416c2aaf99d4b8e51d49bc97c5d9239173b
- Spark file Bind Mount  
**../main/SPARK://home/jovyan/work**
   
## You can create three ".env" files. It is the users job to make sure that the postgres container variables are consistent!
1. first one in the "./docker" directory  

POSTGRES_USER=choosen_value  
POSTGRES_PASSWORD=choosen_value  
POSTGRES_CONTAINER_NAME=choosen_value  
PGADMIN_DEFAULT_EMAIL=choosen_value  
PGADMIN_DEFAULT_PASSWORD=choosen_value  
_AIRFLOW_WWW_USER_USERNAME=choosen_value  
_AIRFLOW_WWW_USER_PASSWORD=choosen_value  

2. second one in the "./main/AIRFLOW/plugins" directory

COOKIE=choosen_value  
TOKEN=choosen_value 
AUTH=choosen_value
POSTGRES_USER=choosen_value
POSTGRES_PASSWORD=choosen_value 
POSTGRES_CONTAINER_NAME=choosen_value

3. third one in the "./main/AIRFLOW/dags" directory  

GIT_REPO_SHH_URL=git@github.com:USERNAME/REPO.git