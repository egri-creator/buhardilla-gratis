"""Fuente C: Google Alerts via Gmail API — lee alertas reales del buzón"""
import re
import time
import requests
from datetime import datetime, timedelta
from src.config.config_template import Config
from src.utils.helpers import setup_logging, generate_lead_id
from src.sources.idealista_alerts import get_gmail_service

log = setup_logging(__name__)

ALERTA_KEYWORDS = [
    'buhardilla', 'atico', 'desvan', 'tejado', 'cubierta',
    'aislamiento', 'aislar', 'rehabilitacion energetica', 'reforma',
    'calefaccion cara', 'factura luz', 'factura gas',
    'subvencion aislamiento', 'ayuda rehabilitacion',
    'programa CAE', 'certificado ahorro energetico',
    'mejora energetica', 'eficiencia energetica',
]

MUNICIPIO_NOMBRES = [m[0].lower() for m in Config.ALL_MUNICIPIOS()]

def search_alert_emails(service):
    """Busca emails de Google Alerts en Gmail de las ultimas 24h."""
    leads = []
    after_date = (datetime.now() - timedelta(hours=24)).strftime('%Y/%m/%d')
    query = f'from:google-alerts@google.com after:{after_date}'
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=50).execute()
        messages = results.get('messages', [])
        for msg in messages:
            full = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            payload = full.get('payload', {})
            headers = {h['name']: h['value'] for h in payload.get('headers', [])}
            subject = headers.get('Subject', '')
            snippet = full.get('snippet', '')
            text = f'{subject} {snippet}'
            if not any(kw in text.lower() for kw in ALERTA_KEYWORDS):
                continue
            lead = {
                'id': generate_lead_id('GEN', 'GAL'),
                'texto': text[:1000],
                'url': extract_url_from_snippet(snippet),
                'alerta': subject,
                'fuente': 'google_alert',
                'fecha': datetime.now().isoformat(),
                'score': 0,
            }
            for ciudad, key, provincia in Config.ALL_MUNICIPIOS():
                if ciudad.lower() in text.lower():
                    lead['provincia'] = provincia
                    lead['ciudad'] = ciudad
                    break
            leads.append(lead)
        log.info(f'Google Alerts Gmail: {len(leads)} alertas relevantes de {len(messages)} totales')
    except Exception as e:
        log.error(f'Error Gmail API Google Alerts: {e}')
    return leads

def extract_url_from_snippet(snippet):
    """Extrae URL del snippet del email de Google Alerts."""
    m = re.search(r'https?://[^\s]+', snippet)
    return m.group(0) if m else ''

def monitor_alerts():
    """Monitoriza Google Alerts via Gmail API."""
    try:
        service = get_gmail_service()
        if service:
            return search_alert_emails(service)
        return []
    except Exception as e:
        log.warning(f'Google Alerts requiere Gmail configurado: {e}')
        return []
