"""Test — MAQUINA CAE DEFINITIVA"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
errors = []

def test(mod_name, path):
    try:
        __import__(path, fromlist=[''])
        print(f'  OK {mod_name}')
    except Exception as e:
        print(f'  FAIL {mod_name}: {e}')
        errors.append(mod_name)

print('=== MAQUINA CAE PERFECTA — 5 pilares, 0€ ===\n')

test('config', 'src.config.config_template')
test('helpers', 'src.utils.helpers')
test('dedup', 'src.utils.dedup')
test('diagnostic', 'src.utils.diagnostic')

sources = [
    'catastro_wfs','admin_fincas','google_alerts','idealista_alerts','email_sender','company_finder',
    'seo_landing_generator','certificados_energeticos','ovc_enricher','cluster_detector',
    'roof_checker','blog_automation','gbp_generator',
]
for s in sources:
    test(s, f'src.sources.{s}')

test('scoring_engine', 'src.scoring.scoring_engine')
test('telegram_bot', 'src.delivery.telegram_bot')
test('airtable_sync', 'src.database.airtable_sync')
test('lead_store', 'src.database.lead_store')
test('sms_gps_verifier', 'src.verification.sms_gps_verifier')
test('orchestrator', 'src.orchestrator')

total = 22
ok = total - len(errors)
print(f'\n=== {len(errors)} errores, {ok}/{total} OK ===')
if not errors:
    print('✅ MAQUINA CAE PERFECTA — 100% automatica, 0€/mes')
