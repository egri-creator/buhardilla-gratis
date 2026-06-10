"""Company Finder via Google Places API (New)"""
import requests, json
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, save_json, load_json

log = setup_logging(__name__)
COMPANIES_FILE = 'data/companies/active.json'

PLACES_URL = 'https://places.googleapis.com/v1/places:searchText'
FIELDS = 'places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.id,places.nationalPhoneNumber,places.websiteUri'

QUERIES = [
    'instalador aislamiento {ciudad}',
    'empresa rehabilitacion energetica {ciudad}',
    'eficiencia energetica {ciudad}',
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
        if '403' in str(e):
            _places_ok = False
            log.warning('Places API no disponible (403). Desactivada.')
        else:
            log.warning(f'Places API error: {e}')
        return []

def calculate_tier(place):
    rating = place.get('rating', 0)
    reviews = place.get('userRatingCount', 0)
    if rating >= 4.5 and reviews >= 50:
        return '1'
    elif rating >= 4.0 and reviews >= 10:
        return '2'
    return '3'

_TODAY_RAN = False

def find_installer_companies():
    global _TODAY_RAN
    if _TODAY_RAN:
        return []
    api_key = Config.GOOGLE_API_KEY
    if not api_key:
        log.warning('GOOGLE_API_KEY no configurada')
        return []
    all_companies = []
    seen = set()
    for ciudad, key, provincia in Config.B2B_CITIES():
        for q in QUERIES:
            query = q.format(ciudad=ciudad)
            results = search_places(query, api_key)
            for place in results:
                name = (place.get('displayName') or {}).get('text', '')
                if not name or name.lower() in seen:
                    continue
                seen.add(name.lower())
                company = {
                    'nombre': name,
                    'direccion': place.get('formattedAddress', ''),
                    'telefono': place.get('nationalPhoneNumber', ''),
                    'website': place.get('websiteUri', ''),
                    'rating': place.get('rating', 0),
                    'resenas': place.get('userRatingCount', 0),
                    'ciudad': ciudad,
                    'provincia': provincia,
                    'place_id': place.get('id', ''),
                    'fuente': 'google_maps',
                    'tier': calculate_tier(place),
                    'contactado': False,
                    'fecha': datetime.now().isoformat(),
                }
                all_companies.append(company)
    _TODAY_RAN = True
    all_companies.sort(key=lambda c: c.get('resenas', 0), reverse=True)
    log.info(f'Company Finder: {len(all_companies)} instaladores de {len(Config.B2B_CITIES())} ciudades')
    return all_companies

def batch_complete():
    companies = find_installer_companies()
    if companies:
        existing = load_companies() if __import__('os').path.exists(COMPANIES_FILE) else []
        existing_names = {c['nombre'].lower() for c in existing}
        new = [c for c in companies if c['nombre'].lower() not in existing_names]
        save_json(COMPANIES_FILE, existing + new)
        log.info(f'Company Finder: {len(new)} nuevas, {len(existing) + len(new)} total')
    return companies
