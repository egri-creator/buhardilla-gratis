"""B2B Companies — busca empresas con locales/naves/oficinas con buhardilla no habitable
via Google Places API (New). Empresas propietarias de inmuebles candidatos a CAE.
"""
import requests
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, save_json

log = setup_logging(__name__)

PLACES_URL = 'https://places.googleapis.com/v1/places:searchText'
FIELDS = 'places.displayName,places.formattedAddress,places.id,places.nationalPhoneNumber,places.websiteUri,places.types'

QUERIES = [
    'naves industriales en {ciudad}',
    'locales comerciales en {ciudad}',
    'oficinas en {ciudad}',
    'poligono industrial {ciudad}',
    'talleres {ciudad}',
]

_places_ok = True

def search_places(query, api_key):
    global _places_ok
    if not _places_ok:
        return []
    headers = {
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': FIELDS,
        'Content-Type': 'application/json',
    }
    try:
        resp = requests.post(PLACES_URL, json={'textQuery': query, 'languageCode': 'es'}, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json().get('places', [])
    except Exception as e:
        if '403' in str(e) or '429' in str(e):
            _places_ok = False
            log.warning(f'Places API bloqueada ({e}). Desactivada.')
        else:
            log.warning(f'Places API error: {e}')
        return []

def batch_complete():
    api_key = Config.GOOGLE_API_KEY
    if not api_key:
        log.warning('GOOGLE_API_KEY no configurada')
        return []
    all_leads = []
    seen = set()
    chunks = list(Config.B2B_CITIES())
    for idx, (ciudad, key, provincia) in enumerate(chunks):
        for q in QUERIES:
            query = q.format(ciudad=ciudad)
            results = search_places(query, api_key)
            for place in results:
                name = (place.get('displayName') or {}).get('text', '')
                place_id = place.get('id', '')
                if not name or place_id in seen:
                    continue
                seen.add(place_id)
                lead = {
                    'id': place_id[:20],
                    'empresa': name,
                    'direccion': place.get('formattedAddress', ''),
                    'telefono': place.get('nationalPhoneNumber', ''),
                    'website': place.get('websiteUri', ''),
                    'tipos': place.get('types', []),
                    'ciudad': ciudad,
                    'provincia': provincia,
                    'fuente': 'b2b_places',
                    'score': 0,
                    'contactado': False,
                    'fecha': datetime.now().isoformat(),
                }
                all_leads.append(lead)
        # Save progressive every 5 cities
        if (idx + 1) % 5 == 0:
            save_json('data/leads/b2b_partial.json', all_leads)
        import time
        time.sleep(0.5)
    save_json('data/leads/b2b_partial.json', all_leads)
    log.info(f'B2B Companies: {len(all_leads)} leads de {len(chunks)} ciudades')
    return all_leads
