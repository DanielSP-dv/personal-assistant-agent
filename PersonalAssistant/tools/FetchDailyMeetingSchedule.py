from agency_swarm.tools import BaseTool
from pydantic import Field
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/gmail.readonly']

class FetchDailyMeetingSchedule(BaseTool):
    """
    A tool for fetching meeting schedule from Google Calendar using OAuth authentication.
    """
    start_date: str = Field(
        default=datetime.now().strftime('%Y-%m-%d'),
        description="Start date to fetch meetings from in YYYY-MM-DD format"
    )
    days: int = Field(
        default=7,
        description="Number of days to fetch meetings for"
    )

    def _get_calendar_service(self):
        """
        Authenticates and returns Calendar service object.
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def run(self):
        """
        Fetches meetings for the specified date range from Google Calendar.
        """
        try:
            service = self._get_calendar_service()
            
            # Convert start date string to datetime
            start_date_obj = datetime.strptime(self.start_date, '%Y-%m-%d')
            end_date_obj = start_date_obj + timedelta(days=self.days)
            
            # Get the start and end times
            time_min = start_date_obj.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
            time_max = end_date_obj.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

            events_result = service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=50,  # Increased to show more events
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            if not events:
                return f"No meetings scheduled between {self.start_date} and {end_date_obj.strftime('%Y-%m-%d')}"

            schedule = []
            current_date = None
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                
                # Add date header if it's a new date
                if current_date != start_time.date():
                    current_date = start_time.date()
                    schedule.append(f"\n📅 {current_date.strftime('%A, %B %d, %Y')}:")
                
                end = event['end'].get('dateTime', event['end'].get('date'))
                end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
                
                schedule.append(
                    f"📍 Meeting: {event['summary']}\n"
                    f"⏰ Time: {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}\n"
                    f"{'📌 Location: ' + event.get('location', 'No location specified') if event.get('location') else ''}\n"
                )

            return "\n".join(schedule)

        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    # Get today's date
    today = datetime.now()
    # Calculate the start of the week (Monday)
    monday = today - timedelta(days=today.weekday())
    tool = FetchDailyMeetingSchedule(start_date=monday.strftime('%Y-%m-%d'), days=7)
    print(tool.run()) 