"""Helper Gmail API — leer y enviar emails con OAuth (sin 2FA ni App Password)"""
import os, base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
]

def get_gmail_service():
    creds = None
    token_path = Config.GMAIL_CREDS_FILE
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/gmail_client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_profile_email():
    """Get the authenticated user's email from Gmail profile."""
    try:
        service = get_gmail_service()
        profile = service.users().getProfile(userId='me').execute()
        return profile.get('emailAddress', '')
    except:
        return ''

def send_email(to, subject, body_html):
    try:
        service = get_gmail_service()
        msg = MIMEText(body_html, 'html')
        msg['To'] = to
        msg['Subject'] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        service.users().messages().send(userId='me', body={'raw': raw}).execute()
        log.info(f'Email enviado a {to}: {subject[:60]}')
        return True
    except Exception as e:
        log.error(f'Error enviando email Gmail API: {e}')
        return False

def search_messages(query, max_results=20):
    """Search Gmail messages with a query string. Returns list of message IDs."""
    try:
        service = get_gmail_service()
        result = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        return result.get('messages', [])
    except Exception as e:
        log.error(f'Error buscando emails: {e}')
        return []

def get_message_thread(message_id):
    """Get full thread for a message ID. Returns dict with messages."""
    try:
        service = get_gmail_service()
        msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        thread_id = msg['threadId']
        thread = service.users().threads().get(userId='me', id=thread_id).execute()
        return thread
    except Exception as e:
        log.error(f'Error obteniendo thread: {e}')
        return None
