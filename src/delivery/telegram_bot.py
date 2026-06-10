"""Notificaciones por Gmail API (sin 2FA ni App Password)"""
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging
from src.utils.gmail_helper import send_email

log = setup_logging(__name__)
NOTIFY_TO = Config.SMTP_EMAIL or 'captacionleads25@gmail.com'

def notify_new_leads(leads):
    body = f'<h2>Nuevos Leads CAE ({len(leads)})</h2><ul>'
    for l in leads:
        score = l.get('score', 0)
        body += f'<li><b>{l.get("id","?")}</b> | Score: {score} | {l.get("provincia","?")} | {l.get("fuente","?")}</li>'
    body += '</ul>'
    send_email(NOTIFY_TO, f'CAE: {len(leads)} nuevos leads', body)

def notify_error(stage, error_msg):
    send_email(NOTIFY_TO, f'ERROR CAE: {stage}', f'<pre>{error_msg[:500]}</pre>')

def notify_daily_summary(stats):
    body = f'''
    <h2>Resumen Diario CAE</h2>
    <p>Leads: {stats.get("generados",0)}</p>
    <p>Entregados: {stats.get("entregados",0)}</p>
    <p>Visitas: {stats.get("visitas",0)}</p>
    <p>Cierres: {stats.get("cierres",0)}</p>
    <p>Ingreso hoy: {stats.get("ingreso_hoy",0)}€</p>
    '''
    send_email(NOTIFY_TO, 'Resumen Diario CAE', body)
