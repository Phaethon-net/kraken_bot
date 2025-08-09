import os, time, yaml
import pandas as pd
from .exchange import make_exchange
from .data import fetch_ohlcv
from .strategy import add_indicators, generate_signal
from .risk import position_size
from .execution import paper_execute, live_place_order
from .logger import log_decision, log_trade
from .storage import init_db, insert_trade

def load_config():
    with open("config.yaml","r") as f:
        return yaml.safe_load(f)

def get_equity_usdt(exchange):
    try:
        bal = exchange.fetch_balance()
        usdt = bal.get("USDT", {}).get("free", 0.0)
        return float(usdt or 0.0)
    except Exception:
        return 100.0  # assume paper equity if no keys

def main():
    cfg = load_config()
    symbol = cfg["exchange"]["pair"]
    tf = cfg["exchange"]["timeframe_entry"]
    max_fraction = cfg["risk"]["max_position_fraction"]
    csv_dir = cfg["storage"]["csv_dir"]
    db_path = cfg["storage"]["db_path"]

    exchange, env = make_exchange()
    con = init_db(db_path)

    print(f"Mode: {env} | Symbol: {symbol} | Timeframe: {tf}")
    while True:
        try:
            df = fetch_ohlcv(exchange, symbol, tf, limit=200)
            df = add_indicators(df)
            sig = generate_signal(df)
            last_price = float(df.iloc[-1]["close"])
            if sig:
                log_decision(csv_dir, symbol, sig["side"], sig["reason"], last_price)
                equity = get_equity_usdt(exchange)
                qty = position_size(equity, max_fraction, last_price)
                if qty > 0:
                    if env == "paper":
                        tr = paper_execute({}, sig["side"], last_price, qty)
                        log_trade(csv_dir, tr["side"], last_price, qty, tr["fee"], env)
                        insert_trade(con, int(time.time()), env, tr["side"], last_price, qty, tr["fee"])
                        print(f"[PAPER] {tr}")
                    else:
                        order = live_place_order(exchange, symbol, sig["side"], qty)
                        log_trade(csv_dir, sig["side"], last_price, qty, 0.0, env)
                        insert_trade(con, int(time.time()), env, sig["side"], last_price, qty, 0.0)
                        print(f"[LIVE] Placed {sig['side']} {qty} {symbol}")
            time.sleep(30)
        except Exception as e:
            print("Error:", e)
            time.sleep(10)
