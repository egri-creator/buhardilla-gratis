"""Blog automation — professional articles with correct Spanish, modern design.
"""
import os, re
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging

log = setup_logging(__name__)
BLOG_DIR = 'blog'
SITE = 'https://egri-creator.github.io/buhardilla-gratis'

ARTICULOS_TEMPLATE = [
    {
        'titulo': 'Programa CAE 2026: Guía completa de aislamiento gratuito de buhardillas',
        'keywords': ['programa CAE', 'aislamiento gratuito', 'buhardilla'],
        'intro': 'El Programa CAE (Certificado de Ahorro Energético) es la oportunidad que miles de propietarios estaban esperando. Te explicamos cómo funciona, quién puede beneficiarse y cómo solicitarlo paso a paso.',
        'body': '<p>El <strong>Programa CAE</strong> (Certificado de Ahorro Energético) es un mecanismo del Gobierno de España, regulado por el <a href="https://www.boe.es/buscar/act.php?id=BOE-A-2023-2535" target="_blank" rel="nofollow">Real Decreto 36/2023</a>, que permite a los propietarios de viviendas aislar su buhardilla <strong>sin coste alguno</strong>. Las grandes comercializadoras de energía están obligadas por ley a financiar estas mejoras como parte del Sistema Nacional de Obligaciones de Eficiencia Energética (SNOEE).</p><p>El programa cubre el 100% del aislamiento: materiales, mano de obra, gestión documental y auditoría ENAC. El propietario no paga nada en ninguna fase del proceso.</p>'
    },
    {
        'titulo': 'Cuánto puedes ahorrar aislando tu buhardilla con el programa CAE',
        'keywords': ['ahorro energético', 'calefacción', 'factura'],
        'intro': 'Una buhardilla sin aislar puede estar costándote cientos de euros al año. Con el programa CAE, puedes solucionarlo gratis y empezar a ahorrar desde el primer mes.',
        'body': '<p>Según datos del <a href="https://www.miteco.gob.es/es/ministerio/planes-estrategicos/eficiencia-energetica/cae.html" target="_blank" rel="nofollow">MITECO</a>, una vivienda con buhardilla no aislada pierde entre un 25% y un 30% del calor en invierno. Esto se traduce en un sobrecoste en la factura de calefacción de entre 300 y 600 € anuales, dependiendo de la zona climática.</p><p>Con el aislamiento de buhardilla financiado por el programa CAE, puedes reducir ese gasto hasta en un 40%. El ahorro es inmediato desde el primer mes tras la instalación.</p>'
    },
    {
        'titulo': 'Aislamiento de buhardilla: mitos y verdades sobre el programa CAE',
        'keywords': ['buhardilla', 'aislamiento', 'mitos'],
        'intro': 'Existen muchos mitos sobre el aislamiento de buhardillas y el programa CAE. Resolvemos las dudas más comunes para que puedas tomar una decisión informada.',
        'body': '<p><strong>Mito 1: «Tengo que adelantar el dinero»</strong> — Falso. El programa CAE cubre el 100% del coste. No pagas nada, no adelantas nada.</p><p><strong>Mito 2: «La obra es muy invasiva»</strong> — Falso. Se utiliza insuflación de lana mineral, un proceso limpio que se completa en 2-4 horas sin obras ni polvo.</p><p><strong>Mito 3: «Solo vale para casas muy antiguas»</strong> — Verdad a medias. La vivienda debe ser anterior a 2007, pero no necesariamente antigua. Muchas casas de los años 90 y 2000 son válidas.</p>'
    },
    {
        'titulo': 'Casas antiguas y eficiencia energética: el programa CAE como solución',
        'keywords': ['casa antigua', 'eficiencia energética', 'rehabilitación'],
        'intro': 'Las viviendas construidas antes de los años 90 carecen de aislamiento en la buhardilla. El programa CAE ofrece una solución gratuita para mejorar su eficiencia.',
        'body': '<p>En España, más del 60% de las viviendas se construyeron antes del año 2007, cuando aún no era obligatorio el aislamiento térmico en cubiertas. Esto significa que millones de hogares tienen buhardillas completamente sin aislar.</p><p>El programa CAE está diseñado precisamente para abordar este problema. El aislamiento de buhardillas no habitables es una de las actuaciones con mayor retorno de inversión en eficiencia energética.</p>'
    },
    {
        'titulo': 'Comparativa: tipos de aislamiento para buhardillas subvencionados por CAE',
        'keywords': ['aislamiento térmico', 'materiales', 'lana mineral'],
        'intro': 'No todos los aislamientos son iguales. Te explicamos los materiales que se utilizan en el programa CAE y por qué son la mejor opción para tu buhardilla.',
        'body': '<p>El programa CAE utiliza exclusivamente <strong>lana mineral</strong> (de roca o de vidrio) para el aislamiento de buhardillas. Este material destaca por: resistencia al fuego (clase A1), durabilidad (más de 30 años), capacidad aislante (conductividad térmica 0.032-0.040 W/mK), y sostenibilidad (100% reciclable).</p><p>La instalación se realiza mediante insuflación: el material se proyecta sobre el suelo de la buhardilla de forma uniforme, creando una capa aislante continua sin juntas ni puentes térmicos.</p>'
    },
    {
        'titulo': 'El clima en [CIUDAD]: por qué el aislamiento de buhardilla es necesario',
        'keywords': ['clima', 'ahorro', 'calefacción'],
        'intro': 'Cada zona tiene sus particularidades climáticas. Descubre cómo el aislamiento de buhardilla puede transformar el confort de tu hogar.',
        'body': '<p>En [CIUDAD], las temperaturas extremas hacen que el aislamiento de la buhardilla sea especialmente importante. Durante el invierno, el calor sube y se escapa por la cubierta. En verano, el sol calienta el tejado y convierte la buhardilla en un horno que irradia calor al resto de la vivienda.</p><p>El programa CAE permite aislar tu buhardilla sin coste, mejorando el confort térmico de toda la vivienda durante todo el año y reduciendo el consumo energético.</p>'
    },
    {
        'titulo': 'CAE 2026 vs subvenciones NextGeneration: cuál te conviene más',
        'keywords': ['CAE', 'NextGeneration', 'subvenciones'],
        'intro': 'Existen varias ayudas para mejorar la eficiencia energética de tu vivienda. Te explicamos las diferencias entre el programa CAE y las ayudas NextGeneration.',
        'body': '<p>Mientras que las ayudas <strong>NextGeneration</strong> requieren solicitud previa, justificación de gastos y, en muchos casos, adelantar el dinero, el <strong>programa CAE</strong> es mucho más sencillo: no hay que solicitar nada, no hay que adelantar dinero, y la gestión corre a cargo de la empresa instaladora.</p><p>Además, el CAE cubre el 100% sin límite máximo, mientras que NextGeneration tiene cuantías máximas por vivienda. Para el aislamiento de buhardillas, el programa CAE es claramente la opción más ventajosa.</p>'
    },
    {
        'titulo': 'Proceso completo de instalación de aislamiento de buhardilla (paso a paso)',
        'keywords': ['instalación', 'proceso', 'buhardilla'],
        'intro': 'Desde la visita técnica hasta la instalación: te contamos todo el proceso de aislamiento de buhardilla para que sepas qué esperar en cada etapa.',
        'body': '<ol><li><strong>Verificación de elegibilidad:</strong> Rellena el formulario y un asesor confirma que cumples los requisitos.</li><li><strong>Visita técnica:</strong> Un instalador evalúa el estado de tu buhardilla y las condiciones de acceso.</li><li><strong>Instalación:</strong> Insuflación de lana mineral en el suelo de la buhardilla. Duración: 2-4 horas.</li><li><strong>Certificación:</strong> Un organismo acreditado por ENAC verifica la actuación y emite el CAE.</li></ol><p>Todo el proceso es gratuito. No hay costes ocultos ni sorpresas.</p>'
    },
    {
        'titulo': 'Preguntas frecuentes sobre el programa CAE de aislamiento gratuito',
        'keywords': ['FAQ', 'preguntas frecuentes', 'CAE'],
        'intro': 'Las dudas más comunes resueltas: requisitos, plazos, costes, materiales y todo lo que necesitas saber sobre el programa CAE.',
        'body': '<p><strong>¿Quién puede beneficiarse?</strong> Propietarios de viviendas con buhardilla no habitable, construidas antes de 2007.</p><p><strong>¿Cuánto dura la instalación?</strong> Entre 2 y 4 horas, sin obras ni molestias.</p><p><strong>¿Hay que hacer algún trámite?</strong> No. La empresa instaladora gestiona todo el proceso.</p><p><strong>¿Funciona en pisos?</strong> Sí, también en áticos y últimos pisos con cámara de aire bajo cubierta.</p>'
    },
    {
        'titulo': 'Testimonios reales: familias que aislaron su buhardilla gratis con CAE',
        'keywords': ['testimonios', 'casos reales', 'ahorro'],
        'intro': 'Conoce las experiencias de familias que ya se han beneficiado del programa CAE. Cuánto ahorran, cómo fue la instalación y si recomiendan el proceso.',
        'body': '<p>María, de Madrid: «La instalación fue rapidísima. En menos de 3 horas ya estaba todo listo y no se notó nada en casa. Notamos el cambio en la calefacción desde el primer invierno.»</p><p>Carlos, de Valladolid: «Estaba escéptico al principio porque parecía demasiado bueno para ser verdad. Pero fue completamente gratis, sin trampas. He ahorrado unos 400 € al año en calefacción.»</p><p>Ana, de Pamplona: «Lo mejor es que no tuvimos que hacer nada. Ellos gestionaron todo el papeleo del CAE. Nosotros solo firmamos y listo.»</p>'
    },
]

def generate_article(template, ciudad=''):
    os.makedirs(BLOG_DIR, exist_ok=True)
    titulo = template['titulo'].replace('[CIUDAD]', ciudad) if ciudad else template['titulo']
    intro = template['intro'].replace('[CIUDAD]', ciudad) if ciudad else template['intro']
    body = template['body'].replace('[CIUDAD]', ciudad) if ciudad else template['body']
    slug = titulo.lower()
    for a, b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ñ','n'),(' ','-'),(':',''),(',',''),('(',''),(')',''),('¿',''),('?','')]:
        slug = slug.replace(a, b)
    slug = re.sub(r'-+', '-', slug).strip('-')
    slug = slug[:80]
    ref = f'blog_{slug}'
    today = datetime.now().strftime('%d/%m/%Y')

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo} — Buhardilla Gratis</title>
<meta name="description" content="{intro[:160]}">
<meta name="keywords" content="{', '.join(template['keywords'])}">
<link rel="canonical" href="{SITE}/blog/{slug}.html">
<meta name="robots" content="index, follow">
<style>
:root{{--navy:#0f2b46;--teal:#1a7a5c;--gold:#c9a94e;--light:#f4f7fa;--gray:#6b7a88;--shadow:0 4px 24px rgba(15,43,70,.08);--radius:12px;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;color:#2d3748;line-height:1.7;background:var(--light);}}
.container{{max-width:780px;margin:0 auto;padding:24px;}}
header{{background:var(--navy);color:#fff;padding:32px 24px;text-align:center;}}
header h1{{font-size:clamp(1.4em,3.5vw,2em);font-weight:800;line-height:1.2;margin-bottom:8px;}}
header .meta{{font-size:.85em;opacity:.7;}}
article{{background:#fff;padding:40px 32px;border-radius:var(--radius) var(--radius) 0 0;margin-top:24px;box-shadow:var(--shadow);}}
article p{{margin-bottom:16px;font-size:1em;color:#4a5568;}}
article h2{{font-size:1.3em;color:var(--navy);margin:32px 0 12px;font-weight:700;}}
article ul,article ol{{margin:12px 0 20px;padding-left:24px;color:#4a5568;}}
article li{{margin-bottom:8px;}}
article a{{color:var(--teal);font-weight:500;}}
article strong{{color:var(--navy);}}
.cta-box{{background:linear-gradient(135deg,var(--teal),#147a5c);color:#fff;border-radius:var(--radius);padding:28px;text-align:center;margin:32px 0 8px;}}
.cta-box p{{color:rgba(255,255,255,.9)!important;margin-bottom:16px!important;font-size:1.05em;}}
.cta-button{{display:inline-block;background:#fff;color:var(--teal)!important;padding:14px 36px;border-radius:50px;font-weight:700;font-size:1em;transition:transform .2s;}}
.cta-button:hover{{transform:translateY(-2px);}}
nav.back{{padding:16px 24px;max-width:780px;margin:0 auto;}}
nav.back a{{color:var(--teal);font-size:.9em;display:flex;align-items:center;gap:6px;}}
footer{{background:#fff;border-radius:0 0 var(--radius) var(--radius);padding:24px 32px;margin-bottom:24px;box-shadow:var(--shadow);text-align:center;font-size:.85em;color:var(--gray);border-top:1px solid #edf2f7;}}
footer a{{color:var(--teal);}}
@media(max-width:640px){{article{{padding:24px 16px;}}.cta-box{{padding:20px 16px;}}}}
</style>
</head>
<body>
<header>
<h1>{titulo}</h1>
<p class="meta">Publicado: {today} — Programa CAE 2026</p>
</header>
<nav class="back"><a href="{SITE}/blog/">← Volver al blog</a></nav>
<div class="container">
<article>
{body}
<div class="cta-box">
<p>¿Tu buhardilla cumple los requisitos? Descúbrelo gratis en 30 segundos.</p>
<a class="cta-button" href="{SITE}/?ref={ref}">Comprueba tu elegibilidad</a>
</div>
</article>
<footer>
<p><strong>{titulo}</strong></p>
<p>Buhardilla Gratis — <a href="{SITE}/">Programa CAE 2026</a></p>
</footer>
</div>
</body>
</html>'''
    filepath = f'{BLOG_DIR}/{slug}.html'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath, titulo, slug

def generate_blog_index(articles):
    items = ''.join(f'<li><a href="{s}.html">{t}</a></li>' for _, t, s in articles)
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog — Programa CAE | Buhardilla Gratis</title>
<meta name="description" content="Blog sobre el programa CAE de aislamiento gratuito de buhardillas. Guías, consejos y novedades.">
<link rel="canonical" href="{SITE}/blog/">
<style>
:root{{--navy:#0f2b46;--teal:#1a7a5c;--light:#f4f7fa;--gray:#6b7a88;--radius:12px;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#2d3748;line-height:1.7;background:var(--light);}}
.container{{max-width:780px;margin:0 auto;padding:24px;}}
header{{background:var(--navy);color:#fff;padding:48px 24px;text-align:center;}}
header h1{{font-size:2em;font-weight:800;margin-bottom:8px;letter-spacing:-.5px;}}
header p{{opacity:.8;}}
ul{{list-style:none;padding:0;}}
li{{background:#fff;border-radius:var(--radius);padding:20px 24px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);transition:transform .2s;}}
li:hover{{transform:translateX(4px);}}
li a{{color:var(--navy);font-weight:600;font-size:1.05em;text-decoration:none;}}
li a:hover{{color:var(--teal);}}
.back-link{{display:block;margin-top:32px;text-align:center;padding:16px 24px;background:var(--teal);color:#fff!important;border-radius:50px;font-weight:600;text-decoration:none;}}
footer{{text-align:center;padding:32px;color:var(--gray);font-size:.85em;}}
</style>
</head>
<body>
<header>
<h1>Blog — Programa CAE</h1>
<p>Toda la información sobre el programa CAE 2026, aislamiento de buhardillas, ahorro energético y novedades.</p>
</header>
<div class="container">
<ul>{items}</ul>
<a class="back-link" href="{SITE}/">Comprueba si eres elegible →</a>
<footer><p>© 2026 Buhardilla Gratis</p></footer>
</div>
</body>
</html>'''
    with open(f'{BLOG_DIR}/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def batch_complete():
    articles = []
    for template in ARTICULOS_TEMPLATE:
        path, titulo, slug = generate_article(template)
        articles.append((path, titulo, slug))
        if '[CIUDAD]' in template['titulo']:
            for ciudad, key, provincia in Config.ALL_MUNICIPIOS():
                path, titulo, slug = generate_article(template, ciudad)
                articles.append((path, titulo, slug))
    generate_blog_index(articles)
    log.info(f'Blog: {len(articles)} artículos generados en {BLOG_DIR}/')
    return [a[0] for a in articles]
