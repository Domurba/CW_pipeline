# Codewars coding exercise solutions pipeline

###### Makes asynchronous API requests, scrapes the Codewars website for solutions, stores data into Postgres database, creates directories, stores files with those solutions and analyses data with Spark.
###### Requests are only made to entires non-existent in the DB, so subsequent runs of the program are FAST!

# Prerequisites
[Docker](https://docs.docker.com/get-docker/)  
[Python 3.9+](https://www.python.org/)  
[Docker-compose](https://docs.docker.com/compose/install/)  

# Before starting docker, you can change the environment variables (Optional)
In "./docker" create a ".env" file with the format:  
POSTGRES_USER=choosen_value  
POSTGRES_PASSWORD=choosen_value  
POSTGRES_CONTAINER_NAME=choosen_value  
PGADMIN_DEFAULT_EMAIL=choosen_value  
PGADMIN_DEFAULT_PASSWORD=choosen_value  
_AIRFLOW_WWW_USER_USERNAME=choosen_value  
_AIRFLOW_WWW_USER_PASSWORD=choosen_value  

# Runing project (in the project directory)
1. Build project infrastructure (Postgres, pgAdmin, Spark, Airflow)
  ```sh
  docker-compose -f ./docker/Docker-compose.yaml build
  docker-compose -f ./docker/Docker-compose.yaml up
  ```

2. Set user Cookie values in order to scrape users solutions  
- If ".env" file in "./main/AIRFLOW/plugins does not exist, solutions scraping is skipped.
- ./main/SCRAPER should have a ".env" file with cookie and header values  
COOKIE=choosen_value  
TOKEN=choosen_value  
AUTH=choosen_value  

In addtion, if you changed the default Postgres container values, add them in this file, below cookie values  

POSTGRES_USER=choosen_value  
POSTGRES_PASSWORD=choosen_value  
POSTGRES_CONTAINER_NAME=choosen_value

3. Install requirements
  ```sh
  pip install -r requirements.txt
  ```

4. Run main.py in the parent directory. You will be prompted for a username. Press ENTER for default
  ```sh
  py main/main.py
  ```

5. Analyse data stored in Postgres using Spark from
  ```sh
  http://localhost:8888/notebooks
  ```

6. For Airflow ETL pipeline configuration, you need to:  
- Create a ".env" file in "./main/AIRFLOW/dags" and paste YOUR git repo ssh url
  ```sh
  GIT_REPO_SHH_URL=git@github.com:USERNAME/REPO.git
  ```
- Check that you git SSH keys are locted in "~/.ssh" folder.  
A bind mout will be created with that folder, so Airflow will have permission to push.

7. Start the DAG
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
    http://localhost:5050/
- Default email
  ```sh
  example@email.com
   ```
- Default password
  ```sh
  admin
  ```
###### AIRFLOW 
  ```sh
  http://localhost:8080/
  ```
  Default username
  ```sh
  airflow
  ```
- Default password
  ```sh
  airflow
  ```
###### Postgres Server info
- Default host name (Docker container name): postgres
- Default port: 5432
- Default server name (value of the "POSTGRES_USER" variable): postgres
- Default username: postgres
- Defaul password: postgres
###### Jupyter notebook for Spark
- URL  
    http://localhost:8888/notebooks
- If prompted for a token, it will appear in the terminal where you ran docker-compose, e.g.  
http://127.0.0.1:8888/lab?token=bf3a23263e3ff416c2aaf99d4b8e51d49bc97c5d9239173b
- Spark file Bind Mount  
../main/SPARK://home/jovyan/work
   
## Variables can be changed with a ".env" file in the same docker directory
- Example of the ".env" file:  
    POSTGRES_USER=value_you_choose  
    POSTGRES_PASSWORD=value_you_choose  
    PGADMIN_DEFAULT_EMAIL=value_you_choose  
    PGADMIN_DEFAULT_PASSWORD=value_you_choose  
    PG_CONTAINER_NAME=value_you_choose  
    _AIRFLOW_WWW_USER_USERNAME=airflow  
    _AIRFLOW_WWW_USER_PASSWORD=airflow  