"""Certificados Energeticos — busca viviendas con calificacion G/F (alta necesidad de mejora)"""
import requests
import re
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, generate_lead_id

log = setup_logging(__name__)

REGISTROS = [
    {'nombre': 'Castilla y Leon', 'url': 'https://www.energiam.jcyl.es', 'tipo': 'web'},
]

def search_cee_registro(provincia):
    """Busca certificados con calificacion energetica baja (G, F) en registros autonomicos."""
    leads = []
    log.info(f'CEE: buscando certificados en {provincia}...')
    return leads

def search_idealista_cee():
    """Busca Idealista para filtrar anuncios con certificado energetico G/F."""
    try:
        from src.sources.idealista_alerts import get_gmail_service
        service = get_gmail_service()
        if not service:
            return []
        from src.sources.idealista_alerts import search_idealista_emails
        emails = search_idealista_emails(service)
        leads = []
        for email in emails:
            texto = email.get('texto', '')
            if re.search(r'calificaci[oó]n energ[ée]tica.*[GF]', texto, re.IGNORECASE):
                email['fuente'] = 'certificado_energetico'
                email['score'] = 0
                leads.append(email)
        log.info(f'CEE Idealista: {len(leads)} viviendas con certificado G/F')
        return leads
    except Exception as e:
        log.warning(f'CEE no disponible: {e}')
        return []

def batch_complete():
    return search_idealista_cee()
