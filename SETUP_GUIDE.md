# GUIA DE SETUP — Maquina CAE v3.0

Tiempo total estimado: 36h distribuidas en 2 semanas.

---

## SEMANA 1: Infraestructura basica

### Dia 1 (4h): Cuentas y configuracion

- [ ] **GitHub** (github.com) — Crear cuenta gratis. Fork de este repo.
- [ ] **Airtable** (airtable.com) — Crear workspace "CAE". Importar plantilla:
  - Tabla `Leads`: LeadID, Direccion, Ciudad, Provincia, CodigoPostal, AnoConstruccion, ValorCatastral, Superficie, Score, Fuente, Estado, Empresa, FechaCreacion, ZonaClimatica, URLReferencia, Telefono, Email, GPSLat, GPSLon, FotoURL, ContratoURL, ExpedienteCAE
  - Tabla `Empresas`: Nombre, Tier, Zonas, ChatID, Email, Estado, LeadsAceptados, LeadsRechazados, TotalFacturado
  - Tabla `Comisiones`: LeadID, Empresa, Concepto, Importe, Fecha, Estado

- [ ] **Telegram Bot** — Hablar con @BotFather en Telegram:
  ```
  /newbot
  Nombre: CAE Leads Bot
  Username: cae_leads_bot
  ```
  Guardar el token. Crear grupo con el bot dentro. Obtener chat_id del grupo.

- [ ] **Groq API** (console.groq.com) — Crear cuenta. API Key gratuita (1M tokens/dia).

- [ ] **Google Cloud Console** — Crear proyecto. Activar APIs:
  - YouTube Data API v3
  - Places API
  - Gmail API
  Crear API Key y descargar credentials para Gmail.

- [ ] **Reddit API** (reddit.com/prefs/apps) — Crear app "script". Guardar client_id y secret.

- [ ] **Twitter/X API** (developer.twitter.com) — Free tier. Bearer token.

- [ ] **Twilio** (twilio.com) — $15 credito inicial. Comprar numero españa (~$3/mes).

### Dia 2 (6h): Configuracion local

- [ ] Instalar Python 3.11+ en PC
- [ ] Clonar repo: `git clone ...`
- [ ] `cd Solar`
- [ ] `python -m venv venv`
- [ ] `venv\Scripts\activate`
- [ ] `pip install -r requirements.txt`
- [ ] Copiar config:
  ```
  copy src\config\config_template.py src\config\config.py
  ```
- [ ] Abrir `src\config\config.py` y rellenar TODAS las claves (no empiecen por "cambia")
- [ ] Test: `python -c "from src.config.config_template import Config; print(Config.validate())"` → debe dar lista vacia
- [ ] Probar Catastro WFS: `python -c "from src.sources.catastro_wfs import query_municipio; leads = query_municipio('Valladolid', 41.65, -4.72, 0.1); print(f'{len(leads)} parcelas')"`

### Dia 3 (6h): Fuentes A + B + C

- [ ] Catastro WFS funcionando para todas las 14 provincias
- [ ] Google Alerts: crear alertas en accounts.google.com. Configurar envio a Gmail.
- [ ] Gmail API: autenticar con OAuth:
  ```
  python -c "from src.sources.idealista_alerts import get_gmail_service; svc = get_gmail_service(); print('Gmail OK')"
  ```
- [ ] Probar pipeline parcial: `python -m src.orchestrator`

### Dia 4 (6h): Fuentes D + E + F + G

- [ ] Facebook: Crear pagina y obtener access_token. Probar post en grupo.
- [ ] Reddit: `python -c "from src.sources.reddit_monitor import monitor; leads = monitor(); print(f'{len(leads)} posts')"`
- [ ] Twitter: `python -c "from src.sources.twitter_monitor import search_tweets; leads = search_tweets(); print(f'{len(leads)} tweets')"`
- [ ] YouTube: `python -c "from src.sources.youtube_comments import batch_complete; leads = batch_complete(); print(f'{len(leads)} comments')"`
- [ ] Idealista: Configurar alertas en idealista.com. Esperar 24h a que lleguen emails.

### Dia 5 (6h): Scoring + Delivery + Testing

- [ ] Probar Groq scoring:
  ```python
  python -c "
  from src.scoring.scoring_engine import score_lead
  test = {'provincia': 'Madrid', 'ano_construccion': 1975, 'fuente': 'reddit', 'texto': 'Necesito aislar mi buhardilla ayuda'}
  print(score_lead(test))
  "
  ```
- [ ] Probar Telegram bot:
  ```python
  python -c "from src.delivery.telegram_bot import send_telegram; send_telegram('? Test CAE Bot OK')"
  ```
- [ ] Probar pipeline completo local: `python -m src.orchestrator`

### Dia 6-7 (4h): GitHub Actions

- [ ] Push repo a GitHub
- [ ] Agregar Secrets en GitHub: Settings → Secrets and variables → Actions:
  ```
  GROQ_API_KEY, GOOGLE_API_KEY, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET,
  TWITTER_BEARER_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
  AIRTABLE_API_KEY, AIRTABLE_BASE_ID
  ```
- [ ] Ejecutar manualmente `pipeline.yml` desde Actions tab
- [ ] Verificar que se ejecuta sin errores
- [ ] Verificar datos en Airtable

---

## SEMANA 2: Outreach a empresas + refinamiento

### Dia 8-10: Contactar empresas

- [ ] Usar `COMPANY_OUTREACH.md` para contactar Aisla Solar
- [ ] Preparar demo: 5 leads reales de prueba (gratis para la empresa)
- [ ] Oferta: "primeros 5 leads gratis, luego 75€/visita + 200€/cierre"
- [ ] Obtener feedback sobre calidad de leads
- [ ] Ajustar scoring basado en feedback

### Dia 11-14: Escalar

- [ ] Contactar empresa 2 y 3
- [ ] Activar fuentes opcionales (TikTok, NextDoor) con Playwright
- [ ] Refinar scoring con datos reales de conversion

---

## DIAGNOSTICO RAPIDO

### Todo funciona?
```bash
python -c "
from src.config.config_template import Config
m = Config.validate()
print(f'Keys pendientes: {m if m else \"NINGUNA - OK\"}')
"
```

### Ver logs
```bash
cat logs/cae_machine.log
```

### Ver datos
```bash
ls data/leads/
```

---

## ARQUITECTURA FINAL

```
GitHub Actions (cada 6h)
    │
    ├── Catastro WFS → 15-30 leads
    ├── Google Alerts → 3-8 leads
    ├── Reddit → 3-6 leads
    ├── Twitter → 2-4 leads
    ├── YouTube → 2-5 leads
    ├── Foros → 2-4 leads
    ├── Idealista → 3-6 leads
    ├── Facebook → 8-20 leads
    ├── Admins fincas → 5-15 leads
    └── LinkedIn → 5-10 leads
    │
    ▼
    Scoring Engine (reglas + Groq IA)
    │
    ▼
    Airtable DB
    │
    ▼
    Telegram Bot → Empresa (Tier 1/2/3)
    │
    ▼
    SMS verificacion (Twilio)
    GPS verificacion (foto)
    ▼
    Comision: 75€ visita + 200€ cierre
```

---

## NOTAS IMPORTANTES

1. **GitHub Actions** tiene 2.000 min/mes gratis. Suficiente para ejecutar el pipeline cada 6h (~120 ejecuciones/mes × ~15 min = 1.800 min). Si te pasas, reduce a cada 12h.

2. **Groq API** da 1M tokens/dia gratis. El scoring usa ~100 tokens por lead. Con 100 leads/dia = 10K tokens/dia. Estas sobrado.

3. **Twilio** $15 dura meses si solo envias SMS de verificacion a leads que reciben visita.

4. **Airtable** 1.000 records/base gratis. Con ~2.000 leads/mes necesitas el plan Pro (12$/mes) al mes 2. Alternativa: seguir con Google Sheets gratis.

5. **Playwright** (TikTok/NextDoor) requiere ejecucion local, no en GitHub Actions. Ejecuta en tu PC 1 vez/dia.
