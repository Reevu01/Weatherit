import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY2')

def getWeather(lat, lon):
    
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "is_day"],
        "wind_speed_unit": "ms",
        "precipitation_unit": "inch",
        "timezone": "auto"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_is_day = current.Variables(1).Value()

    # print(f"Current time {current.Time()}")
    # print(f"Current temperature_2m {current_temperature_2m}")
    is_day = ""
    if current_is_day == 0:
        is_day = "Night"
    else:
        is_day = "Day"
    
    # print(f"It is {is_day}")
    
    return int(current_temperature_2m), is_day
    
def get_lat_lon(country, state, city, api_key):  
    
    address = f"{city}, {state}, {country}"
    resp = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}")
    data = resp.json()
    
    location = data['results'][0]['geometry']['location']
    lat = location['lat']
    lon = location['lng']
    return lat, lon

def main(country, state, city):
    lat, lon = get_lat_lon(country, state, city, api_key)
    temp, day = getWeather(lat, lon)
    return temp, day
    
    