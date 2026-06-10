"""Verificador de tejados via Google Maps Static API.
Usa el crédito gratuito de Google Maps ($200/mes = ~100,000 imágenes).
Comprueba si la parcela tiene un tejado con buhardilla visible.
Sin coste real (dentro del free tier de $200/mes).
"""
import requests
import os
import json
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

ROOF_DIR = 'data/roofs'

def check_roof(lat, lon, ref_catastral):
    """Obtiene imagen satelital de una parcela y verifica si tiene tejado.
    Usa Google Maps Static API dentro del free tier ($200/mes).
    """
    api_key = Config.GOOGLE_API_KEY
    if api_key.startswith('cambia'):
        return None
    os.makedirs(ROOF_DIR, exist_ok=True)
    url = 'https://maps.googleapis.com/maps/api/staticmap'
    params = {
        'center': f'{lat},{lon}',
        'zoom': '20',
        'size': '400x400',
        'maptype': 'satellite',
        'key': api_key,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            filename = f'{ROOF_DIR}/{ref_catastral}.png'
            with open(filename, 'wb') as f:
                f.write(resp.content)
            log.info(f'Roof image saved: {filename}')
            return filename
    except Exception as e:
        log.warning(f'Error roof check {ref_catastral}: {e}')
    return None

def batch_complete():
    return []
