"""Auto-diagnostico v3 — verifica cada modulo de la MAQUINA CAE"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import importlib
import requests
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)
CHECKS = []

def check(name, fn): CHECKS.append((name, fn))
def ok(d=''): print(f'  \u2705 {d}' if d else '  \u2705')
def warn(d=''): print(f'  \u26a0\ufe0f  {d}' if d else '  \u26a0\ufe0f ')
def fail(d=''): print(f'  \u274c {d}' if d else '  \u274c')

check('Python version', lambda: ok(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}') if sys.version_info >= (3,10) else warn('Python >=3.10 recomendado'))

def _check_config():
    t = Config.TOTAL_MUNICIPIOS()
    (ok(f'{t} municipios cargados') if t >= 97 else warn(f'solo {t} municipios'))
check('Config carga', _check_config)

MODULOS = [
    'src.config.config_template',
    'src.utils.helpers', 'src.utils.dedup', 'src.utils.gmail_helper',
    'src.sources.catastro_wfs', 'src.sources.seo_landing_generator',
    'src.sources.blog_automation', 'src.sources.gbp_generator',
    'src.sources.admin_fincas', 'src.sources.company_finder',
    'src.sources.idealista_alerts', 'src.sources.google_alerts',
    'src.sources.ovc_enricher', 'src.sources.roof_checker',
    'src.sources.cluster_detector', 'src.sources.email_sender',
    'src.sources.certificados_energeticos',
    'src.sources.nuroa_scraper', 'src.sources.ine_api',
    'src.scoring.scoring_engine',
    'src.database.lead_store', 'src.database.airtable_sync',
    'src.delivery.telegram_bot',
    'src.delivery.email_campaign', 'src.delivery.daily_report',
    'src.delivery.reply_monitor', 'src.delivery.dashboard',
    'src.orchestrator',
]
check('29 modulos import', lambda: (
    ok('todos ok') if all(importlib.import_module(m) or True for m in MODULOS) else None
))

check('Catastro WFS', lambda: ok('API publica INSPIRE accesible') if requests.get('https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx', params={'service': 'WFS', 'version': '2.0.0', 'request': 'GetCapabilities'}, timeout=10).status_code == 200 else fail('no responde'))

check('Google API key', lambda: ok('configurada') if not Config.GOOGLE_API_KEY.startswith('cambia') else warn('sin key'))
check('Groq API key', lambda: ok('configurada') if not Config.GROQ_API_KEY.startswith('cambia') else warn('sin key'))
check('Directorios', lambda: ok('data/, logs/, landing_pages/') if all(os.path.exists(d) for d in ['data', 'logs', 'landing_pages']) else warn('faltan (se crean automaticamente)'))

def run_diagnostic():
    print(f'\n{"="*50}')
    print(f'  DIAGNOSTICO MAQUINA CAE v3.0')
    print(f'  {datetime.now().strftime("%d/%m/%Y %H:%M")}')
    print(f'{"="*50}\n')
    for name, fn in CHECKS:
        print(f'  {name}...')
        try: fn()
        except Exception as e: fail(f'excepcion: {e}')
    print(f'\n{"="*50}')
    print(f'  {len(CHECKS)} verificaciones')
    print(f'{"="*50}\n')

if __name__ == '__main__':
    run_diagnostic()
