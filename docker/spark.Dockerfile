FROM jupyter/pyspark-notebook
ENV POST_URL=https://jdbc.postgresql.org/download/postgresql-42.3.1.jar
RUN wget ${POST_URL}
ENV SPARK_CLASSPATH=/home/jovyan/postgresql-42.3.1.jar