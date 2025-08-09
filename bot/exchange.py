import os
import ccxt
from dotenv import load_dotenv

load_dotenv()

def make_exchange():
    env = os.getenv("ENVIRONMENT", "paper").lower()
    api_key = os.getenv("KRAKEN_API_KEY", "")
    api_secret = os.getenv("KRAKEN_API_SECRET", "")
    kraken = ccxt.kraken({
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True,
        "options": {"adjustForTimeDifference": True}
    })
    return kraken, env
