# { "Depends": "py-genlayer:test" }
from genlayer import *
import json

class WeatherOracle(gl.Contract):
    city: str
    temperature: float
    condition: str
    humidity: u256
    
    def __init__(self):
        self.city = "None"
        self.temperature = 0.0
        self.condition = "No data"
        self.humidity = 0
    
    @gl.public.write
    def get_weather(self, city: str) -> dict:
        def fetch_weather():
            # Your API key (keep it as is)
            API_KEY = "bbe7e79a414f003442cd9662246f7be7"
            
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            
            response = gl.http_fetch(url)
            data = json.loads(response)
            
            # Extract data - matching your API response structure
            temp = float(data['main']['temp'])
            condition = data['weather'][0]['main']
            humidity = int(data['main']['humidity'])
            
            return {
                'city': city,
                'temp': temp,
                'condition': condition,
                'humidity': humidity
            }
        
        result = gl.eq_principle_strict_eq(fetch_weather)
        
        self.city = result['city']
        self.temperature = result['temp']
        self.condition = result['condition']
        self.humidity = result['humidity']
        
        return result
    
    @gl.public.view
    def get_data(self) -> dict:
        return {
            'city': self.city,
            'temperature': self.temperature,
            'condition': self.condition,
            'humidity': self.humidity
        }
