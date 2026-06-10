"""Google Business Profile generator — descripciones + posts por ciudad.
Crea el contenido optimizado para perfiles de Google en cada ciudad.
Sin coste, 100% automatizado.
"""
import os
import json
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

GBP_DIR = 'gbp_data'

def generate_gbp_profile(ciudad):
    """Genera datos optimizados para Google Business Profile de una ciudad."""
    profile = {
        'business_name': f'Aislamiento Buhardilla {ciudad}',
        'category': 'Instalador de aislamientos',
        'description': (
            f'Instaladores especializados en aislamiento de buhardillas en {ciudad} '
            f'y toda la provincia. Programa CAE 2026: aislamiento GRATIS para propietarios. '
            f'Instalacion en 2h, sin obras, 30 años de garantia. '
            f'Comprueba si tu vivienda es elegible sin coste.'
        ),
        'services': [
            'Aislamiento de buhardilla gratuito (Programa CAE)',
            'Aislamiento termico de cubiertas',
            'Mejora de eficiencia energetica',
            'Certificados de ahorro energetico',
        ],
        'keywords': [
            f'aislamiento buhardilla {ciudad}',
            f'aislar buhardilla gratis {ciudad}',
            f'programa CAE {ciudad}',
            f'instalador aislamiento {ciudad}',
        ],
        'posts': [
            {
                'title': f'Aislamiento GRATIS de buhardilla en {ciudad}',
                'body': f'El Programa CAE 2026 cubre el 100% del aislamiento de tu buhardilla en {ciudad}. Sin obras, sin coste, sin papeleo. Comprueba si eres elegible.',
                'cta': 'Comprobar elegibilidad',
                'url': f'https://egri-creator.github.io/buhardilla-gratis/?ref=gbp_{ciudad.lower()}',
            },
            {
                'title': f'¿Ahorra hasta un 40% en calefacción en {ciudad}',
                'body': f'El aislamiento de buhardilla reduce tu factura de calefaccion entre un 30% y 40%. Y con el programa CAE, te sale GRATIS. Infórmate sin compromiso.',
                'cta': 'Saber mas',
                'url': f'https://egri-creator.github.io/buhardilla-gratis/?ref=gbp_{ciudad.lower()}_ahorro',
            },
        ],
        'ciudad': ciudad,
        'generado': datetime.now().isoformat(),
    }
    return profile

def generate_all():
    """Genera perfiles GBP para todos los municipios de Buhardilla Gratis."""
    os.makedirs(GBP_DIR, exist_ok=True)
    profiles = []
    for ciudad, key, provincia in Config.ALL_MUNICIPIOS():
        profile = generate_gbp_profile(ciudad)
        profiles.append(profile)
    with open(f'{GBP_DIR}/gbp_profiles.json', 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)
    log.info(f'GBP: {len(profiles)} perfiles generados en {Config.TOTAL_MUNICIPIOS()} municipios')
    return profiles

def batch_complete():
    return generate_all()
