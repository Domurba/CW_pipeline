import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0] / "DATABASE"))

from DATABASE.to_DB_and_files import _user_to_db, _katas_to_db, _make_dirs, _db_to_files


if __name__ == "__main__":

    def run_pipeline_in_order(Username):
        _user_to_db(Username)
        _katas_to_db(Username)
        _make_dirs()
        _db_to_files()

    user = input("Enter username (case sensitive): ") or "Kolhelma"
    run_pipeline_in_order(user)
