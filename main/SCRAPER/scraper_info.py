from dotenv import load_dotenv
import os

load_dotenv()

HEADERS = {
    "authority": "www.codewars.com",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "dnt": "1",
    "x-csrf-token": os.getenv("TOKEN"),
    "sec-ch-ua-mobile": "?0",
    "authorization": os.getenv("AUTH"),
    "accept": "application/json, text/plain, */*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://www.codewars.com/dashboard",
    "accept-language": "en-US,en;q=0.9,lt-LT;q=0.8,lt;q=0.7,be;q=0.6,he;q=0.5",
    "cookie": os.getenv("COOKIE"),
}
