from agency_swarm.tools import BaseTool
from pydantic import Field
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GetUnreadEmails(BaseTool):
    """
    A tool for fetching unread emails from Gmail using OAuth authentication.
    """
    max_results: int = Field(
        default=10,
        description="Maximum number of unread emails to fetch"
    )

    def _get_gmail_service(self):
        """
        Authenticates and returns Gmail service object.
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

        return build('gmail', 'v1', credentials=creds)

    def run(self):
        """
        Fetches unread emails from Gmail.
        """
        try:
            service = self._get_gmail_service()
            results = service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=self.max_results
            ).execute()

            messages = results.get('messages', [])
            if not messages:
                return "No unread messages found."

            email_list = []
            for message in messages:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()

                headers = msg['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'] == 'Subject')
                sender = next(h['value'] for h in headers if h['name'] == 'From')
                date = next(h['value'] for h in headers if h['name'] == 'Date')

                email_list.append(f"From: {sender}\nSubject: {subject}\nDate: {date}\n")

            return "\n".join(email_list)

        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    tool = GetUnreadEmails(max_results=5)
    print(tool.run()) 