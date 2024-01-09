import requests

def get_weather_data(place, api_key=None):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": place, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    data = response.json()
    weather_data = {
        "name": data["name"],
        "coord": {"lon": data["coord"]["lon"], "lat": data["coord"]["lat"]},
        "country": data["sys"]["country"],
        "feels_like": data["main"]["feels_like"],
        "timezone": f"UTC{data['timezone']//3600:+d}"
    }
    return weather_data
