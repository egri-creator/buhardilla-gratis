"""Campana de email automatizada — envia propuestas a leads frios.
Busca emails via Places API o website scraping, envia con Gmail API OAuth.
"""
import re, time, os
from datetime import datetime
from urllib.parse import urlparse
from src.utils.gmail_helper import send_email
from src.config.config_template import Config
from src.utils.helpers import setup_logging, load_json, save_json

log = setup_logging(__name__)
CAMPAIGN_DB = 'data/email_campaign.json'

TEMPLATE_AGENCIA = '''
<html><body style="font-family:Arial;color:#333;">
<h2>Colaboracion programa CAE - aislamiento GRATIS</h2>
<p>Hola,</p>
<p>He visto que teneis anunciada una propiedad con buhardilla/atico en <strong>{ciudad}</strong>.</p>
<p>El <strong>programa CAE del Gobierno</strong> (Real Decreto 36/2023) permite aislar buhardillas no habitables <strong>100% gratis</strong> para el propietario. Esto significa que tus compradores obtienen:</p>
<ul>
<li>Aislamiento termico sin coste (valor ~3.000-5.000 EUR)</li>
<li>Hasta 40% de ahorro en calefaccion</li>
<li>Certificado energetico mejorado</li>
<li>Instalacion en 2-4h sin obras</li>
</ul>
<p>Esto es un argumento de venta diferencial para tus anuncios. Quieres que te envie mas informacion?</p>
<p>Un saludo,<br/>{tu_nombre}</p>
</body></html>
'''

TEMPLATE_ADMIN = '''
<html><body style="font-family:Arial;color:#333;">
<h2>Programa CAE - aislamiento GRATIS para tus comunidades</h2>
<p>Hola,</p>
<p>Gestionas comunidades con <strong>buhardillas no habitables?</strong></p>
<p>El programa CAE del Gobierno financia el aislamiento de buhardillas perdidas <strong>al 100%</strong> sin coste para los vecinos ni para la comunidad.</p>
<p><strong>Beneficios para tus comunidades:</strong></p>
<ul>
<li>Cero coste para los propietarios</li>
<li>Instalacion en 2-4h sin obras</li>
<li>Hasta 40% de ahorro energetico</li>
<li>Sin papeleo para la comunidad (lo gestionamos todo)</li>
</ul>
<p>Ademas, ofrezco <strong>{comision}EUR por comunidad</strong> que se acoja.</p>
<p>Te interesa conocer los detalles?</p>
<p>Un saludo,<br/>{tu_nombre}</p>
</body></html>
'''

TEMPLATE_CONFIRMACION = '''
<html><body style="font-family:Arial;color:#333;">
<h2>Gracias por tu solicitud, {nombre}</h2>
<p>Hemos recibido tu solicitud de informacion sobre el <strong>aislamiento gratuito de buhardilla</strong> en <strong>{ciudad}</strong>.</p>
<p>Un asesor de Buhardilla Gratis se pondra en contacto contigo en las proximas <strong>24h</strong> para verificar tu elegibilidad.</p>
<p>Mientras tanto, puedes consultar:</p>
<ul>
<li>Real Decreto 36/2023: <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2023-2535">BOE</a></li>
<li>Programa CAE (MITECO): <a href="https://www.miteco.gob.es/es/ministerio/planes-estrategicos/eficiencia-energetica/cae.html">Informacion oficial</a></li>
</ul>
<p>Un saludo,<br/>{tu_nombre}</p>
</body></html>
'''

def load_campaign_db():
    if os.path.exists(CAMPAIGN_DB):
        return load_json(CAMPAIGN_DB)
    return {'sent': [], 'responded': [], 'pending': []}

def save_campaign_db(db):
    save_json(CAMPAIGN_DB, db)

def find_email_for_agency(agency_name, city):
    """Find email for a real estate agency via Places API or website."""
    # Try Places API: search for the agency
    if Config.GOOGLE_API_KEY and not Config.GOOGLE_API_KEY.startswith('cambia'):
        try:
            import requests
            query = f'{agency_name} {city} agencia inmobiliaria'
            url = f'https://places.googleapis.com/v1/places:searchText'
            headers = {
                'X-Goog-Api-Key': Config.GOOGLE_API_KEY,
                'Content-Type': 'application/json',
                'X-Goog-FieldMask': 'places.displayName,places.websiteUri,places.formattedAddress,places.nationalPhoneNumber',
            }
            r = requests.post(url, json={'textQuery': query, 'languageCode': 'es', 'maxResultCount': 3}, headers=headers, timeout=10)
            if r.status_code == 200:
                places = r.json().get('places', [])
                for p in places:
                    website = p.get('websiteUri', '')
                    if website:
                        email = scrape_email_from_website(website)
                        if email:
                            return email, website
                    phone = p.get('nationalPhoneNumber', '')
                    if website:
                        return None, phone
                return None, None
        except:
            pass
    return None, None

def scrape_email_from_website(url):
    """Scrape a website to find email address."""
    try:
        import requests
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', r.text))
        # Filter out generic/no-reply emails
        valid = [e for e in emails if not any(x in e.lower() for x in ['noreply', 'no-reply', 'example', 'domain.com'])]
        return valid[0] if valid else None
    except:
        return None

def send_campaign_email(lead, lead_type):
    """Send appropriate campaign email based on lead type."""
    db = load_campaign_db()
    lead_id = lead.get('id', '')
    # Skip if already sent
    if lead_id in [s['id'] for s in db['sent']]:
        return False
    
    tu_nombre = 'David'
    
    if lead_type == 'portal':
        # For portal leads (Nuroa), we need to find the agency email
        source = lead.get('fuente', '')
        city = lead.get('ciudad', '')
        # Try to find email for agency in this city
        email, contact = find_email_for_agency(source.title(), city)
        if not email:
            db['pending'].append({'id': lead_id, 'type': 'portal', 'city': city, 'source': source, 'reason': 'no_email_found'})
            save_campaign_db(db)
            return False
        
        body = TEMPLATE_AGENCIA.format(ciudad=city, tu_nombre=tu_nombre)
        ok = send_email(email, f'Colaboracion CAE - aislamiento GRATIS para compradores en {city}', body)
    
    elif lead_type == 'b2b':
        email = lead.get('email', '')
        if not email:
            # Try scraping from website
            website = lead.get('website', '')
            if website:
                email = scrape_email_from_website(website)
        if not email:
            db['pending'].append({'id': lead_id, 'type': 'b2b', 'reason': 'no_email'})
            save_campaign_db(db)
            return False
        
        city = lead.get('ciudad', lead.get('provincia', ''))
        body = TEMPLATE_ADMIN.format(ciudad=city, comision=Config.COMISION_ADMIN_FINCAS_EUR, tu_nombre=tu_nombre)
        ok = send_email(email, f'Programa CAE - aislamiento GRATIS para comunidades en {city}', body)
    
    elif lead_type == 'seo':
        email = lead.get('email', '')
        if not email:
            return False
        nombre = lead.get('nombre', lead.get('titulo', ''))
        ciudad = lead.get('ciudad', 'tu zona')
        body = TEMPLATE_CONFIRMACION.format(nombre=nombre, ciudad=ciudad, tu_nombre=tu_nombre)
        ok = send_email(email, f'Gracias por tu interes - aislamiento buhardilla gratis', body)
    
    else:
        return False
    
    if ok:
        db['sent'].append({'id': lead_id, 'type': lead_type, 'to': email, 'date': datetime.now().isoformat()})
        save_campaign_db(db)
        return True
    return False

def batch_campaign(all_leads):
    """Run campaign for all unsent leads."""
    count = 0
    for lead in all_leads:
        source = lead.get('fuente', '')
        if 'nuroa' in source or 'idealista' in source or 'fotocasa' in source:
            lt = 'portal'
        elif 'company' in source or 'admin' in source:
            lt = 'b2b'
        elif lead.get('email', ''):
            lt = 'seo'
        else:
            lt = 'portal'
        
        if send_campaign_email(lead, lt):
            count += 1
        time.sleep(1)  # Rate limit
    
    log.info(f'Campana: {count} nuevos emails enviados')
    return count
