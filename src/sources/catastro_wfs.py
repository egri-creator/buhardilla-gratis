"""Catastro via INSPIRE WFS — recoge muestra sin filtro y filtra por provincia.
No es exhaustivo, pero cada ejecucion da ~80 parcelas de toda España.
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, generate_lead_id

log = setup_logging(__name__)

WFS_URL = 'https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx'
OVC_URL = 'https://www1.sedecatastro.gob.es/OVCFrames.aspx'

PROV_CODES = {
    '28': 'Madrid', '05': 'Ávila', '09': 'Burgos', '24': 'León',
    '34': 'Palencia', '37': 'Salamanca', '40': 'Segovia', '42': 'Soria',
    '47': 'Valladolid', '49': 'Zamora', '31': 'Navarra', '26': 'La Rioja',
    '19': 'Guadalajara', '45': 'Toledo',
}

NS_WFS = 'http://www.opengis.net/wfs/2.0'
NS_CP = 'http://inspire.ec.europa.eu/schemas/cp/4.0'

def _extract_province(ref):
    digits = ''.join(filter(str.isdigit, ref))
    return digits[:2] if len(digits) >= 2 else ''

def batch_complete():
    seen = set()
    total = []
    params = {
        'SERVICE': 'WFS', 'VERSION': '2.0.0', 'REQUEST': 'GetFeature',
        'TYPENAMES': 'cp:CadastralParcel', 'COUNT': '500',
    }
    try:
        r = requests.get(WFS_URL, params=params, timeout=90)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        for member in root.iter(f'{{{NS_WFS}}}member'):
            parcel = member.find(f'{{{NS_CP}}}CadastralParcel')
            if parcel is None:
                parcel = member.find(f'{{{NS_CP}/}}CadastralParcel')
            if parcel is None:
                continue
            ref_el = parcel.find(f'{{{NS_CP}}}nationalCadastralReference')
            if ref_el is None or not ref_el.text:
                continue
            ref = ref_el.text.strip()
            if ref in seen:
                continue
            seen.add(ref)
            prov_code = _extract_province(ref)
            provincia = PROV_CODES.get(prov_code, '')
            if not provincia:
                continue
            area_el = parcel.find(f'{{{NS_CP}}}areaValue')
            area = float(area_el.text) if area_el is not None and area_el.text else 0
            lead = {
                'id': generate_lead_id(provincia, 'CAT'),
                'ref_catastral': ref,
                'superficie_parcela': area,
                'ciudad': provincia,
                'provincia': provincia,
                'fuente': 'catastro_wfs',
                'score': 0,
                'fecha': datetime.now().isoformat(),
                'url': f'{OVC_URL}?RC={ref}',
            }
            total.append(lead)
        log.info(f'Catastro WFS: {len(total)} parcelas en provincias objetivo')
    except Exception as e:
        log.warning(f'Catastro WFS: {e}')
    return total
