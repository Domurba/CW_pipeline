import requests
import asyncio
from aiohttp import ClientSession
from math import ceil
from data_parser import *


URL = "https://www.codewars.com/api/v1/"


def get_user(name: str) -> tuple:
    """Returns: Rank, Username, Honor, LB_position, Total_solved, *Languages"""
    return user_from_dict(requests.get(URL + f"users/{name}").json())


async def _gather(CW_name: str, solved) -> dict:
    """Improvement: make this func a generator (if possible). A large response could cause memory issues
    One page contains 200 solutions, so math.ceil is used to round up"""
    if solved is None:
        solved = get_user(CW_name)[4]
    url_ch = URL + f"users/{CW_name}" + "/code-challenges/completed?page={}"
    async with ClientSession() as session:
        tasks = [session.get(url_ch.format(page)) for page in range(ceil(solved / 200))]
        responses = await asyncio.gather(*tasks)
        return [await response.json() for response in responses]


def generate_completed(CW_name: str, solved=None):
    """A generator of tuples for all completed challanges.
    Yields: Kata_id, Kata_name, Completed_at (conversion handled by Postges), *Language(s).
    By default, this function is called with solved=None, which means that we make an additional API call to the users endpoint.
    When storing solutions to DB, we retrieve the number of solved katas from DB."""
    for data in asyncio.get_event_loop().run_until_complete(_gather(CW_name, solved)):
        for kata in data["data"]:
            yield kata_from_dict(kata)


async def _get_kata_descr(ids) -> dict:
    url = URL + "code-challenges/{}"
    async with ClientSession() as session:
        tasks = [session.get(url.format(kata_id)) for kata_id in ids]
        responses = await asyncio.gather(*tasks)
        return [await response.json() for response in responses]


def gen_desc(ids):
    "Yields: Kata_rank_id, Description"
    for desc in asyncio.get_event_loop().run_until_complete(_get_kata_descr(ids)):
        yield kata_info_from_dict(desc)


if __name__ == "__main__":
    # either set below event loop policy or run until complete (known aiohttp error)

    # import sys
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # print(get_user("Kolhelma"))
    solved = list(generate_completed("Kolhelma", 260))
    print(solved)
    pass
