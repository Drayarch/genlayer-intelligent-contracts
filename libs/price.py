"""
Price Feed Library for GenLayer Intelligent Contracts

This library provides reusable functions for fetching cryptocurrency prices
from CoinGecko API. Can be imported by multiple contracts.

Usage:
    from libs.price import fetch_crypto_prices, get_single_price
"""

import json
from typing import Dict, List, Any


def fetch_crypto_prices(coin_ids: List[str], gl_http_fetch) -> Dict[str, float]:
    """
    Fetch cryptocurrency prices from CoinGecko API.
    
    Args:
        coin_ids (list): List of coin IDs (e.g., ['bitcoin', 'ethereum'])
        gl_http_fetch: GenLayer's http_fetch function
        
    Returns:
        dict: Price data for each coin in USD
        
    Example:
        prices = fetch_crypto_prices(['bitcoin', 'ethereum'], gl.http_fetch)
        # Returns: {'bitcoin': 45000.0, 'ethereum': 2500.0}
    """
    coins = ','.join(coin_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd"
    
    response = gl_http_fetch(url)
    data = json.loads(response)
    
    # Extract prices
    prices = {}
    for coin in coin_ids:
        if coin in data:
            prices[coin] = float(data[coin]['usd'])
    
    return prices


def get_single_price(coin_id: str, gl_http_fetch) -> float:
    """
    Get price for a single cryptocurrency.
    
    Args:
        coin_id (str): Coin ID (e.g., 'bitcoin')
        gl_http_fetch: GenLayer's http_fetch function
        
    Returns:
        float: Current price in USD
        
    Example:
        btc_price = get_single_price('bitcoin', gl.http_fetch)
    """
    prices = fetch_crypto_prices([coin_id], gl_http_fetch)
    return prices.get(coin_id, 0.0)


def fetch_prices_with_details(coin_ids: List[str], gl_http_fetch) -> Dict[str, Dict]:
    """
    Fetch detailed price information including 24h change and market cap.
    
    Args:
        coin_ids (list): List of coin IDs
        gl_http_fetch: GenLayer's http_fetch function
        
    Returns:
        dict: Detailed price data for each coin
        
    Example:
        details = fetch_prices_with_details(['bitcoin'], gl.http_fetch)
    """
    coins = ','.join(coin_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
    
    response = gl_http_fetch(url)
    data = json.loads(response)
    
    result = {}
    for coin in coin_ids:
        if coin in data:
            result[coin] = {
                'price': float(data[coin]['usd']),
                'change_24h': float(data[coin].get('usd_24h_change', 0.0)),
                'market_cap': float(data[coin].get('usd_market_cap', 0.0))
            }
    
    return result


def format_price(price: float, decimals: int = 2) -> str:
    """
    Format price with proper decimals and currency symbol.
    
    Args:
        price (float): Price value
        decimals (int): Number of decimal places
        
    Returns:
        str: Formatted price string
        
    Example:
        formatted = format_price(45000.5678)  # Returns "$45,000.57"
    """
    return f"${price:,.{decimals}f}"


def calculate_portfolio_value(holdings: Dict[str, float], gl_http_fetch) -> float:
    """
    Calculate total portfolio value.
    
    Args:
        holdings (dict): Dictionary of coin_id -> amount
        gl_http_fetch: GenLayer's http_fetch function
        
    Returns:
        float: Total portfolio value in USD
        
    Example:
        holdings = {'bitcoin': 0.5, 'ethereum': 2.0}
        value = calculate_portfolio_value(holdings, gl.http_fetch)
    """
    coin_ids = list(holdings.keys())
    prices = fetch_crypto_prices(coin_ids, gl_http_fetch)
    
    total = 0.0
    for coin, amount in holdings.items():
        if coin in prices:
            total += prices[coin] * amount
    
    return total


def get_price_change_percentage(old_price: float, new_price: float) -> float:
    """
    Calculate percentage change between two prices.
    
    Args:
        old_price (float): Previous price
        new_price (float): Current price
        
    Returns:
        float: Percentage change
        
    Example:
        change = get_price_change_percentage(100, 110)  # Returns 10.0
    """
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100


def is_price_increasing(coin_id: str, gl_http_fetch) -> bool:
    """
    Check if a coin's price increased in the last 24 hours.
    
    Args:
        coin_id (str): Coin ID
        gl_http_fetch: GenLayer's http_fetch function
        
    Returns:
        bool: True if price increased, False otherwise
        
    Example:
        is_up = is_price_increasing('bitcoin', gl.http_fetch)
    """
    details = fetch_prices_with_details([coin_id], gl_http_fetch)
    if coin_id in details:
        return details[coin_id]['change_24h'] > 0
    return False


# Supported cryptocurrencies
SUPPORTED_COINS = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'cardano': 'ADA',
    'solana': 'SOL',
    'polkadot': 'DOT',
    'binancecoin': 'BNB',
    'ripple': 'XRP',
    'dogecoin': 'DOGE'
}


def get_coin_symbol(coin_id: str) -> str:
    """
    Get short symbol for a coin ID.
    
    Args:
        coin_id (str): Full coin ID (e.g., 'bitcoin')
        
    Returns:
        str: Coin symbol (e.g., 'BTC')
        
    Example:
        symbol = get_coin_symbol('bitcoin')  # Returns 'BTC'
    """
    return SUPPORTED_COINS.get(coin_id, coin_id.upper())
