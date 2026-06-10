"""Admin Fincas via Google Places API (New)"""
import requests
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, generate_lead_id

log = setup_logging(__name__)

PLACES_URL = 'https://places.googleapis.com/v1/places:searchText'
FIELDS = 'places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.id,places.nationalPhoneNumber,places.websiteUri'

_places_ok = True

def search_administradores(ciudad, provincia):
    global _places_ok
    if not _places_ok:
        return []
    leads = []
    params = {
        'textQuery': f'administrador de fincas {ciudad}',
        'languageCode': 'es',
    }
    headers = {
        'X-Goog-Api-Key': Config.GOOGLE_API_KEY,
        'X-Goog-FieldMask': FIELDS,
        'Content-Type': 'application/json',
    }
    try:
        resp = requests.post(PLACES_URL, json=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        for place in data.get('places', []):
            name = (place.get('displayName') or {}).get('text', '')
            if not name:
                continue
            lead = {
                'id': generate_lead_id(provincia, 'ADM'),
                'nombre': name,
                'direccion': place.get('formattedAddress', ''),
                'telefono': place.get('nationalPhoneNumber', ''),
                'website': place.get('websiteUri', ''),
                'rating': place.get('rating', 0),
                'ciudad': ciudad,
                'provincia': provincia,
                'place_id': place.get('id', ''),
                'fuente': 'google_places_admin',
                'score': 0,
                'fecha': datetime.now().isoformat(),
            }
            leads.append(lead)
    except Exception as e:
        if '403' in str(e):
            _places_ok = False
            log.warning('Places API no disponible (403). Desactivada para el resto del pipeline.')
        else:
            log.warning(f'Places API {ciudad}: {e}')
    return leads

_TODAY_RAN = False

def batch_complete():
    global _TODAY_RAN
    if _TODAY_RAN:
        return []
    total = []
    for ciudad, key, provincia in Config.B2B_CITIES():
        leads = search_administradores(ciudad, provincia)
        if leads:
            log.info(f'Admins {ciudad}: {len(leads)}')
            total.extend(leads)
    _TODAY_RAN = True
    log.info(f'Total admins: {len(total)} de {len(Config.B2B_CITIES())} ciudades')
    return total
