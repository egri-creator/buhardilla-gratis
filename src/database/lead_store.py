"""Almacenamiento local de leads con fallback automatico.
Cuando Airtable se llena (1000 records en free tier),
cae automaticamente a CSV/JSON local.
"""
import os
import json
import csv
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, save_json, load_json, save_csv

log = setup_logging(__name__)

LEADS_DIR = 'data/leads'
COMPANIES_DIR = 'data/companies'

AIRTABLE_MAX_RECORDS = 1000

def _count_airtable_records():
    try:
        from src.database.airtable_sync import _disabled
        if _disabled():
            return AIRTABLE_MAX_RECORDS + 1
        from src.database.airtable_sync import _request
        resp = _request('GET', 'Leads', params={'maxRecords': 1})
        if resp and resp.get('records'):
            total = len(resp['records'])
            if 'offset' in resp:
                return AIRTABLE_MAX_RECORDS + 1
            return total
    except:
        pass
    return AIRTABLE_MAX_RECORDS + 1

def save_lead(lead, force_local=False):
    """Guarda un lead. Intenta Airtable primero, cae a local si falla."""
    lead_id = lead.get('id', '')
    if not force_local:
        try:
            from src.database.airtable_sync import create_lead
            count = _count_airtable_records()
            if count < AIRTABLE_MAX_RECORDS:
                result = create_lead(lead)
                if result and result.get('records') and len(result['records']) > 0:
                    log.info(f'Lead {lead_id} guardado en Airtable')
                    return 'airtable'
            if count >= AIRTABLE_MAX_RECORDS:
                log.info(f'Airtable lleno ({count} records). Cambiando a local.')
        except Exception as e:
            log.warning(f'Airtable no disponible: {e}')
    os.makedirs(LEADS_DIR, exist_ok=True)
    today = datetime.now().strftime('%Y%m%d')
    filepath = f'{LEADS_DIR}/leads_{today}.json'
    existing = load_json(filepath) if os.path.exists(filepath) else []
    existing.append(lead)
    save_json(filepath, existing)
    csv_path = f'{LEADS_DIR}/leads_{today}.csv'
    existing_csv = []
    fieldnames = list(lead.keys())
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_csv = list(reader)
            if existing_csv:
                fieldnames = list(dict.fromkeys(list(existing_csv[0].keys()) + list(lead.keys())))
    existing_csv.append(lead)
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(existing_csv)
    log.info(f'Lead {lead_id} guardado en local ({len(existing)} total)')
    return 'local'

def save_company(company):
    """Guarda una empresa en JSON local."""
    os.makedirs(COMPANIES_DIR, exist_ok=True)
    companies = load_json(f'{COMPANIES_DIR}/active.json') if os.path.exists(f'{COMPANIES_DIR}/active.json') else []
    companies.append(company)
    save_json(f'{COMPANIES_DIR}/active.json', companies)
    log.info(f'Empresa {company.get("nombre", "?")} guardada')
    return True
