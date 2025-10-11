import requests
import smtplib
from email.message import EmailMessage

BASE_URL = "https://api.open-meteo.com/v1/forecast?latitude=48.8411&longitude=19.6331&daily=snowfall_sum,precipitation_sum,temperature_2m_max,temperature_2m_min&timezone=Europe%2FBerlin&past_days=1&forecast_days=1&wind_speed_unit=ms"
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
RECEIVER_ADDRESS = ''


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

    def get_weather(self) -> dict:
        """Fetch weather data from the API"""
        try:
            response = requests.get(self.url)
            data = response.json()
            self.get_data()
            return data
        except Exception as e:
            print(f"Error fetching weather data: {e}")

    def get_data(self) -> None:
        """Extract relevant data from the API response"""
        self.snowfall = self.data['daily']['snowfall_sum'][0]
        self.precipitation = self.data['daily']['precipitation_sum'][0]
        self.precipitation_forecast = self.data['daily']['precipitation_sum'][1]
        self.snowfall_forecast = self.data['daily']['snowfall_sum'][1]
        self.min_tmp = self.data['daily']['temperature_2m_min'][1]
        self.max_tmp = self.data['daily']['temperature_2m_max'][1]

    def check_for_snow(self) -> bool:
        """Check for snowfall"""
        if self.snowfall > 0:
            return True
        else:
            return False

    def create_message(self) -> EmailMessage|None:
        """Create an email message if there is snowfall else None"""
        if self.check_for_snow():
            msg = EmailMessage()
            msg['Subject'] = 'Snow Alert!'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = RECEIVER_ADDRESS
            msg.set_content(f"There is {self.snowfall}cm of new snow and total precipitation of {self.precipitation}mm today!\n"
                            f"Tomorrow's forecast:\n"
                            f"Snowfall: {self.snowfall_forecast}cm\n"
                            f"Precipitation: {self.precipitation_forecast}mm\n"
                            f"Temperature between {self.min_tmp} and {self.max_tmp}C.")
            return msg
        else:
            return None

class SendEmail:
    def __init__(self, email_address=EMAIL_ADDRESS, email_password=EMAIL_PASSWORD):
        self.email_address = email_address
        self.email_password = email_password

    def send_email(self, msg: EmailMessage):
        """Send an email using SMTP"""
        with smtplib.SMTP('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, RECEIVER_ADDRESS, str(msg))



if __name__ == "__main__":
    weather = GetWeather()
    email = SendEmail()
    message = weather.create_message()
    email.send_email(message)