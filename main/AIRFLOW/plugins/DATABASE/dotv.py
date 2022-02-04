from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(Path(__file__).parents[1] / '.env')


def get_uri():
    """Returns DB conn info URI from .env file, which is used in by docker"""
    load_dotenv()
    return "postgresql://{}:{}@{}:{}/{}".format(
        os.getenv("POSTGRES_USER", "postgres"),
        os.getenv("POSTGRES_PASSWORD", "root"),
        os.getenv("POSTGRES_CONTAINER_NAME", "postgres"),
        "5432",
        os.getenv("POSTGRES_USER", "postgres"),
    )