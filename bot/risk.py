def position_size(equity_usdt: float, max_fraction: float, price: float):
    notional = equity_usdt * max_fraction
    if price <= 0:
        return 0.0
    qty = notional / price
    return round(qty, 6)
