import requests

#-------------------------------------------------------------   

url = "https://api.binance.com/api/v3/ticker/price"
params = {"symbol": "BTCUSDT"}  # Par de trading: BTC/USDT

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"Precio de BTC/USDT: {data['price']}")
else:
    print(f"Error: {response.status_code}")
    
    url = "https://api.binance.com/api/v3/depth"
params = {
    "symbol": "BTCUSDT",  # Par de trading: BTC/USDT
    "limit": 5            # Número de órdenes a mostrar
}

#-------------------------------------------------------------   

url = "https://api.binance.com/api/v3/depth"
params = {
    "symbol": "BTCUSDT",  # Par de trading: BTC/USDT
    "limit": 5            # Número de órdenes a mostrar
}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Órdenes de compra (Bids):")
    for bid in data['bids']:
        print(f"Precio: {bid[0]}, Cantidad: {bid[1]}")
    print("\nÓrdenes de venta (Asks):")
    for ask in data['asks']:
        print(f"Precio: {ask[0]}, Cantidad: {ask[1]}")
else:
    print(f"Error: {response.status_code}")
    
#-------------------------------------------------------------    
    
url = "https://api.binance.com/api/v3/klines"
params = {
    "symbol": "BTCUSDT",  # Par de trading: BTC/USDT
    "interval": "1h",     # Intervalo de tiempo: 1 hora
    "limit": 5            # Número de velas a mostrar
}
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    for candle in data:
        print(f"Fecha: {candle[0]}, Precio de apertura: {candle[1]}, Precio de cierre: {candle[4]}")
else:
    print(f"Error: {response.status_code}")