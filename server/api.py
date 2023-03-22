import requests
import json
import datetime

air_quality_index = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor",
}

def get_location():
    data = []
    search_location = str(input("Search Location: "))
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={search_location}&limit=5&appid=44d1756e7fd91b4801d50fa88ac13b8c")
    results = response.json()

    for result in results:
        location = {"name": result.get('name', ''), "state": result.get('state', ''), "country": result.get('country', '')}
        if location not in data:
            data.append(location)

    for i, location in enumerate(data):
        print(f"{i}: {location['name']}, {location['state']}, {location['country']}")
    selection = int(input(">> "))
    latitude, longitude, name, country = results[selection].get('lat', ''), results[selection].get('lon', ''), results[selection].get('name', ''), results[selection].get('country', '')
    print(f"{latitude}, {longitude}")
    return latitude, longitude, name, country

def get_weather_data(api_url):
    latitude, longitude, name, country = get_location()
    response = requests.get(api_url.format(latitude=latitude, longitude=longitude, name=name, country=country))
    return response.json()

def print_date(forecast):
    dt = forecast['dt']
    print(datetime.datetime.fromtimestamp(dt).strftime("%d/%m/%Y %I:%M:%S %p")) 

def print_air_quality(forecast):
    aqi = forecast['main']['aqi']
    if aqi in air_quality_index:
        print(f"Date: {datetime.datetime.fromtimestamp(forecast['dt'])} Air Quality Level: {air_quality_index[aqi]}")
    else:
        print("Invalid AQI value")

def forecast_weather(): 
    response = get_weather_data("https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid=44d1756e7fd91b4801d50fa88ac13b8c&units=metric")
    for i, forecast in enumerate(response['list']):
        print_date(forecast)
    return response

def current_weather():
    response = get_weather_data("https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=44d1756e7fd91b4801d50fa88ac13b8c&units=metric")
    print(response)
    return response

def current_polution():
    response = get_weather_data("http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid=44d1756e7fd91b4801d50fa88ac13b8c")
    print_air_quality(response)
    return response

def forecast_polution():
    response = get_weather_data("https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={latitude}&lon={longitude}&appid=44d1756e7fd91b4801d50fa88ac13b8c&units=metric")
    for forecast in response['list']:
        print_air_quality(forecast)
    return response

def get_weather_alerts():
    response = get_weather_data("https://api.weatherbit.io/v2.0/alerts?lat={latitude}&lon={longitude}&key=b3e792d10fd54853b69b2c2954b0c8c0&city={name}&country={country}")
    for alert in response['alerts']:
        print(f"\n\nTitle: {alert['title']}\n\nDescription: {alert['description']}\n\nSeverity: {alert['severity']}\n\n(UTC) time that alert was issued: {alert['effective_utc']}\n\n(UTC) time that alert expires: {alert['expires_utc']}")
    return response

forecast_polution()