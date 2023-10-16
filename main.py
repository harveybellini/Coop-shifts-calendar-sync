from __future__ import print_function
import requests

# Define the API
url = "API_GOES_HERE"

# Define the headers
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Authorization': 'TOKEN GOES HERE',
    'Content-Type': 'application/json',
    'Dnt': '1',
    'Origin': 'SITE',
    'Referer': 'SITE',
    'Sec-Ch-Ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

# Send the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    #print(response.text)
    data = response.text
else:
    print(f"Request failed with status code: {response.status_code}")
    quit()




import datetime
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        # Assuming your API response is stored in a variable called 'api_response'
        api_data = json.loads(data)

        # Define the calendar ID (usually your primary calendar)
        calendar_id = 'primary'

        # Extract the schedule data
        schedule = api_data.get('schedule', {})
        weeks = schedule.get('weeks', [])

        for week in weeks:
            days = week.get('days', [])
            for day in days:
                items = day.get('items', [])
                for item in items:
                    start_time = item.get('scheduled_start_time')
                    end_time = item.get('scheduled_end_time')
                    summary = 'Shift'  # You can customize the event title
                    description = 'Your work shift'  # You can add a description

                    # Create an event object
                    event = {
                        'summary': 'WORK',  # Change the title to "WORK"
                        'description': description,
                        'start': {
                            'dateTime': start_time,
                        },
                        'end': {
                            'dateTime': end_time,
                        },
                        'colorId': '11'  # Set the color to "peacock" (colorId 11)
                    }


                    # Check if the event already exists
                    events_result = service.events().list(calendarId=calendar_id, timeMin=start_time, timeMax=end_time).execute()
                    existing_events = events_result.get('items', [])

                    if not existing_events:
                        # No existing events found, insert the event
                        event = service.events().insert(calendarId=calendar_id, body=event).execute()
                        print(f'Event created: {event.get("htmlLink")}')
                    else:
                        # Event already exists, skip adding
                        print('Event already exists. Skipping.')


    except HttpError as error:
        print('An error occurred: %s' % error)


main()
print('Events added to your Google Calendar.')
