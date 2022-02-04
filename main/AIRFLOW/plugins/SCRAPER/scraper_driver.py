import asyncio
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from re import search
from json import loads

from scraper_info import HEADERS

URL = "https://www.codewars.com/kata/{}/train"


async def _get_page(session, url):
    async with session.get(url) as r:
        return await r.text()


async def _seshion(ids):
    async with ClientSession(headers=HEADERS) as ses:
        tasks = [asyncio.create_task(_get_page(ses, URL.format(idk))) for idk in ids]
        return await asyncio.gather(*tasks)


def _parse(result):
    soup = BeautifulSoup(result, features="html.parser").find_all("script")[-2].text
    js = search(r"data: JSON.parse\(\"(.*?)\"\),\n", soup).groups(1)[0]
    dic = loads(js.encode("utf-8", "backslashreplace").decode("unicode-escape"))
    return [(i["language"].lower(), *i["solutions"]) for i in dic["previousSolutions"]]


def get_solutions(ids: list) -> list:
    """Returns a generator of kata solutions.
    IMPORTANT! Header info located in (--SCRAPER > scraper_info.py--) must be set for the user whose solutions are being retrieved.
    Each item in the generator is a list and it may contain more than one solution in different languages. In addition, there might be multiple solutions in each language!
    Solutions are of format [('Language1', 'Solution1', Solution2), ('Language2', 'Solution3', Solution4)]"""
    for html_page in asyncio.get_event_loop().run_until_complete(_seshion(ids)):
        yield _parse(html_page)
