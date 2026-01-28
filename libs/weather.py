"""
Weather Library for GenLayer Intelligent Contracts

This library provides reusable functions for fetching weather data
from OpenWeatherMap API. Can be imported by multiple contracts.

Usage:
    from libs.weather import fetch_weather_data, parse_weather_response
"""

import json
from typing import Dict, Any


def fetch_weather_data(city: str, api_key: str, gl_http_fetch) -> Dict[str, Any]:
    """
    Fetch weather data for a given city from OpenWeatherMap API.
    
    Args:
        city (str): Name of the city
        api_key (str): OpenWeatherMap API key
        gl_http_fetch: GenLayer's http_fetch function
        
    Returns:
        dict: Raw weather data from API
        
    Example:
        data = fetch_weather_data("London", "your_api_key", gl.http_fetch)
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = gl_http_fetch(url)
    return json.loads(response)


def parse_weather_response(data: Dict[str, Any], city: str) -> Dict[str, Any]:
    """
    Parse raw weather API response into clean format.
    
    Args:
        data (dict): Raw API response
        city (str): City name
        
    Returns:
        dict: Cleaned weather data with temp, condition, humidity
        
    Example:
        clean_data = parse_weather_response(raw_data, "London")
    """
    temp = float(data['main']['temp'])
    condition = data['weather'][0]['main']
    humidity = int(data['main']['humidity'])
    
    return {
        'city': city,
        'temp': temp,
        'condition': condition,
        'humidity': humidity
    }


def get_weather_complete(city: str, api_key: str, gl_http_fetch) -> Dict[str, Any]:
    """
    Complete function - fetch and parse weather in one call.
    
    Args:
        city (str): City name
        api_key (str): API key
        gl_http_fetch: GenLayer's http_fetch function
        
    Returns:
        dict: Clean weather data ready to use
        
    Example:
        weather = get_weather_complete("Paris", api_key, gl.http_fetch)
        print(f"Temperature: {weather['temp']}°C")
    """
    raw_data = fetch_weather_data(city, api_key, gl_http_fetch)
    return parse_weather_response(raw_data, city)


def format_weather_message(weather_data: Dict[str, Any]) -> str:
    """
    Format weather data into a readable message.
    
    Args:
        weather_data (dict): Cleaned weather data
        
    Returns:
        str: Formatted message
        
    Example:
        message = format_weather_message(weather)
        # Output: "Paris: 18.5°C, Sunny, Humidity: 65%"
    """
    return (
        f"{weather_data['city']}: {weather_data['temp']}°C, "
        f"{weather_data['condition']}, Humidity: {weather_data['humidity']}%"
    )


# Common weather condition mappings
WEATHER_CONDITIONS = {
    'Clear': ' Sunny',
    'Clouds': ' Cloudy',
    'Rain': ' Rainy',
    'Snow': 'Snowy',
    'Thunderstorm': ' Stormy',
    'Drizzle': 'Drizzle',
    'Mist': ' Misty',
    'Fog': ' Foggy'
}


def get_weather_emoji(condition: str) -> str:
    """
    Get emoji representation of weather condition.
    
    Args:
        condition (str): Weather condition (e.g., 'Rain', 'Clear')
        
    Returns:
        str: Emoji representation
        
    Example:
        emoji = get_weather_emoji("Rain")  # Returns "Rainy"
    """
    return WEATHER_CONDITIONS.get(condition, f"{condition}")
