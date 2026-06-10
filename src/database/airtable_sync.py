"""Sincronizacion con Airtable (base de datos principal)"""
import requests
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

BASE_URL = 'https://api.airtable.com/v0'

HEADERS = {
    'Authorization': f'Bearer {Config.AIRTABLE_TOKEN}',
    'Content-Type': 'application/json',
}

_AIRTABLE_DISABLED = None

def _disabled():
    global _AIRTABLE_DISABLED
    if _AIRTABLE_DISABLED is None:
        _AIRTABLE_DISABLED = not Config.AIRTABLE_TOKEN or Config.AIRTABLE_TOKEN.startswith('cambia') or not Config.AIRTABLE_BASE_ID
        if _AIRTABLE_DISABLED:
            log.info('Airtable no configurado — todos los leads se guardan solo en local')
    return _AIRTABLE_DISABLED

def _table_url(table_name):
    return f'{BASE_URL}/{Config.AIRTABLE_BASE_ID}/{table_name}'

def _request(method, table, data=None, params=None):
    if _disabled():
        return {'records': []}
    try:
        resp = requests.request(
            method, _table_url(table),
            headers=HEADERS, json=data, params=params,
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        log.warning(f'Airtable {method} {table}: {e}')
        return {'records': []}

def create_lead(lead):
    """Crea un nuevo lead en Airtable."""
    fields = {
        'LeadID': lead.get('id'),
        'Direccion': lead.get('direccion', ''),
        'Ciudad': lead.get('ciudad', ''),
        'Provincia': lead.get('provincia', ''),
        'CodigoPostal': lead.get('cp', ''),
        'AnoConstruccion': lead.get('ano_construccion', 0),
        'ValorCatastral': lead.get('valor_catastral', 0),
        'Superficie': lead.get('superficie', 0),
        'Score': lead.get('score', 0),
        'Fuente': lead.get('fuente', ''),
        'Estado': 'NUEVO',
        'FechaCreacion': lead.get('fecha', ''),
        'ZonaClimatica': lead.get('zona_climatica', ''),
        'URLReferencia': lead.get('url', ''),
        'Telefono': lead.get('telefono', ''),
        'Email': lead.get('email', ''),
        'NombreContacto': lead.get('nombre', ''),
    }
    return _request('POST', 'Leads', {'fields': fields})

def get_leads_by_status(status):
    """Obtiene leads por estado."""
    params = {
        'filterByFormula': f"{{Estado}} = '{status}'",
        'sort': ['-FechaCreacion'],
    }
    return _request('GET', 'Leads', params=params)

def update_lead_status(lead_id, status, extra_fields=None):
    """Actualiza estado de un lead."""
    fields = {'Estado': status}
    if extra_fields:
        fields.update(extra_fields)
    return _request('PATCH', 'Leads', {
        'records': [{'id': lead_id, 'fields': fields}]
    })

def assign_lead_to_company(lead_id, company_name, tier):
    """Asigna un lead a una empresa."""
    return update_lead_status(lead_id, 'ASIGNADO', {
        'Empresa': company_name,
        'Tier': tier,
    })

def record_visit(lead_id, gps_lat, gps_lon, foto_url=''):
    """Registra visita tecnica verificada."""
    return update_lead_status(lead_id, 'VISITA_OK', {
        'GPSLat': gps_lat,
        'GPSLon': gps_lon,
        'FotoURL': foto_url,
        'FechaVisita': __import__('datetime').datetime.now().isoformat(),
    })

def record_cierre(lead_id, contrato_url='', expediente_cae=''):
    return update_lead_status(lead_id, 'CERRADO', {
        'ContratoURL': contrato_url,
        'ExpedienteCAE': expediente_cae,
    })

def create_company(company_data):
    return _request('POST', 'Empresas', {'fields': company_data})

def get_pending_leads():
    return get_leads_by_status('PENDIENTE')

def get_companies_by_tier(tier):
    params = {
        'filterByFormula': f"{{Tier}} = '{tier}'",
    }
    return _request('GET', 'Empresas', params=params)
