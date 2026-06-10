"""INE API module — market sizing by CNAE code per province.
NOTA: API estadistica (agregados), NO da empresas individuales.
Sirve para validar tamano de mercado B2B.
"""
import requests, json
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

BASE = 'https://servicios.ine.es/wstempus/js/ES'
HEADERS = {'Accept': 'application/json'}

CNAE_LABELS = {
    '6832': 'Gestion fincas (administracion)',
    '4322': 'Instalaciones fontaneria/calefaccion',
    '4321': 'Instalaciones electricas',
    '412':  'Construccion edificios',
    '4391': 'Cubiertas y tejados',
}

def query_dirce(cnae_code, province_code=None):
    """Query DIRCE (op 43) by CNAE and optional province.
    Returns aggregated counts, not individual companies."""
    endpoint = f'{BASE}/OPERACION/43/DATOS'
    params = {'p': 1, 'g1': cnae_code}
    if province_code:
        params['g2'] = str(province_code)
    try:
        r = requests.get(endpoint, params=params, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return data
    except Exception as e:
        log.warning(f'INE query error CNAE {cnae_code}, prov {province_code}: {e}')
    return None

def market_report():
    """Return a summary of B2B market size by CNAE across target provinces.
    Pure statistics — no individual company data."""
    results = {}
    for cnae, label in CNAE_LABELS.items():
        prov_data = []
        for prov_name, prov_code in [
            ('Madrid', '28'), ('Avila', '05'), ('Burgos', '09'),
            ('Leon', '24'), ('Palencia', '34'), ('Salamanca', '37'),
            ('Segovia', '40'), ('Soria', '42'), ('Valladolid', '47'),
            ('Zamora', '49'), ('Navarra', '31'), ('La Rioja', '26'),
            ('Guadalajara', '19'), ('Toledo', '45'),
        ][:Config.AISLA_PROVINCES.count(',')+1 if Config.AISLA_PROVINCES else 14]:
            data = query_dirce(cnae, prov_code)
            if data:
                prov_data.append({'provincia': prov_name, 'datos': data})
        results[cnae] = {'label': label, 'provincias': prov_data}
    log.info(f'INE market report: {len(results)} CNAEs')
    return results

def batch_complete():
    """Return empty leads list — INE is stats only, no individual contacts.
    Market data available via market_report()."""
    log.info('INE module: estadisticas solamente. Usar market_report() para datos.')
    return []
