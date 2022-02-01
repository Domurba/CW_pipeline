FROM postgres
ENV TZ="UTC"
ENV PG_TZ="UTC"
COPY load_ext.sh /docker-entrypoint-initdb.d/
RUN chmod 755 /docker-entrypoint-initdb.d/load_ext.sh
COPY create_tables.sql /docker-entrypoint-initdb.d/
RUN chmod 755 /docker-entrypoint-initdb.d/create_tables.sql