"""Deduplicacion de leads — evita duplicados por direccion, telefono o ref catastral"""
import re
from datetime import datetime
from src.utils.helpers import setup_logging, load_json, save_json

log = setup_logging(__name__)

DEDUP_CACHE = 'data/dedup_cache.json'

def normalize_address(addr):
    """Normaliza una direccion para comparacion."""
    if not addr:
        return ''
    addr = addr.lower().strip()
    addr = re.sub(r'[^\w\s]', '', addr)
    addr = re.sub(r'\bs/n\b', 'sin numero', addr)
    addr = re.sub(r'\b(calle|cl|avda|avenida|plaza|pza|travesia|trva|camino|cno)\b', '', addr)
    addr = re.sub(r'\s+', ' ', addr).strip()
    return addr

def is_duplicate(lead, cache=None):
    """Comprueba si un lead ya existe en el cache de dedup."""
    if cache is None:
        cache = load_cache()
    ref = lead.get('ref_catastral', '').strip().upper()
    if ref and ref in cache.get('refs', set()):
        return True
    addr = normalize_address(lead.get('direccion', ''))
    if addr and addr in cache.get('addresses', set()):
        return True
    telefono = re.sub(r'\D', '', lead.get('telefono', ''))
    if telefono and len(telefono) >= 9 and telefono in cache.get('phones', set()):
        return True
    url = lead.get('url', '').strip().lower()
    if url and url in cache.get('urls', set()):
        return True
    return False

def load_cache():
    """Carga cache de dedup."""
    import os
    if os.path.exists(DEDUP_CACHE):
        c = load_json(DEDUP_CACHE)
        c['refs'] = set(c.get('refs', []))
        c['addresses'] = set(c.get('addresses', []))
        c['phones'] = set(c.get('phones', []))
        c['urls'] = set(c.get('urls', []))
        return c
    return {'refs': set(), 'addresses': set(), 'phones': set(), 'urls': set(), 'count': 0}

def save_cache(cache):
    """Guarda cache de dedup."""
    serializable = {
        'refs': list(cache['refs']),
        'addresses': list(cache['addresses']),
        'phones': list(cache['phones']),
        'urls': list(cache['urls']),
        'count': cache['count'],
        'updated': datetime.now().isoformat(),
    }
    save_json(DEDUP_CACHE, serializable)

def add_to_cache(lead, cache):
    """Anade un lead al cache de dedup."""
    ref = lead.get('ref_catastral', '').strip().upper()
    if ref:
        cache['refs'].add(ref)
    addr = normalize_address(lead.get('direccion', ''))
    if addr:
        cache['addresses'].add(addr)
    telefono = re.sub(r'\D', '', lead.get('telefono', ''))
    if telefono and len(telefono) >= 9:
        cache['phones'].add(telefono)
    url = lead.get('url', '').strip().lower()
    if url:
        cache['urls'].add(url)
    cache['count'] = cache.get('count', 0) + 1

def filter_duplicates(leads):
    """Filtra leads duplicados de una lista."""
    cache = load_cache()
    unique = []
    dupes = 0
    for lead in leads:
        if is_duplicate(lead, cache):
            dupes += 1
            continue
        add_to_cache(lead, cache)
        unique.append(lead)
    save_cache(cache)
    log.info(f'Dedup: {len(unique)} unicos, {dupes} duplicados de {len(leads)} total')
    return unique
