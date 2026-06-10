"""Orquestador PERFECTO — solo lo que genera leads reales"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, save_json
from src.utils.dedup import filter_duplicates
from src.scoring.scoring_engine import batch_score
from src.delivery.telegram_bot import notify_new_leads, notify_error
from src.delivery.daily_report import generate_report
from src.delivery.reply_monitor import detect_replies
from src.delivery.email_campaign import batch_campaign
from src.database.lead_store import save_lead
from src.sources import (
    catastro_wfs, admin_fincas, idealista_alerts, google_alerts, company_finder,
    seo_landing_generator, blog_automation, gbp_generator,
    nuroa_scraper, ine_api,
)
from src.sources.ovc_enricher import batch_enrich
from src.sources.cluster_detector import detect_clusters

log = setup_logging(__name__)
DATA_DIR = 'data'

def ensure_dirs():
    for d in [f'{DATA_DIR}/leads', f'{DATA_DIR}/companies', f'{DATA_DIR}/stats',
              f'{DATA_DIR}/clusters', 'logs', 'landing_pages', 'blog', 'gbp_data', 'dashboard']:
        os.makedirs(d, exist_ok=True)

def run_source(name, fn, *args):
    try:
        result = fn(*args) if args else fn()
        count = len(result) if isinstance(result, list) else (result if isinstance(result, (int, float)) else 0)
        log.info(f'{name}: {count}')
        return result if isinstance(result, list) else ([result] if result else [])
    except Exception as e:
        notify_error(f'Fuente {name}', str(e))
        log.error(f'Error {name}: {e}')
        return []

def pipeline_completo():
    ensure_dirs()
    log.info('=' * 60)
    log.info('MAQUINA CAE PERFECTA — 5 PILARES, 0€')
    log.info('=' * 60)

    todos_los_leads = []

    log.info('\n--- FASE 1: EXTRACCION (Catastro + Portales + Alertas) ---')
    fuentes = [
        ('Catastro WFS', catastro_wfs.batch_complete),
        ('Admin Fincas', admin_fincas.batch_complete),
        ('Idealista', idealista_alerts.batch_complete),
        ('Google Alerts', google_alerts.monitor_alerts),
        ('Nuroa (Fotocasa/Idealista)', nuroa_scraper.batch_complete),
    ]
    for name, fn in fuentes:
        todos_los_leads.extend(run_source(name, fn))

    if todos_los_leads:
        fname = f'{DATA_DIR}/leads/raw_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
        save_json(fname, todos_los_leads)
        log.info(f'Total crudos: {len(todos_los_leads)}')

        log.info('\n--- FASE 2: OVC ENRICHMENT ---')
        run_source('OVC', batch_enrich, todos_los_leads)

        log.info('\n--- FASE 3: SCORING + DEDUP + CLUSTERS ---')
        unicos = filter_duplicates(todos_los_leads)
        scored = batch_score(unicos)
        save_json(f'{DATA_DIR}/leads/scored_{datetime.now().strftime("%Y%m%d_%H%M")}.json', scored)
        for lead in scored:
            save_lead(lead)
        deliverable = [l for l in scored if l.get('score', 0) >= Config.SCORE_MINIMO]
        if deliverable:
            notify_new_leads(deliverable[:15])
        run_source('Clusters', detect_clusters, scored)
        log.info(f'Leads entregables: {len(deliverable)}')

    log.info('\n--- FASE 4: SEO + CONTENIDO ---')
    run_source('Landing Pages', seo_landing_generator.batch_complete)
    run_source('Blog', blog_automation.batch_complete)
    run_source('GBP', gbp_generator.batch_complete)

    log.info('\n--- FASE 5: B2B + MERCADO ---')
    run_source('Company Finder', company_finder.batch_complete)
    run_source('INE Market', ine_api.batch_complete)

    log.info('\n--- FASE 6: ENTREGA (email + dashboard) ---')
    if todos_los_leads:
        run_source('Campana Email', batch_campaign, todos_los_leads)
    run_source('Monitor Respuestas', detect_replies, 24)
    run_source('Reporte Diario', generate_report, todos_los_leads)

    log.info('\n=== PIPELINE COMPLETADO ===')

if __name__ == '__main__':
    pipeline_completo()
