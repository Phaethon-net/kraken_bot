import os
import csv
import time
import krakenex
from datetime import datetime

# CONFIG
LOG_FILE = os.path.join("logs", "balances.csv")
INTERVAL = 300  # seconds (5 min)

# Kraken API init
api = krakenex.API()
api.load_key("kraken.key")  # file with your public/secret API keys

def get_balances():
    # Raw balances
    res = api.query_private("Balance")
    if res.get("error"):
        print(f"[ERROR] {res['error']}")
        return None
    return res["result"]

def log_balances():
    balances = get_balances()
    if not balances:
        return
    now = datetime.utcnow().isoformat()

    # Prepare row: time, asset1, asset2..., total_BTC, total_USD
    # For simplicity, no price conversion here; add if you want live value
    row = {"timestamp": now, **balances}

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"[{now}] Logged balances: {balances}")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    print(f"Logging balances every {INTERVAL} seconds...")
    while True:
        log_balances()
        time.sleep(INTERVAL)
