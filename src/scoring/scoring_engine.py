"""Motor de Scoring — clasifica leads usando reglas + Groq IA"""
import json
import requests
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

def score_lead(lead):
    """Calcula score 0-100 para un lead usando reglas + IA."""
    s = 0
    provincia = lead.get('provincia', '')
    ano = lead.get('ano_construccion', 0)
    fuente = lead.get('fuente', '')
    texto = lead.get('texto', '')
    valor_catastral = lead.get('valor_catastral', 0)
    superficie = lead.get('superficie', 0)

    # 1. Ano de construccion (hasta 35 pts)
    try:
        ano = int(ano)
        if ano < 1970: s += Config.W_ANO_CONSTRUCCION
        elif ano < 1990: s += Config.W_ANO_CONSTRUCCION * 0.7
        elif ano < 2000: s += Config.W_ANO_CONSTRUCCION * 0.3
        elif ano == 0: s += Config.W_ANO_CONSTRUCCION * 0.4
    except:
        s += Config.W_ANO_CONSTRUCCION * 0.4

    # 2. Zona climatica (hasta 15 pts)
    zona = Config.ZONAS_CLIMATICAS.get(provincia, 'D2')
    s += Config.ZONA_SCORE.get(zona, 8)

    # 3. Valor catastral (hasta 15 pts)
    try:
        vc = float(valor_catastral)
        if vc > 80000: s += 15
        elif vc > 50000: s += 10
        elif vc > 30000: s += 5
    except:
        s += 8

    # 4. Fuente (hasta 10 pts)
    peso_fuente = {
        'catastro_wfs': 8,
        'google_places_admin': 10,
        'google_alert': 6,
        'reddit': 4,
        'twitter': 4,
        'youtube_comments': 5,
        'idealista_alerta': 7,
        'linkedin_admin': 9,
        'foro': 5,
        'tiktok': 3,
    }
    s += peso_fuente.get(fuente, 5)

    # 5. Superficie (hasta 10 pts)
    try:
        sup = float(superficie)
        if sup > 150: s += 10
        elif sup > 100: s += 7
        elif sup > 60: s += 4
    except:
        s += 4

    # 6. Intencion de compra via Groq IA (hasta 15 pts) — solo si hay texto
    if texto:
        intento = classify_intent_groq(texto)
        s += intento * 15
        lead['intent_score'] = intento
    else:
        lead['intent_score'] = 0.5

    lead['score'] = round(min(s, 100), 1)
    lead['zona_climatica'] = zona
    return lead

def classify_intent_groq(texto):
    """Usa Groq API para clasificar intencion de compra (0.0-1.0)."""
    try:
        resp = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {Config.GROQ_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': Config.GROQ_MODEL,
                'messages': [
                    {'role': 'system', 'content': (
                        'Eres un clasificador de leads. Responde SOLO con un numero del 0.0 al 1.0 '
                        'indicando la probabilidad de que esta persona necesite aislamiento de buhardilla '
                        'en su vivienda. 0.0 = nada interesado, 1.0 = busca activamente solucion. '
                        'No expliques nada, solo el numero.'
                    )},
                    {'role': 'user', 'content': texto[:1000]},
                ],
                'temperature': 0.0,
                'max_tokens': 5,
            },
            timeout=10,
        )
        resp.raise_for_status()
        intent = float(resp.json()['choices'][0]['message']['content'].strip())
        return max(0.0, min(1.0, intent))
    except Exception as e:
        log.warning(f'Groq API error: {e}')
        return 0.5

def batch_score(leads):
    """Aplica scoring a una lista de leads."""
    scored = []
    for lead in leads:
        try:
            scored.append(score_lead(lead))
        except Exception as e:
            log.error(f'Error scoreando lead {lead.get("id", "?")}: {e}')
    scored.sort(key=lambda x: x.get('score', 0), reverse=True)
    log.info(f'Scoring: {len(scored)} leads clasificados (max: {scored[0]["score"] if scored else 0})')
    return scored

def filter_deliverable(scored_leads):
    """Filtra leads con score suficiente para entregar a empresas."""
    deliverable = [l for l in scored_leads if l.get('score', 0) >= Config.SCORE_ENTREGA]
    log.info(f'Entregables: {len(deliverable)}/{len(scored_leads)} leads con score >= {Config.SCORE_ENTREGA}')
    return deliverable
