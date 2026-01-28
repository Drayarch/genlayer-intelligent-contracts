"""
API Key Management Service for GenLayer Intelligent Contracts

This service demonstrates how to keep API keys private and secure,
separate from contract code on the blockchain.

For Testnet: Your contracts work fine with hardcoded keys.
For Production: Use this pattern to keep keys private.
"""

# API Keys Storage (In production, use environment variables or encrypted database)
API_KEYS = {
    "weather": {
        "key": "bbe7e79a414f003442cd9662246f7be7",
        "service": "OpenWeatherMap",
        "description": "Get weather data for any city"
    },
    "price": {
        "key": "your-coingecko-api-key-here",
        "service": "CoinGecko",
        "description": "Get cryptocurrency prices"
    },
    "social": {
        "key": "your-twitter-api-key-here",
        "service": "Twitter/Web Scraping",
        "description": "Scrape and analyze web content"
    }
}


def get_api_key(service_name: str) -> str:
    """
    Get API key for a specific service.
    
    Args:
        service_name (str): Name of service (weather, price, social)
        
    Returns:
        str: API key for the service
        
    Example:
        weather_key = get_api_key("weather")
    """
    if service_name in API_KEYS:
        return API_KEYS[service_name]["key"]
    else:
        raise ValueError(f"Service '{service_name}' not found")


def list_services() -> list:
    """
    List all available services.
    
    Returns:
        list: List of available service names
        
    Example:
        services = list_services()
        # Returns: ['weather', 'price', 'social']
    """
    return list(API_KEYS.keys())


def get_service_info(service_name: str) -> dict:
    """
    Get detailed information about a service.
    
    Args:
        service_name (str): Name of service
        
    Returns:
        dict: Service information (without exposing the actual key)
        
    Example:
        info = get_service_info("weather")
    """
    if service_name in API_KEYS:
        service = API_KEYS[service_name]
        return {
            "name": service_name,
            "service": service["service"],
            "description": service["description"],
            "key_length": len(service["key"])
        }
    else:
        return {"error": f"Service '{service_name}' not found"}


# Usage Example:
if __name__ == "__main__":
    print("API Key Management Service")
    print("=" * 50)
    
    # List all services
    print("\nAvailable Services:")
    for service in list_services():
        info = get_service_info(service)
        print(f"  - {service}: {info['service']}")
    
    # Get a specific key
    print("\nExample: Getting weather API key")
    weather_key = get_api_key("weather")
    print(f"  Key: {weather_key[:10]}...{weather_key[-5:]}")  # Show partial key
    
    print("\n Service is working!")
