import logging
import os.path
from datetime import datetime, timedelta, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

log = logging.getLogger(__name__)

SPREADSHEET_ID = '1PC--vmwgtMrL_pxM_J24_yKE51mwGJoZVmuutqXAI_c'
RANGE_NAME = 'Sheet1!A2:H'
VALUE_INPUT_OPTIONS = 'USER_ENTERED'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def auth():
    creds = None
    if os.path.exists('auth/token.json'):
        creds = Credentials.from_authorized_user_file('auth/token.json', scopes=SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'auth/credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('auth/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def append_to_table(email: str, username: str, is_payed: bool, occasion: str, gift_type: str, relation: str,
                    person_desc: str):
    creds = auth()
    try:
        service = build('sheets', 'v4', credentials=creds)
        now = datetime.now(tz=timezone(timedelta(hours=3)))
        now = now.strftime('%H:%M - %d %B %Y')
        values = [
            [
                now,
                email,
                username,
                'Да' if is_payed else 'Нет',
                occasion,
                relation,
                gift_type,
                person_desc,
            ]
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption=VALUE_INPUT_OPTIONS, body=body
        ).execute()
        log.info(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as err:
        log.error(err)
        return err
