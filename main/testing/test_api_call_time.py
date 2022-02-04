import requests
import asyncio
from aiohttp import ClientSession
from functools import wraps
from time import time


URL = "https://httpbin.org/delay/{}"


def duration(func):
    async def helper(func, *args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            print(f"this function is a coroutine: {func.__name__}")
            return await func(*args, **kwargs)
        else:
            print(f"not a coroutine: {func.__name__}")
            return func(*args, **kwargs)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_ts = time()
        result = await helper(func, *args, **kwargs)
        dur = time() - start_ts
        print("{} took {:.2} seconds".format(func.__name__, dur))

        return result

    return wrapper


@duration
async def _get_completed():
    async with ClientSession() as session:
        tasks = [
            session.get(URL.format(delay)) for delay in [2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        responses = await asyncio.gather(*tasks)
        rs = [await response.json() for response in responses]
    return rs


def get_completed():
    """async call to get all of the completed challanges and their metadata in json format."""
    return asyncio.get_event_loop().run_until_complete(_get_completed())


@duration
def sync_get():
    resp = [requests.get(URL.format(delay)) for delay in [1, 1, 1, 1, 1]]
    return resp


if __name__ == "__main__":
    get_completed()
