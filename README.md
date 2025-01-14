# Personal Assistant Agent

A powerful personal assistant agent built using the Agency Swarm framework. This agent can help you manage your emails, calendar, and provide time-related information.

## Features

- **Email Management**: Check unread emails from Gmail
- **Calendar Management**: View and manage calendar events
- **Time Information**: Get current time information

## Tools

1. **GetUnreadEmails**: Fetches unread emails from Gmail using OAuth authentication
2. **FetchDailyMeetingSchedule**: Retrieves calendar events using Google Calendar API
3. **GetCurrentTime**: Provides current time information

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google OAuth:
   - Create a project in Google Cloud Console
   - Enable Gmail and Calendar APIs
   - Create OAuth 2.0 credentials
   - Download and save credentials as `credentials.json` in the root directory

3. Configure OpenAI API:
   - Create a `.env` file
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

4. Run the agent:
```bash
python agency.py
```

## Project Structure

```
.
├── PersonalAssistant/
│   ├── tools/
│   │   ├── GetUnreadEmails.py
│   │   ├── FetchDailyMeetingSchedule.py
│   │   └── GetCurrentTime.py
│   ├── PersonalAssistant.py
│   └── instructions.md
├── agency.py
├── agency_manifesto.md
└── requirements.txt
```

## Authentication

The agent uses OAuth 2.0 for Google services authentication. On first run, it will:
1. Open your default web browser
2. Request permission to access Gmail and Calendar
3. Save the authentication token in `token.json`

## Security

- All API keys and tokens are stored securely
- OAuth 2.0 is used for Google services
- No sensitive data is logged or stored permanently

## License

MIT License 