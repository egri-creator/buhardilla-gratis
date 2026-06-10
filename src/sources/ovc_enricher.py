"""Enriquecedor OVC — APIs publica del Catastro descontinuada.
Se mantiene como stub: devuelve datos basicos usando solo la referencia.
"""
from datetime import datetime

def batch_complete(leads=None):
    from src.utils.helpers import setup_logging
    log = setup_logging(__name__)
    if not leads:
        return []
    enriched = []
    for lead in leads:
        lead['fuente_enriquecida'] = 'ovc'
        enriched.append(lead)
    log.info(f'OVC: {len(enriched)} leads (enriquecimiento saltado — API Catastro no disponible)')
    return enriched

def batch_enrich(leads):
    return batch_complete(leads)
