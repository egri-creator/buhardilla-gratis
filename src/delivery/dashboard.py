"""Genera dashboard HTML estatico con todos los leads.
Se despliega en Cloudflare Pages o GitHub Pages (gratis).
"""
import os, json
from datetime import datetime
from src.utils.helpers import setup_logging, load_json
from src.config.config_template import Config

log = setup_logging(__name__)
DASHBOARD_DIR = 'dashboard'

def generate_dashboard(all_leads=None):
    """Generate static dashboard HTML with all leads data."""
    os.makedirs(DASHBOARD_DIR, exist_ok=True)
    
    # Load leads from latest file if not provided
    if all_leads is None:
        all_leads = []
        leads_dir = 'data/leads'
        if os.path.exists(leads_dir):
            files = sorted([f for f in os.listdir(leads_dir) if f.endswith('.json')], reverse=True)
            for f in files[:5]:
                data = load_json(f'{leads_dir}/{f}')
                if isinstance(data, list):
                    all_leads.extend(data)
    
    # Stats
    total = len(all_leads)
    scored = [l for l in all_leads if l.get('score', 0) > 0]
    hot = [l for l in all_leads if l.get('score', 0) >= Config.SCORE_MINIMO]
    
    # Group by source
    by_source = {}
    for l in all_leads:
        s = l.get('fuente', l.get('source', 'unknown'))
        by_source[s] = by_source.get(s, 0) + 1
    
    # Table rows
    rows = ''
    for l in all_leads[:200]:  # Max 200 for perf
        score = l.get('score', 0)
        badge = 'hot' if score >= Config.SCORE_MINIMO else 'warm' if score > 0 else 'cold'
        rows += f'''<tr class="{badge}">
            <td>{l.get('fecha', l.get('date', ''))[:10]}</td>
            <td>{l.get('fuente', l.get('source', ''))}</td>
            <td>{l.get('titulo', l.get('nombre', l.get('title', '')))[:60]}</td>
            <td>{l.get('ciudad', l.get('city', ''))}</td>
            <td>{l.get('precio', l.get('price', ''))}</td>
            <td><span class="badge {badge}">{score}</span></td>
            <td>{l.get('email', '')}</td>
            <td>{l.get('telefono', '')[:12]}</td>
        </tr>'''
    
    html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard - MAQUINA CAE</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,sans-serif;background:#f5f6fa;color:#333;padding:20px;}}
.header{{background:#1a5276;color:#fff;padding:20px 30px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-between;align-items:center;}}
.header h1{{font-size:1.5em;}} .header .date{{font-size:.85em;opacity:.8;}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:15px;margin-bottom:25px;}}
.stat{{background:#fff;padding:20px;border-radius:10px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.06);}}
.stat .num{{font-size:2em;font-weight:bold;color:#1a5276;}} .stat .label{{font-size:.85em;color:#666;}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.06);}}
th{{background:#1a5276;color:#fff;padding:12px 15px;text-align:left;font-size:.85em;}}
td{{padding:10px 15px;border-bottom:1px solid #eef;font-size:.85em;}}
tr:hover{{background:#f0f7ff;}}
.hot td{{border-left:3px solid #27ae60;}} .warm td{{border-left:3px solid #f39c12;}} .cold td{{border-left:3px solid #bdc3c7;}}
.badge{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.8em;font-weight:bold;color:#fff;}}
.badge.hot{{background:#27ae60;}} .badge.warm{{background:#f39c12;}} .badge.cold{{background:#95a5a6;}}
.sources{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;}}
.src-tag{{background:#e8f0fe;padding:4px 12px;border-radius:15px;font-size:.8em;color:#1a5276;}}
.footer{{text-align:center;margin-top:30px;font-size:.8em;color:#999;}}
</style></head><body>
<div class="header"><div><h1>MAQUINA CAE - Dashboard de Leads</h1><div class="date">Actualizado: {datetime.now().strftime("%d/%m/%Y %H:%M")}</div></div></div>
<div class="stats">
<div class="stat"><div class="num">{total}</div><div class="label">Total leads</div></div>
<div class="stat"><div class="num">{len(hot)}</div><div class="label">Calientes</div></div>
<div class="stat"><div class="num">{len(scored)}</div><div class="label">Con score</div></div>
</div>
<div class="sources">''' + ''.join(f'<span class="src-tag">{s}: {c}</span>' for s, c in sorted(by_source.items(), key=lambda x: -x[1])) + '''</div>
<table><thead><tr><th>Fecha</th><th>Fuente</th><th>Titulo</th><th>Ciudad</th><th>Precio</th><th>Score</th><th>Email</th><th>Telefono</th></tr></thead><tbody>''' + rows + '''</tbody></table>
<div class="footer">Generado automaticamente por MAQUINA CAE | Datos locales</div>
</body></html>'''
    
    path = f'{DASHBOARD_DIR}/index.html'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    log.info(f'Dashboard generado: {path} ({total} leads)')
    return path
