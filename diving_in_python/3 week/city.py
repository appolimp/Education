from pprint import pprint
import requests
from datetime import datetime


class OpenWeatherMapForecast:

    def __init__(self):
        self._city_cache = {}

    def get(self, city):
        if city in self._city_cache:
            return self._city_cache[city]

        api_url = 'https://api.openweathermap.org/data/2.5/forecast'
        params = {
            'q': city,  # 'Saint Petersburg'
            'appid': '6ef9ce215b4fa36d5e332cc4155a7138',
            'units': 'metric',
        }
        print('sending HTTPS request')
        forecast_data = requests.get(api_url, params=params).json()['list']
        forecast = []
        for day_data in forecast_data:
            dt = datetime.fromtimestamp(day_data['dt'])
            if dt.hour == 12:
                forecast.append({
                    'date': dt,
                    'high_temp': day_data['main']['temp_max']
                })
        self._city_cache[city] = forecast
        return forecast


class CityInfo:

    def __init__(self, city, weather_forecast=None):
        self.city = city
        self._weather_forecast = weather_forecast or OpenWeatherMapForecast()

    def weather_forecast(self):
        return self._weather_forecast.get(self.city)


def _main():
    weather_forecast = OpenWeatherMapForecast()
    for i in range(1):
        city = 'Saint Petersburg'
        city_info = CityInfo(city, weather_forecast=weather_forecast)
        pprint([city, city_info.weather_forecast()])


if __name__ == '__main__':
    _main()
