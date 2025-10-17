import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/forms.body"]
TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'

def authenticate():
    """Authenticates the user and returns the Google Forms service."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    return build('forms', 'v1', credentials=creds)

def create_form(service, title):
    """Creates a new Google Form."""
    form_info = {"info": {"title": title}}
    result = service.forms().create(body=form_info).execute()
    return result

def batch_update_form(service, form_id, requests):
    """Applies a batch of updates to a Google Form."""
    if requests:
        body = {"requests": requests}
        service.forms().batchUpdate(formId=form_id, body=body).execute()
