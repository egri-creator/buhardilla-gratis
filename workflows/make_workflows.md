# Workflows Make.com para Maquina CAE v3.0

Make.com es el complemento visual a GitHub Actions.
Se usa para workflows que requieren interaccion humana o login en servicios web.

---

## Workflow 1: Facebook Auto-Poster

**Trigger:** Schedule, cada 12h
**Accion:**
1. HTTP Request → Facebook Graph API → POST /{group_id}/feed
2. 20 grupos configurados (uno por ciudad/zona)
3. Router: mensaje aleatorio de pool de 5 variantes
4. Response → log en Google Sheets

**Variables:**
- `access_token`: Token de pagina de Facebook (renovar cada 60 dias)
- `grupos`: Array de IDs de grupos

---

## Workflow 2: Telegram Bot — Gestion de leads

**Trigger:** Webhook de Telegram
**Accion:**
1. Recibe mensaje de empresa:
   - `/aceptar_LEAD-XXX` → Actualiza Airtable: Estado=ASIGNADO
   - `/rechazar_LEAD-XXX` → Actualiza Airtable: Estado=RECHAZADO
   - `/visita_LEAD-XXX` → Envia link de verificacion GPS
   - `/cerrar_LEAD-XXX` → Solicita numero expediente CAE
2. Envia confirmacion a la empresa
3. Notifica al admin via Telegram privado

---

## Workflow 3: Envio de Admin Toolkit

**Trigger:** Schedule, cada 7 dias
**Accion:**
1. Obtener lista de administradores de fincas (desde Airtable o Google Sheets)
2. Para cada admin:
   - Generar link unico de tracking: `https://leads.aisla-solar.es/?ref=admin-{ID}`
   - Enviar email con toolkit:
     - Explicacion CAE en 1 parrafo
     - Mensaje pre-escrito para reenviar a grupos de WhatsApp
     - Su link unico
3. Log de envio en Airtable

---

## Workflow 4: Alertas Google — Procesamiento

**Trigger:** Webhook de Gmail (nuevo email de Google Alerts)
**Accion:**
1. Leer email via Gmail API
2. Extraer URL del resultado
3. Scrapear contenido de la URL
4. Evaluar relevancia (Groq API: "? este texto habla de alguien que necesita aislamiento?")
5. Si score > 0.7 → crear lead en Airtable
6. Notificar via Telegram

---

## Para implementar en Make.com:

1. Crear cuenta en make.com (gratis)
2. Crear nuevo Scenario
3. Anadir modulo HTTP para llamadas API
4. Anadir modulo Airtable para DB
5. Anadir modulo Telegram para notificaciones
6. Configurar Schedule

**Limite free tier:** 1.000 operaciones/mes.
- Facebook poster: 2 ops × 30 ejecuciones = 60 ops
- Admin toolkit: 50 ops × 4 ejecuciones = 200 ops
- Google Alerts: 20 ops × 30 ejecuciones = 600 ops
- **Total: ~860 ops/mes** — dentro del free tier.
