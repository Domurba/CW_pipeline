import sys
from pathlib import Path
from contextlib import contextmanager
from psycopg2.extras import execute_values
from itertools import groupby
from re import sub

sys.path.append(str(Path(__file__).parents[1] / "API"))
sys.path.append(str(Path(__file__).parents[1] / "SCRAPER"))

from scraper_driver import get_solutions
from api_call import get_user, generate_completed, gen_desc
from db_pool import db


@contextmanager
def _get_con_cur():
    con = db.getconn()
    cur = con.cursor()
    try:
        yield con, cur
    except (Exception) as error:
        print("Rollback! Could not get connection from pool: ", error)
        con.rollback()
        raise
    finally:
        con.commit()
        cur.close()
        db.putconn(con)


def _user_to_db(username: str) -> None:
    """Fetches a connection from connection pool and upserts: to Users and users_languages tables.
    Languages table has ON CONFLICT DO NOTHING, so these errors will be silenced and wont interfere with other parts of the insert.
    In case user is already inserted into DB, Users table has ON CONFLICT UPDATE, which updates: rank_id, Honor, LB_position, Total_solved."""
    with _get_con_cur() as (con, cur):
        try:
            # API call to retrieve user info used in the INSERTS
            print(f"API call to retrieve latest user info for user: {username}")
            user_info = get_user(username)

            # INSERTS or UPDATES languages used by the user into languages table
            user_info_args = ",".join(
                cur.mogrify("(%s)", (x,)).decode("utf-8") for x in user_info[5:]
            )
            print("Upserting languages table")
            cur.execute(
                "INSERT INTO languages (prog_language) VALUES"
                + user_info_args
                + "ON CONFLICT DO NOTHING"
            )
            print(f"Upserting Users table for user: {username}")
            # INSERTS or UPDATES Users table, RETURNING UID for further inserts into the userlanguages table
            cur.execute(
                """
                INSERT INTO Users (Rank_id, Username, Honor, LB_position, Total_solved) 
                VALUES ((SELECT rank_id FROM Ranks WHERE rank_name = %s),  %s, %s,%s,%s) 
                ON CONFLICT (Username) DO UPDATE SET 
                (Rank_id, Honor, LB_position, Total_solved) = (EXCLUDED.Rank_id, EXCLUDED.Honor, EXCLUDED.LB_position, EXCLUDED.Total_solved) 
                RETURNING User_id as UID;
                """,
                user_info[:5],
            )

            # Previous INSERT returns UID
            # We fetch it and use it to construct an INSERT into user_languages Table

            uid = cur.fetchone()[0]
            lang_args = ",".join(
                cur.mogrify(
                    "((SELECT language_id FROM languages WHERE languages.prog_language = %s) , %s)",
                    (x, uid),
                ).decode("utf-8")
                for x in user_info[5:]
            )

            print(f"Upserting user_languages table for user: {username}")
            cur.execute(
                "INSERT INTO user_languages VALUES"
                + lang_args
                + "ON CONFLICT DO NOTHING"
            )

        except (Exception) as error:
            print("Error while commiting PostgreSQL", error, "Rolling back")
            con.rollback()


def _katas_to_db(username: str, page_size=500) -> None:
    """Adds new Katas to the Katas table and solutions to kata_solutions table.
    COMPLETED_AT is only valid for the first time the kata was completed.
    Subsequent completions in different languages will share one timestamp."""
    with _get_con_cur() as (con, cur):
        try:
            cur.execute(
                "SELECT Total_solved, User_id FROM Users where Username = %s",
                (username,),
            )
            total_solved, uuid = cur.fetchone()
            print(f"API call to retrieve completed katas for user: {username}")
            # Solved katas are put in a list, because the generator would become exhausted and we will use this info multiple times
            solved = list(generate_completed(username, total_solved))

            # Sets are used to see which katas are not in the Katas table. API calls are only made to the non-existing Katas.
            unique_kata_ids = {id[0] for id in solved}

            cur.execute("SELECT kata_id FROM katas")
            existing_ids = {id[0] for id in cur.fetchall()}

            new_kata_ids = unique_kata_ids - existing_ids
            print("API call to get descriptions of katas not in DB")
            # We need to dereference the tuple received from 'gen_desc' function
            gen = ((x, *y) for (x, y) in zip(new_kata_ids, gen_desc(new_kata_ids)))
            print("Upserting katas table")
            execute_values(
                cur,
                "INSERT INTO katas VALUES %s ON CONFLICT DO NOTHING",
                gen,
                template="(%s,%s,%s,%s)",
                page_size=min(total_solved, page_size),
            )

            # Inserting kata solutions into KATA_SOLUTIONS table.
            cur.execute(
                """
            SELECT kata_id, user_id, to_char(completed_at, 'YYYY-MM-DD\"T\"HH24:MI:SS.MSZ'), 
            ARRAY_AGG(prog_language) FROM kata_solutions 
            JOIN languages USING(language_id)
            GROUP BY kata_id, user_id, completed_at"""
            )
            print(f"Check for already existing kata solutions by user: {username}")
            db_kid_uuid_ts_lang = {
                (*ids[:3], tuple(sorted(ids[3]))) for ids in cur.fetchall()
            }

            api_kid_uuid_ts_lang = {
                (sol[0], uuid, sol[2], tuple(sorted(sol[3]))) for sol in solved
            }

            new = api_kid_uuid_ts_lang - db_kid_uuid_ts_lang
            print("Scraping solutions that are not yet in the DB")
            solutions = get_solutions((i[0] for i in new))

            # Generator returns solutions in format (kata_id, PROG_LANGUAGE (not ID!), completed_at, *Solutions)
            gen = (
                (meta_info[0], lang_sol[0], meta_info[2], lang_sol[1:])
                for (meta_info, sol) in zip(new, solutions)
                for lang_sol in sol
            )
            print(f"Upserting kata_solutions table for user {username}")
            execute_values(
                cur,
                "INSERT INTO kata_solutions VALUES %s ON CONFLICT DO NOTHING",
                gen,
                template=f"(%s, '{uuid}', (SELECT language_id FROM languages WHERE languages.prog_language = %s), %s, %s)",
                page_size=200,
            )

        except (Exception) as error:
            print("Error while commiting PostgreSQL", error)
            con.rollback()


def _make_dirs():
    """Creates directories for the distinct combinations of programing language and ranks"""
    with _get_con_cur() as (con, cur):

        cur.execute(
            """SELECT DISTINCT prog_language, rank_name FROM kata_solutions 
                JOIN languages USING(language_id)
                JOIN katas USING(kata_id)
                JOIN ranks USING(rank_id)
                ORDER BY prog_language, rank_name;"""
        )
        print("Creating directories...")
        folder = Path(__file__).parents[3] / "Push_to_github"
        for lang, ranks in groupby(cur.fetchall(), lambda x: x[0]):
            Path(folder / lang).mkdir(parents=True, exist_ok=True)
            for rank in ranks:
                Path(folder / lang / rank[1].replace(" ", "_")).mkdir(
                    parents=True, exist_ok=True
                )


def _db_to_files():
    """Fetches solved katas and creates files in the corresponding directories (prog lang -> rank)"""
    with _get_con_cur() as (con, cur):

        cur.itersize = 10000
        cur.execute(
            """SELECT prog_language, rank_name, username, kata_name, kata_description, completed_at, solution  FROM kata_solutions 
                    JOIN languages USING(language_id)
                    JOIN katas USING(kata_id)
                    JOIN ranks USING(rank_id)
                    JOIN users USING(user_id)"""
        )

        folder = Path(__file__).parents[3] / "Push_to_github"
        extentions = {"python": "py", "shell": "sh", "sql": "sql"}
        print("Creating script files for all solutions...")
        for sol in cur:
            f_dir = (
                folder
                / sol[0]
                / sol[1].replace(" ", "_")
                / "{}--by_{}--.{}".format(
                    sub("[^a-zA-Z0-9 \.]", "", sol[3]).replace(" ", "_"),
                    sol[2],
                    extentions.get(sol[0], "txt"),
                )
            )
            if not f_dir.is_file():
                with open(f_dir, "w", encoding="utf-8") as f:
                    f.write("#" + str(sol[5]) + "\n")
                    f.write('"""' + sol[4] + '"""' + "\n\n")
                    solut = sol[-1]
                    if not solut[0] == "(":
                        f.write(solut)
                    else:
                        f.write("\n\n".join(solut[2:-2].split('","')))
    print("Operation completed!")


if __name__ == "__main__":
    # _user_to_db("Kolhelma")
    # _katas_to_db("Kolhelma")
    # _make_dirs()
    # _db_to_py()
    pass
