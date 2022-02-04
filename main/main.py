import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0] / "DATABASE"))

from to_DB_and_files import run_pipeline_in_order

if __name__ == "__main__":
    user = input("Enter username (case sensitive): ") or "Kolhelma"
    run_pipeline_in_order(user)