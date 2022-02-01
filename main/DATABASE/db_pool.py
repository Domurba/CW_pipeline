import dotv
from psycopg2 import pool, DatabaseError


"""Create a threaded Pool on import called db"""

try:
    db = pool.ThreadedConnectionPool(3, 6, dotv.get_uri())
    if db:
        print("Connection pool created successfully")
except (Exception, DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)
