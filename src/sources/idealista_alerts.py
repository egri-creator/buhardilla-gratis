"""Fuente G: Idealista Alertas via Gmail API — sin scraping directo"""
import re
from datetime import datetime, timedelta
from src.config.config_template import Config
from src.utils.helpers import setup_logging, generate_lead_id
from src.utils.gmail_helper import get_gmail_service

log = setup_logging(__name__)

MUNICIPIO_NOMBRES = {m[0].lower(): (m[0], m[2]) for m in Config.ALL_MUNICIPIOS()}

def search_idealista_emails(service):
    """Busca emails de Idealista en Gmail de las ultimas 24h."""
    leads = []
    query = 'from:idealista.com subject:(atico OR buhardilla) newer_than:1d'
    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        for msg in messages[:20]:
            full = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = full.get('payload', {})
            parts = payload.get('parts', [])
            text = ''
            for part in parts:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data', '')
                    import base64
                    text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    break
            lead = parse_idealista_email(text)
            if lead:
                leads.append(lead)
    except Exception as e:
        log.error(f'Error Gmail API: {e}')
    return leads

def parse_idealista_email(text):
    """Parsea un email de alerta de Idealista."""
    if not text:
        return None
    lead = {
        'id': generate_lead_id('GEN', 'IDS'),
        'texto': text[:500],
        'fuente': 'idealista_alerta',
        'fecha': datetime.now().isoformat(),
        'score': 0,
    }
    m = re.search(r'(\d{2,3}\.\d{3,})\s*€', text)
    if m:
        lead['precio'] = float(m.group(1).replace('.', ''))
    else:
        lead['precio'] = 0
    for ciudad_lower, (ciudad, provincia) in MUNICIPIO_NOMBRES.items():
        if ciudad_lower in text.lower():
            lead['provincia'] = provincia
            lead['ciudad'] = ciudad
            break
    m = re.search(r'(https?://[^\s]+idealista[^\s]+)', text)
    if m:
        lead['url'] = m.group(1)
    return lead

def batch_complete():
    try:
        service = get_gmail_service()
        leads = search_idealista_emails(service)
        log.info(f'Idealista alertas: {len(leads)} anuncios')
        return leads
    except Exception as e:
        log.error(f'Error Gmail auth: {e}. Necesitas configurar credentials/')
        return []
