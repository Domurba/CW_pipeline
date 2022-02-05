# Codewars coding exercise solutions pipeline

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#optional-parameters">Optional parameters</a></li>
      </ul>      
    </li>
    <li><a href="#Runing-the-project">Runing the project</a></li>
    <li><a href="#Docker-services-info">Docker services info</a></li>
    <li><a href="#env-files">env files</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
**Python** asynchronously calls the API, scrapes the website for solutions, stores the data into a Postgres DB, creates directories and files with kata descriptions and solutions.  

**Spark** connects to the Postgres DB, fetches the data, transforms it and creates charts with the help of **matplotlib**.  

**Airflow** starts the ETL process and pushes changes to your Github repository!  

In addition, requests are only made to non-existent entries in the DB, so subsequent runs of the program are much faster!  
Database tables are upserted with missing values only.

DB ERD

![ERD 2022-01-28](https://user-images.githubusercontent.com/91464837/152539725-cc57f4b1-0fc1-435f-b979-776b2f05741f.png)

Airflow DAG

![Airflow graph](https://user-images.githubusercontent.com/91464837/152539805-d5d91885-aa65-49a0-9301-0e14d52f6873.png)

Airflow runs

![Airflow ETL](https://user-images.githubusercontent.com/91464837/152539843-f6cc309d-b698-465c-8ef3-169bbf390340.png)

### Prerequisites
[Docker](https://docs.docker.com/get-docker/)  
[Python 3.9+](https://www.python.org/)  
[Docker-compose](https://docs.docker.com/compose/install/)  

### Optional parameters
Before running docker compose, you have the option to change the default container values. If you choose to, please read the last section of this README document.


# Running the project
1. In parent directory, build the project infrastructure (Postgres, pgAdmin, Spark, Airflow)
  ```sh
  docker-compose -f ./docker/Docker-compose.yaml build
  docker-compose -f ./docker/Docker-compose.yaml up
  ```

2. Scraping requires cookie values, if none are set, scraping is skipped

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

5. Analyse data using Spark
  ```sh
  http://localhost:8888/notebooks
  ```

6. Airflow pipeline requires YOUR git repository SSH URL  

create a ".env" file in the "./main/AIRFLOW/dags" directory
  ```sh
  GIT_REPO_SHH_URL=git@github.com:USERNAME/REPO.git
  ```

7. Check that your git SSH keys are locted in the "~/.ssh" folder  
- **Docker creates a bind mount, so Airflow has permission to push**

8. Start the DAG from webserver
  ```sh
  http://localhost:8080/
  ```

9. When done, stop project infrastructure
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
## Docker services info
###### Postgres Server info
- Default host name (Docker container name): **postgres**
- Default port: **5432**
- Default server name (value of the "POSTGRES_USER" variable): **postgres**
- Default username: **postgres**
- Defaul password: **postgres**

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

###### Jupyter notebook for Spark
  ```sh
  http://localhost:8888/notebooks
  ```
- If prompted for a token, it will appear in the terminal where you ran docker-compose, e.g.  
http://127.0.0.1:8888/lab?token=bf3a23263e3ff416c2aaf99d4b8e51d49bc97c5d9239173b
- Spark file Bind Mount at: **../main/SPARK://home/jovyan/work**
   
## env files
###### You can create three ".env" files. It is the users job to make sure that the postgres container variables are consistent!
1. The first one in the "./docker" dir.

  POSTGRES_USER=choosen_value  
  POSTGRES_PASSWORD=choosen_value  
  POSTGRES_CONTAINER_NAME=choosen_value  
  PGADMIN_DEFAULT_EMAIL=choosen_value  
  PGADMIN_DEFAULT_PASSWORD=choosen_value  
  _AIRFLOW_WWW_USER_USERNAME=choosen_value  
  _AIRFLOW_WWW_USER_PASSWORD=choosen_value  

2. The second one in the "./main/AIRFLOW/plugins" dir.

  COOKIE=choosen_value  
  TOKEN=choosen_value  
  AUTH=choosen_value  
  POSTGRES_USER=choosen_value  
  POSTGRES_PASSWORD=choosen_value  
  POSTGRES_CONTAINER_NAME=choosen_value  

3. The third one in the "./main/AIRFLOW/dags" dir. 

  GIT_REPO_SHH_URL=git@github.com:USERNAME/REPO.git
