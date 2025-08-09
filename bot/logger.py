import os, csv, time

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def log_decision(csv_dir, symbol, side, reason, price):
    ensure_dir(csv_dir)
    fn = os.path.join(csv_dir, "decisions.csv")
    new = not os.path.exists(fn)
    with open(fn, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts","symbol","side","reason","price"])
        w.writerow([int(time.time()), symbol, side, reason, price])

def log_trade(csv_dir, side, price, qty, fee, mode):
    ensure_dir(csv_dir)
    fn = os.path.join(csv_dir, "trades.csv")
    new = not os.path.exists(fn)
    with open(fn, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts","mode","side","price","qty","fee"])
        w.writerow([int(time.time()), mode, side, price, qty, fee])
