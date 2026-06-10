"""Detector de clusters vecinales — encuentra edificios/grupos de parcelas elegibles.
Si en una misma calle/número hay 5+ parcelas elegibles, es un B2B opportunity 
(cliente administrador de fincas o presidente de comunidad).
"""
import re
import json
import os
from collections import defaultdict
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

MIN_CLUSTER_SIZE = 5

def normalize_street(address):
    """Extrae calle y número de una dirección."""
    if not address:
        return None
    address = address.strip().lower()
    address = re.sub(r'[^\w\sáéíóúñ0-9,/]', '', address)
    m = re.match(r'(.*?)(?:\s*[nN][oO]?\s*[.:]\s*)?(\d+)\s*.*', address)
    if m:
        street = m.group(1).strip()
        number = m.group(2)
        street = re.sub(r'\b(calle|cl|avda|avenida|plaza|pza|travesia|trva|camino|cno)\b', '', street).strip()
        return f'{street}, {number}'
    return address[:30]

def detect_clusters(leads):
    """Detecta clusters de parcelas elegibles en la misma dirección."""
    street_map = defaultdict(list)
    for lead in leads:
        addr = normalize_street(lead.get('direccion', ''))
        if addr:
            street_map[addr].append(lead)
    clusters = []
    for addr, group in street_map.items():
        if len(group) >= MIN_CLUSTER_SIZE:
            cluster = {
                'direccion': addr,
                'num_parcelas': len(group),
                'ciudad': group[0].get('ciudad', ''),
                'provincia': group[0].get('provincia', ''),
                'score_medio': sum(l.get('score', 0) for l in group) / len(group),
                'refs_catastrales': [l.get('ref_catastral', '') for l in group],
                'leads': group,
                'tipo': 'cluster_residencial',
                'potencial_b2b': len(group) >= 10,
            }
            clusters.append(cluster)
    clusters.sort(key=lambda c: c['num_parcelas'], reverse=True)
    log.info(f'Cluster detector: {len(clusters)} clusters de >= {MIN_CLUSTER_SIZE} parcelas')
    return clusters

def save_clusters(clusters):
    os.makedirs('data/clusters', exist_ok=True)
    with open('data/clusters/latest.json', 'w', encoding='utf-8') as f:
        json.dump(clusters, f, ensure_ascii=False, indent=2)
    log.info(f'Clusters guardados: data/clusters/latest.json')

def batch_complete():
    """Carga leads del último scrape y detecta clusters."""
    import glob
    all_leads = []
    for f in sorted(glob.glob('data/leads/scored_*.json'), reverse=True)[:2]:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                all_leads.extend(json.load(fh))
        except:
            pass
    if not all_leads:
        log.warning('No hay leads para detectar clusters')
        return []
    clusters = detect_clusters(all_leads)
    save_clusters(clusters)
    return clusters
