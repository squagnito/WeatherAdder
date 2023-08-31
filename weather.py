import requests
import urllib3
import datetime
import time
import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Strava API

auth_url = ("https://www.strava.com/oauth/token")
response = requests.post(auth_url, data=config.payload, verify=False)
access_token = response.json()['access_token']

activities_url = ("https://www.strava.com/api/v3/athlete/activities")
header = {'Authorization': "Bearer " + access_token}
param = {'per_page': 1, 'page': 1}
dataset = requests.get(activities_url, headers=header, params=param).json()

print(dataset[0]['id'])

# Get information about latest Strava activity and store in variable 'latest_activity'

id = dataset[0]['id']
activity_url = (f"https://www.strava.com/api/v3/activities/{id}")
latest_activity = requests.get(activity_url, headers=header, params=param).json()
print(latest_activity['description'])
print(latest_activity['start_date'])
print(latest_activity)

start_date = latest_activity['start_date_local']
date_format = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
print(date_format)

# Weather API

lat = (latest_activity['start_latlng'][0])
long = (latest_activity['start_latlng'][1])
time = int(datetime.datetime.timestamp(date_format))
weather_url = (f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={long}&dt={time}&appid={config.API_key}&units=imperial")

weather = requests.get(weather_url, headers=header).json()
print(weather)
temp = round((weather['data'][0]['temp']))
print(f"Temperature = {temp} F")
feels_like = round((weather['data'][0]['feels_like']))
print(f"Feels like = {feels_like} F")
humidity = (weather['data'][0]['humidity'])
print(f"Humidity = {humidity}%")

# Change Strava info

latest_activity[temp] = temp
latest_activity[feels_like] = feels_like
latest_activity[humidity] = humidity

# Update Strava description

description = (f"Temperature: {temp}°F\nFeels like: {feels_like}°F\nHumidity: {humidity}%")

print(latest_activity['description'])

update = requests.put(activity_url, data={'description': description},headers= header, params= param).json()