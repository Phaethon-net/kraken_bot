def paper_execute(state, side, price, qty):
    fill_price = price
    fee = 0.0006 * qty * fill_price  # placeholder fee model
    return {"price": fill_price, "qty": qty, "fee": fee, "side": side}
    
def live_place_order(exchange, symbol, side, qty, price=None, params=None):
    if price is None:
        order = exchange.create_order(symbol=symbol, type="market", side=side, amount=qty)
    else:
        order = exchange.create_order(symbol=symbol, type="limit", side=side, amount=qty, price=price, params=params or {})
    return order
