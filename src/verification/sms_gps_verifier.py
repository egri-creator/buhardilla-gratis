"""Verificacion de visitas via SMS (Twilio) + GPS"""
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

# ============================================================
# VERIFICACION SMS (Twilio)
# ============================================================

def send_verification_sms(telefono_cliente, lead_id, empresa_nombre):
    """Envia SMS al cliente preguntando si recibio visita."""
    try:
        from twilio.rest import Client
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=f'? Hola, {empresa_nombre} nos indica que le hicieron una visita tecnica '
                 f'hoy. ? Responda SI si es correcto o NO si no recibio ninguna visita. '
                 f'Ref: {lead_id}',
            from_=Config.TWILIO_PHONE_NUMBER,
            to=telefono_cliente,
        )
        log.info(f'SMS enviado a {telefono_cliente}: {msg.sid}')
        return msg.sid
    except ImportError:
        log.warning('twilio no instalado. pip install twilio')
        return None
    except Exception as e:
        log.error(f'Error SMS: {e}')
        return None

def process_sms_reply(incoming_msg):
    """Procesa respuesta SMS del cliente."""
    respuesta = incoming_msg.strip().upper()
    if respuesta == 'SI':
        return 'verificado'
    elif respuesta == 'NO':
        return 'rechazado'
    return 'pendiente'

# ============================================================
# VERIFICACION GPS (desde foto del tecnico)
# ============================================================

def verify_gps_photo(lat_tecnico, lon_tecnico, lat_lead, lon_lead, max_dist_km=0.5):
    """Verifica que el tecnico estaba en la direccion del lead."""
    from math import radians, cos, sin, asin, sqrt
    try:
        lat1, lon1 = radians(float(lat_tecnico)), radians(float(lon_tecnico))
        lat2, lon2 = radians(float(lat_lead)), radians(float(lon_lead))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        dist = c * r
        ok = dist <= max_dist_km
        log.info(f'GPS verify: {dist:.2f}km de la direccion -> {"OK" if ok else "FUERA"}')
        return ok, dist
    except Exception as e:
        log.error(f'Error GPS verify: {e}')
        return False, 999

def create_verification_link(lead_id, empresa_id):
    """Genera link para que el tecnico suba foto con GPS."""
    import hashlib
    token = hashlib.sha256(f'{lead_id}:{empresa_id}:{Config.TELEGRAM_TOKEN}'.encode()).hexdigest()[:16]
    return f'https://verificacion.leads.com/visita/{lead_id}?token={token}'
