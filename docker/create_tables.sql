CREATE ROLE airflow LOGIN SUPERUSER PASSWORD 'airflow';
CREATE DATABASE airflow
    WITH 
    OWNER = airflow
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

\connect postgres;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS Ranks (
  Rank_id SMALLINT PRIMARY KEY,
  Rank_name CHAR(5) UNIQUE
);

CREATE TABLE IF NOT EXISTS Katas (
 -- Kata_id taken from json api response
  Kata_id VARCHAR(255) PRIMARY KEY,
  Kata_name VARCHAR(255) UNIQUE,
  Rank_id SMALLINT,
  Kata_description TEXT NOT NULL,
  CONSTRAINT fk_kata_rank
        FOREIGN KEY(Rank_id) 
            REFERENCES Ranks(Rank_id) 
);

CREATE TABLE IF NOT EXISTS Languages (
  Language_id SERIAL PRIMARY KEY,
  Prog_language VARCHAR(55) UNIQUE
);

CREATE TABLE IF NOT EXISTS Users (
  User_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  Rank_id SMALLINT NOT NULL,
  Username VARCHAR(255) UNIQUE, 
  Honor INT,
  LB_position INT UNIQUE,
  Total_solved SMALLINT,
    CONSTRAINT fk_rank
        FOREIGN KEY(Rank_id) 
            REFERENCES Ranks(Rank_id) 
            ON DELETE RESTRICT
            ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS User_Languages (
  Language_id SMALLINT,
  User_id UUID,
    CONSTRAINT fk_lang FOREIGN KEY(Language_id) REFERENCES Languages(Language_id),
    CONSTRAINT fk_userid FOREIGN KEY(User_id) REFERENCES Users(User_id),
  PRIMARY KEY (Language_id, User_id)
);

CREATE TABLE IF NOT EXISTS Kata_Solutions (
  Kata_id VARCHAR(255),
  User_id UUID,
  Language_id SMALLINT,
  Completed_at TIMESTAMPTZ,
  Solution TEXT NOT NULL,
    CONSTRAINT fk_kata FOREIGN KEY(Kata_id) REFERENCES Katas(Kata_id),
    CONSTRAINT fk_userid FOREIGN KEY(User_id) REFERENCES Users(User_id),
    CONSTRAINT fk_lang FOREIGN KEY(Language_id) REFERENCES Languages(Language_id),
    PRIMARY KEY (User_id, Kata_id, Language_id)
);


INSERT INTO Ranks (Rank_id, Rank_name) VALUES (2, '2 dan'),(1, '1 dan'),(-1, '1 kyu'),(-2, '2 kyu'),(-3, '3 kyu'),(-4, '4 kyu'),(-5, '5 kyu'),(-6, '6 kyu'),(-7, '7 kyu'),(-8, '8 kyu');

CREATE OR REPLACE VIEW kata_info_view_OLAP as
SELECT u.username, k.kata_name, r.rank_name, l.prog_language, ks.completed_at
FROM kata_solutions ks
JOIN katas k USING(kata_id)
JOIN ranks r USING(rank_id)
JOIN users u USING(user_id)
JOIN languages l USING(language_id);