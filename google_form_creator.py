import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/forms.body", "https://www.googleapis.com/auth/drive"]
TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'

def authenticate():
    """Authenticates the user and returns Google services for Forms and Drive."""
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
            
    forms_service = build('forms', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    
    return forms_service, drive_service

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


def get_or_create_folder(service, folder_name):
    """Searches for a folder by name and creates it if not found.

    Args:
        service: The Google Drive service object.
        folder_name (str): The name of the folder to find or create.

    Returns:
        str: The ID of the found or created folder.
    """
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    files = response.get('files', [])

    if files:
        return files[0].get('id')
    else:
        folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        return folder.get('id')


def move_form_to_folder(service, file_id, folder_id):
    """Moves a file to a specific folder in Google Drive.

    Args:
        service: The Google Drive service object.
        file_id (str): The ID of the file to move.
        folder_id (str): The ID of the destination folder.
    """
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    service.files().update(
        fileId=file_id, addParents=folder_id, removeParents=previous_parents, fields='id, parents'
    ).execute()
