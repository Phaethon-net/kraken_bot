import pandas as pd

def fetch_ohlcv(exchange, symbol: str, timeframe: str, limit: int = 500):
    candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(candles, columns=["ts","open","high","low","close","volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    return df

def tail_merge(old: pd.DataFrame, new: pd.DataFrame, key="ts"):
    if old is None or old.empty:
        return new
    return pd.concat([old, new]).drop_duplicates(subset=[key]).sort_values(key).reset_index(drop=True)
