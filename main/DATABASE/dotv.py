from dotenv import load_dotenv
from pathlib import Path
import os


def get_uri():
    """Returns DB conn info URI from .env file, which is used in by docker"""
    direc = Path(__file__).resolve().parents[2] / "docker" / ".env"
    load_dotenv(direc)
    return "postgresql://{}:{}@{}:{}/{}".format(
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        "localhost",
        "5432",
        os.getenv("POSTGRES_USER"),
    )
