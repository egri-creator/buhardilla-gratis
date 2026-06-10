"""Monitor de respuestas — revisa Gmail en busca de respuestas a campanas de email.
Detecta replies positivas y marca lider como caliente.
"""
import base64, os
from datetime import datetime, timedelta
from src.utils.gmail_helper import search_messages, get_message_thread, send_email as gmail_send
from src.utils.helpers import setup_logging
from src.delivery.email_campaign import load_campaign_db, save_campaign_db

log = setup_logging(__name__)

POSITIVE_KEYWORDS = [
    'interesado', 'quiero', 'si', 'info', 'informacion', 'adelante',
    'cuentame', 'dime', 'ok', 'vale', 'genial', 'perfecto',
    'contacta', 'llamame', 'escribe', 'presupuesto', 'solicito',
    'me interesa', 'quisiera', 'podemos', 'hablamos', 'acepto',
]

NEGATIVE_KEYWORDS = [
    'no interesado', 'baja', 'stop', 'unsubscribe', 'no gracias',
    'no quiero', 'no me interesa', 'spam', 'eliminar',
]

def detect_replies(since_hours=24):
    """Check for replies to our sent campaign emails in the last N hours."""
    db = load_campaign_db() if os.path.exists(CAMPAIGN_DB) else {'sent': [], 'responded': [], 'pending': []}
    
    if not db.get('sent'):
        return []
    
    since = (datetime.now() - timedelta(hours=since_hours)).strftime('%Y/%m/%d')
    new_responses = []
    
    for sent in db['sent']:
        # Skip if already responded
        if sent['id'] in [r['id'] for r in db.get('responded', [])]:
            continue
        
        # Search for replies in threads containing our sent email
        to_email = sent.get('to', '')
        if not to_email:
            continue
        
        query = f'from:{to_email} after:{since}'
        messages = search_messages(query, max_results=5)
        
        for msg in messages:
            thread = get_message_thread(msg['id'])
            if not thread:
                continue
            
            for m in thread.get('messages', []):
                payload = m.get('payload', {})
                headers = {h['name']: h['value'] for h in payload.get('headers', [])}
                from_h = headers.get('From', '')
                subject = headers.get('Subject', '')
                body = ''
                
                # Extract body
                if 'parts' in payload:
                    for part in payload['parts']:
                        if part.get('mimeType') == 'text/plain':
                            data = part.get('body', {}).get('data', '')
                            if data:
                                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                
                text = f'{subject} {body}'.lower()
                
                # Check for negative first
                if any(k in text for k in NEGATIVE_KEYWORDS):
                    db['responded'].append({'id': sent['id'], 'status': 'not_interested', 'date': datetime.now().isoformat()})
                    continue
                
                # Check for positive
                if any(k in text for k in POSITIVE_KEYWORDS):
                    response = {
                        'id': sent['id'],
                        'status': 'interested',
                        'from': from_h,
                        'subject': subject,
                        'body': body[:500],
                        'date': datetime.now().isoformat(),
                    }
                    db['responded'].append(response)
                    new_responses.append(response)
                    log.info(f'Respuesta positiva detectada: {sent["id"]} de {from_h}')
    
    save_campaign_db(db)
    
    if new_responses:
        for r in new_responses:
            html = f'''<html><body style="font-family:Arial;">
            <h2 style="color:#27ae60;">Lead caliente detectado!</h2>
            <p>Alguien ha respondido interesado a tu campana de email.</p>
            <p><strong>Lead ID:</strong> {r['id']}</p>
            <p><strong>De:</strong> {r['from']}</p>
            <p><strong>Asunto:</strong> {r['subject']}</p>
            <p><strong>Mensaje:</strong> {r['body'][:500]}</p>
            <p>Revisa tu Gmail para responder personalmente.</p>
            </body></html>'''
            try:
                gmail_send('captacionleads25@gmail.com', f'Lead caliente: respondio {r["from"]}', html)
            except:
                pass
    
    return new_responses
