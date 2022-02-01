--- PgAdmin4 info (used in dcDEV.yaml compose file) ---
email: PGADMIN_DEFAULT_EMAIL (Default - example@email.com)
password: PGADMIN_DEFAULT_PASSWORD (Default - admin)

--- Postgres Server info ---
Server name: POSTGRES_USER (Default - value of the "POSTGRES_USER" variable) 
Host name: postgres (It's the name of the Container)
Port: 5432
Username: POSTGRES_USER (Default - postgres)
Password: POSTGRES_PASSWORD (Default - postgres)

--- START ---
docker compose up -f dcPROD.yaml
Run: TODO

--- SHUTDOWN ---
docker compose down -f dcPROD.yaml
Delete volumes [Optional]: docker vomule prune
Delete containers [Optional]: docker container prune


--- Spark ---
http://localhost:8888/notebooks
If prompted for a token, it should appear in the terminal where you ran docker-compose. 
(e.g. http://127.0.0.1:8888/lab?token=bf3a23263e3ff416c2aaf99d4b8e51d49bc97c5d9239173b)
