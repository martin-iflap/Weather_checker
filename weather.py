import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast?latitude=48.8411&longitude=19.6331&daily=snowfall_sum,precipitation_sum,temperature_2m_max,temperature_2m_min&timezone=Europe%2FBerlin&past_days=1&forecast_days=1&wind_speed_unit=ms"


class GetWeather:
    def __init__(self, url=BASE_URL):
        self.url = BASE_URL
        self.data = self.get_weather()
        self.snowfall = None
        self.precipitation = None
        self.precipitation_forecast = None
        self.snowfall_forecast = None
        self.min_tmp = None
        self.max_tmp = None

    def get_weather(self):
        response = requests.get(self.url)
        data = response.json()
        return data

    def get_data(self):
        self.snowfall = self.data['daily']['snowfall_sum'][0]
        self.precipitation = self.data['daily']['precipitation_sum'][0]
        self.precipitation_forecast = self.data['daily']['precipitation_sum'][1]
        self.snowfall_forecast = self.data['daily']['snowfall_sum'][1]
        self.min_tmp = self.data['daily']['temperature_2m_min'][1]
        self.max_tmp = self.data['daily']['temperature_2m_max'][1]

    def check_for_snow(self):
        if self.snowfall > 0:
            return True
        else:
            return False

    def respond(self):
        if self.check_for_snow():
            message = f"Today we had {self.snowfall}cm of snow and {self.precipitation}mm of rain.\n"
        else:
            print("No snow today")

if __name__ == "__main__":
    weather = GetWeather()