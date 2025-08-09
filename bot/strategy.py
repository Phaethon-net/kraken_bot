import pandas as pd
import numpy as np

def add_indicators(df: pd.DataFrame):
    df["ema_fast"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=50, adjust=False).mean()
    delta = df["close"].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    gain = up.ewm(alpha=1/14, adjust=False).mean()
    loss = down.ewm(alpha=1/14, adjust=False).mean()
    rs = gain / (loss.replace(0, np.nan))
    df["rsi"] = 100 - (100 / (1 + rs))
    df["rsi"] = df["rsi"].fillna(50)
    return df

def generate_signal(df: pd.DataFrame):
    if len(df) < 60:
        return None
    row = df.iloc[-1]
    prev = df.iloc[-2]
    cross_up = prev["ema_fast"] <= prev["ema_slow"] and row["ema_fast"] > row["ema_slow"]
    cross_dn = prev["ema_fast"] >= prev["ema_slow"] and row["ema_fast"] < row["ema_slow"]
    if cross_up and row["rsi"] < 70:
        return {"side": "buy", "reason": "ema_cross_up_rsi_ok"}
    if cross_dn and row["rsi"] > 30:
        return {"side": "sell", "reason": "ema_cross_dn_rsi_ok"}
    return None
