"""Reporte diario — envia resumen HTML de leads a la bandeja del usuario.
Se ejecuta 1 vez al dia al final del pipeline.
"""
from datetime import datetime
from src.utils.helpers import setup_logging, load_json
from src.utils.gmail_helper import send_email, get_profile_email
from src.config.config_template import Config
from src.delivery.dashboard import generate_dashboard

log = setup_logging(__name__)

REPORT_TO = 'captacionleads25@gmail.com'

def generate_report(all_leads):
    """Generate and send daily report email + dashboard."""
    total = len(all_leads)
    
    # Group by source
    by_source = {}
    for l in all_leads:
        s = l.get('fuente', l.get('source', 'unknown'))
        by_source[s] = by_source.get(s, 0) + 1
    
    hot = [l for l in all_leads if l.get('score', 0) >= Config.SCORE_MINIMO]
    
    # Build suggested email copy for new portal leads
    suggested = ''
    portal_leads = [l for l in all_leads if 'nuroa' in l.get('fuente', '') or 'fotocasa' in l.get('fuente', '')]
    for l in portal_leads[:5]:
        city = l.get('ciudad', '')
        suggested += f'''
        <div style="background:#f9f9f9;padding:15px;margin:10px 0;border-radius:8px;border-left:4px solid #3498db;">
        <p><strong>Propiedad en {city}</strong> - {l.get('precio', '')}EUR</p>
        <p style="font-size:.85em;">{l.get('titulo', '')[:80]}</p>
        <p style="background:#fff;padding:10px;border-radius:5px;font-size:.85em;color:#555;">
        Copia esto: "Hola, veo que vendes una propiedad con buhardilla en {city}. 
        El programa CAE permite aislarla GRATIS. Te interesa?"</p>
        </div>'''
    
    html = f'''<html><body style="font-family:Arial;color:#333;">
    <h2>Reporte Diario - MAQUINA CAE</h2>
    <p style="color:#666;">{datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
    
    <div style="background:#e8f5e9;padding:20px;border-radius:10px;margin:20px 0;">
    <h3 style="margin:0;color:#27ae60;">Resumen</h3>
    <p><strong>{total}</strong> leads totales | <strong>{len(hot)}</strong> calientes | <strong>{len(portal_leads)}</strong> nuevos portales</p>
    </div>
    
    <h3>Leads por fuente</h3>
    <table style="width:100%;border-collapse:collapse;">
    ''' + ''.join(f'<tr><td style="padding:8px;border-bottom:1px solid #eef;">{s}</td><td style="padding:8px;border-bottom:1px solid #eef;"><strong>{c}</strong></td></tr>' for s, c in sorted(by_source.items(), key=lambda x: -x[1])) + '''
    </table>
    
    <h3>Emails sugeridos para hoy ({len(portal_leads)} portales nuevos)</h3>
    ''' + (suggested if suggested else '<p>No hay nuevos leads de portales hoy.</p>') + '''
    
    <h3>Dashboard</h3>
    <p>Abre el dashboard en: <a href="https://egri-creator.github.io/buhardilla-gratis/dashboard">egri-creator.github.io/buhardilla-gratis/dashboard</a></p>
    
    <p style="margin-top:30px;font-size:.85em;color:#999;">
    Generado automaticamente. Para cambiar la frecuencia, edita el cron en GitHub Actions.</p>
    </body></html>'''
    
    # Send email
    ok = send_email(REPORT_TO, f'Reporte CAE - {total} leads ({datetime.now().strftime("%d/%m")})', html)
    
    # Generate dashboard
    generate_dashboard(all_leads)
    
    return ok
