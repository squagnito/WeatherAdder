
import requests
import urllib3
import datetime
import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Strava API
# --------------------------

auth_url = "https://www.strava.com/oauth/token"
response = requests.post(auth_url, data=config.payload, verify=False)
access_token = response.json()['access_token']

activities_url = "https://www.strava.com/api/v3/athlete/activities"
header = {'Authorization': "Bearer " + access_token}
param = {'per_page': 1, 'page': 1}
dataset = requests.get(activities_url, headers=header, params=param).json()

print(dataset[0]['id'])

# Get information about latest Strava activity and store in variable 'latest_activity'
# --------------------------

activity_id = dataset[0]['id']
activity_url = f"https://www.strava.com/api/v3/activities/{activity_id}"
latest_activity = requests.get(activity_url, headers=header, params=param).json()
print(latest_activity['description'])
print(latest_activity['start_date'])
print(latest_activity)

start_date = latest_activity['start_date_local']
activity_time_length = latest_activity['elapsed_time']
start_date_formatted = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
print(start_date_formatted)

# Weather API
# --------------------------

lat = (latest_activity['start_latlng'][0])
long = (latest_activity['start_latlng'][1])

# Start of activity in UTC
time_start = int(datetime.datetime.timestamp(start_date_formatted))

start_weather_url = (f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={long}&"
                     f"dt={time_start}&appid={config.API_key}&units=imperial")

end_weather_url = (f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={long}"
                   f"&dt={time_start + activity_time_length}&appid={config.API_key}&units=imperial")

start_weather = requests.get(start_weather_url, headers=header).json()
end_weather = requests.get(end_weather_url, headers=header).json()
print(start_weather)
print(end_weather)
temp = round((start_weather['data'][0]['temp'] + end_weather['data'][0]['temp']) / 2)
print(f"Temperature = {temp} F")
feels_like = round((start_weather['data'][0]['feels_like'] + end_weather['data'][0]['feels_like']) / 2)
print(f"Feels like = {feels_like} F")
humidity = round((start_weather['data'][0]['humidity'] + end_weather['data'][0]['humidity']) / 2)
print(f"Humidity = {humidity}%")

# Change Strava info

latest_activity[temp] = temp
latest_activity[feels_like] = feels_like
latest_activity[humidity] = humidity

# Update Strava description

description = f"Temperature: {temp}°F\nFeels like: {feels_like}°F\nHumidity: {humidity}%"

print(latest_activity['description'])

update = requests.put(activity_url, data={'description': description}, headers=header, params=param).json()

