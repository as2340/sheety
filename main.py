import os
import json
import requests
import datetime as dt

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}

body = {
    "query": input("What exercises did you do? ")
}

response = requests.post(url=EXERCISE_ENDPOINT, headers=headers, json=body)
data = response.text  # JSON string to use eg in jsonviewer.stack.hu
data_dict = json.loads(data)  # equivalent to response.json()

print(response.status_code)
print(type(data_dict))
print(data_dict["exercises"][0]["name"])
print(data_dict["exercises"][0]["nf_calories"])

print(type(json.dumps(data_dict)))

# add a row to Sheety using a POST request
# Sheety Docs: https://sheety.co/docs/requests.html

SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]
TOKEN = os.environ["TOKEN"]

# https://stackoverflow.com/questions/29931671/making-an-api-call-in-python-with-an-api-that-requires-a-bearer-token
sheety_headers = {
    "Authorization": "Bearer " + TOKEN,
}

now = dt.datetime.now()

for exercise in data_dict["exercises"]:

    # HINT - outer key needs to match the name of the sheet in the spreadsheet. workouts => workout
    # HINT - Sheety camelCases the keys of sheet column headings
    workout_data = {
        "workout": {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M"),
            "exercise": exercise["name"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    response = requests.post(
        url=SHEET_ENDPOINT, json=workout_data, headers=sheety_headers)
    response.raise_for_status()
    print(response.status_code)
    print(response.text)
