import requests, time

def gen():
    """Yield one BTC price record as a dictionary."""
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    
    response = requests.get(url)
    record = response.json()

    yield {
        "symbol": record["symbol"],
        "price": float(record["price"]),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
