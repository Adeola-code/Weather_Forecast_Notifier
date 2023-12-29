import requests
from twilio.rest import Client
import os
from decouple import config
MY_LAT = 6.695070
MY_LONG = -1.615800
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"


# Load environment variables from .env
api_key = config('OWM_API_KEY')
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
exc="city"
weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "exclude": exc
}
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice=weather_data["list"][:12]
# weather_id=weather_slice[0]["weather"][0]["id"]
will_rain=False
for hour_data in weather_slice:
    condition_code=hour_data["weather"][0]["id"]
    if int(condition_code <700):
        will_rain=True

if will_rain:
    client=Client(account_sid,auth_token)
    message=client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔",
        from_="+17049372724",
        to="+2348064561720"
    )

    print(message.status)