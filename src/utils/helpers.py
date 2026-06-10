"""Utilidades comunes para la Maquina CAE"""
import json
import csv
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logging(name, level='INFO'):
    Path('logs').mkdir(exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('logs/cae_machine.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout),
        ]
    )
    return logging.getLogger(name)

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def save_csv(path, data, fieldnames=None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if not data:
        return
    if not fieldnames:
        fieldnames = data[0].keys()
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def normalize_text(text):
    import re
    text = text.lower()
    text = re.sub(r'[áàäâ]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöô]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'ñ', 'n', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_lead_id(province, source):
    ts = datetime.now().strftime('%y%m%d%H%M%S')
    return f'{source[:3].upper()}-{province[:3].upper()}-{ts}'

ZONA_KEYWORDS_BUENAS = [
    'buhardilla', 'atico', 'desvan', 'tejado', 'cubierta',
    'aislar', 'aislamiento', 'aislante', 'rehabilitacion', 'reforma',
    'eficiencia energetica', 'calefaccion', 'factura', 'luz', 'gas',
    'calor', 'frio', 'temperatura', 'confort', 'ahorrar',
    'subvencion', 'ayuda', 'cae', 'certificado', 'next generation',
]

ZONA_KEYWORDS_MALAS = [
    'alquiler', 'hipoteca', 'vendo', 'compro', 'busco',
    'trabajo', 'empleo', 'se busca', 'gratis' '(sin contexto de aislamiento)',
]
