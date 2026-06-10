"""Dashboard web local — Flask. Sin depender de Airtable, lee de JSON local."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from flask import Flask, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = type('Flask', (), {'__call__': lambda *a: None})

from src.utils.helpers import load_json, save_json
from datetime import datetime
import glob
import json

app = Flask(__name__) if FLASK_AVAILABLE else None
DATA_DIR = 'data'

if not FLASK_AVAILABLE:
    import sys
    sys.modules[__name__].app = None

def load_all_leads():
    leads = []
    for f in sorted(glob.glob(f'{DATA_DIR}/leads/*.json'), reverse=True)[:5]:
        leads.extend(load_json(f))
    return leads

def load_all_companies():
    return load_json('data/companies/active.json') if os.path.exists('data/companies/active.json') else []

@app.route('/')
def index():
    leads = load_all_leads()
    companies = load_all_companies()
    total = len(leads)
    scored = len([l for l in leads if l.get('score', 0) > 0])
    deliverable = len([l for l in leads if l.get('score', 0) >= 60])
    by_source = {}
    for l in leads:
        s = l.get('fuente', 'desconocida')
        by_source[s] = by_source.get(s, 0) + 1
    by_province = {}
    for l in leads:
        p = l.get('provincia', 'desconocida')
        by_province[p] = by_province.get(p, 0) + 1
    return jsonify({
        'total_leads': total,
        'scored': scored,
        'deliverable': deliverable,
        'by_source': dict(sorted(by_source.items(), key=lambda x: -x[1])),
        'by_province': dict(sorted(by_province.items(), key=lambda x: -x[1])),
        'companies': len(companies),
        'last_update': datetime.now().isoformat(),
    })

@app.route('/leads')
def list_leads():
    leads = load_all_leads()
    source = request.args.get('fuente', '')
    if source:
        leads = [l for l in leads if l.get('fuente') == source]
    provincia = request.args.get('provincia', '')
    if provincia:
        leads = [l for l in leads if l.get('provincia') == provincia]
    min_score = request.args.get('min_score', 0, type=int)
    if min_score:
        leads = [l for l in leads if l.get('score', 0) >= min_score]
    leads.sort(key=lambda x: x.get('score', 0), reverse=True)
    return jsonify(leads[:200])

@app.route('/stats')
def stats():
    leads = load_all_leads()
    total = len(leads)
    if total == 0:
        return jsonify({'msg': 'sin datos'})
    avg_score = sum(l.get('score', 0) for l in leads) / total
    return jsonify({
        'total': total,
        'avg_score': round(avg_score, 1),
        'max_score': max(l.get('score', 0) for l in leads),
        'fuentes_activas': len(set(l.get('fuente', '') for l in leads)),
    })

def run_dashboard(port=5000):
    print(f'? Dashboard CAE corriendo en http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    run_dashboard()
