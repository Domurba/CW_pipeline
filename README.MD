# Codewars coding exercise solutions pipeline

###### Makes asynchronous API requests, scrapes the Codewars website for solutions, stores data into Postgres database, creates directories, stores files with those solutions and analyses data with Spark.

# Prerequisites
[Docker](https://docs.docker.com/get-docker/)  
[Python 3.9+](https://www.python.org/)  
[Docker-compose](https://docs.docker.com/compose/install/)  

# Runing project (in the project directory)
1. Build project infrastructure (Postgres, pgAdmin, Spark)
  ```sh
  docker-compose -f ./docker/Docker-compose.yaml up
  ```

2. Set user Cookie values in order to scrape users solutions  
- ./main/SCRAPER should have a ".env" file with cookie and header values  
COOKIE=value  
TOKEN=value  
AUTH=value  

3. Install requirements. In your shell type
  ```sh
  pip install -r requirements.txt
  ```

4. Run main.py with your username as the argument!
  ```sh
  py main/main.py
  ```

5. Analyse data stored in Postgres using Spark through
  ```sh
  http://localhost:8888/notebooks
  ```

6. Stop project infrastructure
  ```sh
  docker-compose -f ./docker/Docker-compose.yaml down
  ```

- Remove volumes (Optional)
  ```sh 
  docker volume prune
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
- Mount bind at  
../main/SPARK://home/jovyan/work
   
## Variables can be changed with a ".env" file in the same docker directory
- Example of the ".env" file:  
    POSTGRES_USER=value_you_choose  
    POSTGRES_PASSWORD=value_you_choose  
    PGADMIN_DEFAULT_EMAIL=value_you_choose  
    PGADMIN_DEFAULT_PASSWORD=value_you_choose  
    PG_CONTAINER_NAME=value_you_choose  