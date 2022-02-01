import sys
from pathlib import Path
import subprocess

sys.path.append(str(Path(__file__).parents[0] / "DATABASE"))

from DATABASE.to_DB_and_files import _user_to_db, _katas_to_db, _make_dirs, _db_to_files

if __name__ == "__main__":
    _user_to_db("Kolhelma")
    _katas_to_db("Kolhelma")
    _make_dirs()
    _db_to_files()
