"""Pipeline de email SMTP real — envio automatizado con templates"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email(to_email, subject, html_body, text_body=''):
    """Envia email via Gmail SMTP."""
    try:
        user = Config.SMTP_EMAIL
        password = Config.SMTP_PASSWORD
        if user.startswith('cambia'):
            log.warning('SMTP_EMAIL no configurado')
            return False
        msg = MIMEMultipart('alternative')
        msg['From'] = user
        msg['To'] = to_email
        msg['Subject'] = subject
        if text_body:
            msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(user, password)
            server.sendmail(user, to_email, msg.as_string())
        log.info(f'Email enviado a {to_email}: {subject}')
        return True
    except Exception as e:
        log.error(f'Error enviando email a {to_email}: {e}')
        return False

TEMPLATE_ADMIN_FINCAS_HTML = '''
<html><body style="font-family:Arial;color:#333;">
<h2>Programa CAE: Aislamiento GRATIS para tus comunidades</h2>
<p>Hola {nombre},</p>
<p>He conseguido un programa que permite aislar buhardillas <strong>100% gratis</strong>
para los propietarios a través del programa CAE 2026.</p>
<p><strong>Sin coste para los vecinos. Sin obras molestas. Instalacion en 2h.</strong></p>
<p>Como administrador de fincas, puedes llevar este beneficio a todas tus comunidades.
Ademas, te ofrezco <strong>{comision}€ por cada comunidad que se acoja</strong>.</p>
<p>Solo tienes que reenviar este mensaje a tus grupos de WhatsApp:</p>
<div style="background:#f0f8ff;padding:15px;border-radius:8px;margin:15px 0;">
<p style="font-style:italic;">"Buenas vecinos, he conseguido que aislen la buhardilla
GRATIS a traves del programa CAE. Sin coste para vosotros.
Comprobad si sois elegibles aqui: {link}"</p>
</div>
<p>Tu link personal de tracking: <a href="{link}">{link}</a></p>
<p>Un saludo,<br/>{tu_nombre}</p>
<p style="font-size:11px;color:#999;">
Si no quieres recibir mas emails, responde "BAJA".</p>
</body></html>
'''

TEMPLATE_INMOBILIARIA_HTML = '''
<html><body style="font-family:Arial;color:#333;">
<h2>Valor anadido para tus clientes: aislamiento GRATIS</h2>
<p>Hola {nombre},</p>
<p>Vendes casas con buhardilla o atico? El programa CAE 2026 permite aislarlas
<strong>100% gratis</strong> para el comprador.</p>
<p>Esto significa que puedes ofrecer a tus clientes:
<ul>
<li>Una casa que ya viene con aislamiento termico (sin que ellos paguen)</li>
<li>Hasta 40% de ahorro en calefaccion desde el dia 1</li>
<li>Un argumento de venta diferencial frente a otros agentes</li>
</ul>
</p>
<p><strong>Tu comision: {comision}€ por cada cliente que se acoja.</strong>
Tu solo recomiendas, nosotros hacemos el resto.</p>
<p>Quieres que te explique como funciona en 5 minutos?</p>
<p>Un saludo,<br/>{tu_nombre}</p>
</body></html>
'''

TEMPLATE_EMPRESA_CAE_HTML = '''
<html><body style="font-family:Arial;color:#333;">
<h2>Leads de aislamiento CAE en {zona} — sin coste fijo</h2>
<p>Hola {nombre},</p>
<p>Soy lead generator especializado en el programa CAE de aislamiento de buhardillas.</p>
<p>Actualmente genero <strong>{cantidad} leads cualificados/semana</strong> en {zona}
a coste <strong>0€ para ti</strong>. Solo pagas por resultados:</p>
<ul>
<li><strong>{comision_visita}€</strong> por visita tecnica verificada (GPS + SMS cliente)</li>
<li><strong>{comision_cierre}€</strong> adicionales por obra cerrada</li>
</ul>
<p>Sin cuota fija. Sin riesgo. Sin inversion inicial.</p>
<p>Te paso los primeros <strong>5 leads GRATIS</strong> para que compruebes la calidad.</p>
<p>Hablamos?</p>
<p>{tu_nombre}</p>
</body></html>
'''

def send_admin_toolkit(admin_email, admin_nombre, link_unico, tu_nombre):
    return send_email(
        to_email=admin_email,
        subject=f'Programa CAE: aislamiento GRATIS para tus comunidades',
        html_body=TEMPLATE_ADMIN_FINCAS_HTML.format(
            nombre=admin_nombre, comision=Config.COMISION_ADMIN_FINCAS_EUR,
            link=link_unico, tu_nombre=tu_nombre
        ),
        text_body=f'Hola {admin_nombre}, te envio info del programa CAE. Link: {link_unico}'
    )

def send_empresa_oferta(empresa_email, empresa_nombre, zona, cantidad, tu_nombre):
    return send_email(
        to_email=empresa_email,
        subject=f'Leads de aislamiento CAE en {zona} — sin coste fijo',
        html_body=TEMPLATE_EMPRESA_CAE_HTML.format(
            nombre=empresa_nombre, zona=zona, cantidad=cantidad,
            comision_visita=Config.COMISION_VISITA_EUR,
            comision_cierre=Config.COMISION_CIERRE_EUR,
            tu_nombre=tu_nombre
        ),
        text_body=f'Hola {empresa_nombre}, genero leads CAE en {zona}. Sin coste fijo. {cantidad}/semana.'
    )

def send_inmobiliaria_oferta(email, nombre, comision, tu_nombre):
    return send_email(
        to_email=email,
        subject='Valor anadido para tus clientes: aislamiento GRATIS',
        html_body=TEMPLATE_INMOBILIARIA_HTML.format(
            nombre=nombre, comision=comision, tu_nombre=tu_nombre
        )
    )
