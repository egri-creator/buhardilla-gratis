import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

class Config:
    # === MUNICIPIOS REALES DE AISLA SOLAR ===
    MUNICIPIOS = {
        'madrid': {
            'provincia': 'Madrid',
            'lat': 40.4168, 'lon': -3.7038, 'span': 0.8,
            'municipios': [
                'Madrid', 'Alcalá de Henares', 'Leganés', 'Getafe', 'Alcorcón',
                'Torrejón de Ardoz', 'Parla', 'Alcobendas', 'Las Rozas',
                'Pozuelo de Alarcón', 'Móstoles', 'Fuenlabrada', 'Majadahonda',
                'Collado Villalba', 'Aranjuez'
            ]
        },
        'avila': {
            'provincia': 'Ávila',
            'lat': 40.6569, 'lon': -4.6814, 'span': 0.8,
            'municipios': ['Ávila', 'Arévalo', 'El Barco de Ávila']
        },
        'burgos': {
            'provincia': 'Burgos',
            'lat': 42.3500, 'lon': -3.7000, 'span': 0.8,
            'municipios': ['Burgos', 'Miranda de Ebro', 'Aranda de Duero']
        },
        'leon': {
            'provincia': 'León',
            'lat': 42.5987, 'lon': -5.5671, 'span': 0.8,
            'municipios': ['León', 'Ponferrada', 'San Andrés del Rabanedo']
        },
        'palencia': {
            'provincia': 'Palencia',
            'lat': 42.0096, 'lon': -4.5313, 'span': 0.8,
            'municipios': ['Palencia', 'Aguilar de Campoo', 'Guardo']
        },
        'salamanca': {
            'provincia': 'Salamanca',
            'lat': 40.9650, 'lon': -5.6640, 'span': 0.8,
            'municipios': ['Salamanca', 'Béjar', 'Santa Marta de Tormes']
        },
        'segovia': {
            'provincia': 'Segovia',
            'lat': 40.9481, 'lon': -4.1184, 'span': 0.8,
            'municipios': ['Segovia', 'Cuéllar', 'El Espinar']
        },
        'soria': {
            'provincia': 'Soria',
            'lat': 41.7630, 'lon': -2.4660, 'span': 0.8,
            'municipios': ['Soria', 'Almazán', 'Ólvega']
        },
        'valladolid': {
            'provincia': 'Valladolid',
            'lat': 41.6523, 'lon': -4.7245, 'span': 0.8,
            'municipios': ['Valladolid', 'Medina del Campo', 'Laguna de Duero']
        },
        'zamora': {
            'provincia': 'Zamora',
            'lat': 41.5035, 'lon': -5.7442, 'span': 0.8,
            'municipios': ['Zamora', 'Benavente', 'Toro']
        },
        'navarra': {
            'provincia': 'Navarra',
            'lat': 42.8186, 'lon': -1.6459, 'span': 0.8,
            'municipios': [
                'Pamplona', 'Tudela', 'Barañáin', 'Burlada', 'Estella-Lizarra',
                'Villava', 'Berriozar', 'Ansoáin', 'Sarriguren', 'Tafalla',
                'Zizur Mayor', 'Sangüesa', 'Beriáin', 'Alsasua', 'Noáin'
            ]
        },
        'la_rioja': {
            'provincia': 'La Rioja',
            'lat': 42.4667, 'lon': -2.4500, 'span': 0.8,
            'municipios': [
                'Logroño', 'Calahorra', 'Arnedo', 'Alfaro', 'Haro', 'Lardero',
                'Nájera', 'Santo Domingo de la Calzada', 'Autol',
                'Rincón de Soto', 'Villamediana de Iregua', 'Quel',
                'Aldeanueva de Ebro', 'Cervera del Río Alhama'
            ]
        },
        'guadalajara': {
            'provincia': 'Guadalajara',
            'lat': 40.6300, 'lon': -3.1667, 'span': 0.8,
            'municipios': [
                'Guadalajara', 'Azuqueca de Henares', 'Cabanillas del Campo',
                'Alovera', 'Marchamalo', 'El Casar', 'Yunquera de Henares',
                'Molina de Aragón', 'Sigüenza', 'Brihuega', 'Pastrana',
                'Cifuentes', 'Sacedón'
            ]
        },
        'toledo': {
            'provincia': 'Toledo',
            'lat': 39.8667, 'lon': -3.9833, 'span': 0.8,
            'municipios': [
                'Toledo', 'Talavera de la Reina', 'Illescas', 'Torrijos',
                'Madridejos', 'Consuegra', 'Quintanar de la Orden', 'Ocaña',
                'Tembleque', 'Mora', 'Orgaz', 'Yepes', 'Villacañas'
            ]
        }
    }

    @classmethod
    def PROVINCIA_KEYS(cls):
        return list(cls.MUNICIPIOS.keys())

    @classmethod
    def TOTAL_MUNICIPIOS(cls):
        return sum(len(v['municipios']) for v in cls.MUNICIPIOS.values())

    @classmethod
    def ALL_MUNICIPIOS(cls):
        """Devuelve lista de (municipio, provincia_key, provincia_nombre)"""
        result = []
        for key, cfg in cls.MUNICIPIOS.items():
            for m in cfg['municipios']:
                result.append((m, key, cfg['provincia']))
        return result

    @classmethod
    def B2B_CITIES(cls):
        """Solo ciudades principales para busquedas B2B (cuestan $)"""
        big = [
            'Madrid', 'Alcalá de Henares', 'Leganés', 'Getafe', 'Alcorcón',
            'Torrejón de Ardoz', 'Parla', 'Alcobendas', 'Las Rozas',
            'Pozuelo de Alarcón', 'Móstoles', 'Fuenlabrada', 'Majadahonda',
            'Pamplona', 'Tudela', 'Barañáin', 'Logroño', 'Calahorra',
            'Valladolid', 'León', 'Burgos', 'Salamanca', 'Segovia',
            'Ávila', 'Palencia', 'Soria', 'Zamora', 'Ponferrada',
            'Miranda de Ebro', 'Aranda de Duero', 'Guadalajara',
            'Azuqueca de Henares', 'Toledo', 'Talavera de la Reina', 'Illescas',
        ]
        return [m for m in cls.ALL_MUNICIPIOS() if m[0] in big]

    # === SCORING ===
    SCORE_PESOS = {
        'antiguedad': 30,
        'superficie': 20,
        'tipo_via': 10,
        'cluster': 15,
        'fuente': 25,
    }
    SCORE_MINIMO = 60
    SCORE_ENTREGA = 60
    W_ANO_CONSTRUCCION = 35
    ZONA_SCORE = {'D3': 15, 'E1': 15, 'D2': 12, 'D1': 10}
    GROQ_MODEL = 'llama-3.1-8b-instant'

    # === COMISIONES ===
    COMISION_VISITA = 75
    COMISION_CIERRE = 200

    # === ZONAS CLIMATICAS (CTE DB-HE) ===
    ZONAS_CLIMATICAS = {
        'Madrid': 'D3', 'Ávila': 'E1', 'Burgos': 'E1', 'León': 'E1',
        'Palencia': 'E1', 'Salamanca': 'D2', 'Segovia': 'E1', 'Soria': 'E1',
        'Valladolid': 'D2', 'Zamora': 'D2', 'Navarra': 'D1',
        'La Rioja': 'D2', 'Guadalajara': 'D3', 'Toledo': 'D3',
    }

    # === API KEYS (desde .env) ===
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
    TELEGRAM_CHAT_ID_ADMIN = os.getenv('TELEGRAM_CHAT_ID_ADMIN', '')
    AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN', '')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID', '')
    SMTP_EMAIL = os.getenv('SMTP_EMAIL', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
    FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN', '')
    NEXTDOOR_TOKEN = os.getenv('NEXTDOOR_TOKEN', '')
    LINKEDIN_TOKEN = os.getenv('LINKEDIN_TOKEN', '')
    TIKTOK_TOKEN = os.getenv('TIKTOK_TOKEN', '')
    GMAIL_CREDS_FILE = 'credentials/gmail_token.json'

    # === DIRS ===
    DIRS = ['data', 'landing_pages', 'blog', 'sitemaps', 'screenshots', 'credentials']

Config = Config()
