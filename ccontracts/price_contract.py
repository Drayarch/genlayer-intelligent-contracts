# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

class CryptoPrices(gl.Contract):
    btc_price: float
    eth_price: float
    
    def __init__(self):
        self.btc_price = 0.0
        self.eth_price = 0.0
    
    @gl.public.write
    def update_prices(self):
        def fetch():
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
            response = gl.http_fetch(url)
            data = json.loads(response)
            return data
        
        prices = gl.eq_principle_strict_eq(fetch)
        self.btc_price = prices['bitcoin']['usd']
        self.eth_price = prices['ethereum']['usd']
    
    @gl.public.view
    def get_prices(self) -> dict:
        return {
            'bitcoin': self.btc_price,
            'ethereum': self.eth_price
        }
