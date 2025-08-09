import os, sqlite3

def init_db(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS trades(
        id INTEGER PRIMARY KEY,
        ts INTEGER,
        mode TEXT,
        side TEXT,
        price REAL,
        qty REAL,
        fee REAL
    );""")
    con.commit()
    return con

def insert_trade(con, ts, mode, side, price, qty, fee):
    con.execute("INSERT INTO trades(ts,mode,side,price,qty,fee) VALUES(?,?,?,?,?,?)",
                (ts, mode, side, price, qty, fee))
    con.commit()
