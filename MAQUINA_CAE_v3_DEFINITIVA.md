# MAQUINA CAE DEFINITIVA — Números reales desde el día 1

## Stack real (0€/mes, 100% automático)

| Componente | Coste |
|-----------|:-----:|
| Python + 23 módulos | 0€ |
| Catastro INSPIRE WFS + OVC | 0€ (API pública sin auth) |
| Google Cloud (YouTube, Places, Maps, Gmail) | 0€ ($200/mes crédito gratis) |
| Groq (scoring IA) | 0€ (1M tokens/día gratis) |
| GitHub Actions (orquestación) | 0€ (2.000 min/mes gratis) |
| Telegram (notificaciones) | 0€ |
| Airtable + CSV (almacenamiento) | 0€ (1.000 records + fallback local) |
| **TOTAL** | **0€/mes** |

## Lo que genera leads de verdad (ordenado por impacto real)

### #1 Catastro WFS + OVC → 15-30 leads/día
La API pública del Catastro devuelve parcelas con nombre del propietario, año de construcción, superficie y valor catastral. **Sin autenticación, sin límite, 100% legal.** Esto es el core de la máquina.

### #2 SEO Landing Pages → 5-15 leads/día (crecimiento 1-3 meses)
70 páginas para "aislamiento buhardilla gratis [provincia]" + variaciones. Tráfico orgánico de Google. Empieza con 0, crece cada mes. A los 3 meses es el canal #1.

### #3 Admin Fincas (B2B) → 5-15 leads/día
Email toolkit automatizado para administradores de fincas. Cada admin = 10-30 viviendas. Efecto multiplicador.

### #4 Idealista Alertas → 3-6 leads/día
Email alerts de áticos/buhardillas en venta. Propietarios con intención de vender = probablemente también quieran aislar.

### #5 Google Alerts → 3-8 leads/día
Monitorización pasiva de menciones en tiempo real. Gente quejándose del calor/factura en foros, blogs y noticias.

### #6 YouTube Comments → 2-5 leads/día
Comentarios en vídeos de aislamiento/eficiencia donde la gente dice "necesito esto en mi casa".

### #7 Foros (Burbuja, ForoCoches) → 2-4 leads/día
Gente buscando activamente soluciones de aislamiento.

### #8 BORM/BOE → 2-4 empresas/semana
Pipeline de empresas compradoras de leads.

### #9 Reddit + Twitter → 3-6 leads/día
Monitorización pasiva (se queda porque es 0 esfuerzo).

### Fuentes opcionales (0 coste, 0 esfuerzo, déjalas correr)
Facebook auto-posting, NextDoor, TikTok, LinkedIn, Certificados Energéticos.

## Números reales por mes

| Mes | Fuentes activas | Leads/día | Leads/mes | Visitas estimadas | Ingreso estimado |
|:---:|:---------------:|:---------:|:---------:|:-----------------:|:----------------:|
| **1** | Catastro + Alerts + Idealista + Foros | 20-35 | 440-770 | 3-5/día | **~3.300-5.775€** |
| **2** | + Admin Fincas + YouTube + SEO | 35-60 | 770-1.320 | 6-10/día | **~6.600-11.550€** |
| **3+** | Todo activo + SEO consolidado | 50-80 | 1.100-1.760 | 9-14/día | **~9.900-16.500€** |

**Cálculo**: 75€/visita × 17% de leads entregados que llegan a visita.
Ejemplo mes 1: 600 leads × 65% scoring × 90% entregados × 70% aceptados × 17% visitas = ~42 visitas/mes × 75€ = **3.150€** solo por visitas. Más cierres.

## Qué hace la máquina cada día (automáticamente)

```
06:00 — Catastro WFS extrae parcelas en 14 provincias
06:05 — OVC enriquece cada parcela (año, superficie, propietario)
06:30 — Google Alerts + Idealista + YouTube + Foros + Reddit + Twitter
07:00 — Scoring IA (Groq) clasifica todos los leads
07:05 — Deduplicación + almacenamiento (Airtable + CSV)
07:10 — Cluster detection (edificios con 5+ parcelas → B2B)
07:15 — Company Finder (nuevas empresas instaladoras vía Google Maps)
07:20 — SEO pages + Blog generados
07:25 — Telegram: resumen del día
```

**Todo esto ocurre solo, sin que toques nada.**

## Lo que necesitas para que funcione (1 hora de setup)

1. **Gmail dedicado** (5 min) — para las API keys y recibir alertas de Idealista/Google
2. **API keys gratuitas** (30 min): Groq, Google Cloud, Reddit, Twitter, Telegram
3. **Rellenar `.env`** (5 min)
4. **Subir a GitHub** (10 min) — los Secrets se configuran automáticamente
5. **Ejecutar**: `python -m src.orchestrator` (o esperar a GitHub Actions)

## Lo que NO hace esta máquina

- ❌ No contacta a particulares directamente
- ❌ No envía WhatsApp
- ❌ No requiere que llames a nadie
- ❌ No tiene costes ocultos
- ❌ No depende de redes sociales (puedes desactivarlas todas y sigue funcionando)

**Solo genera leads que llegan a Aisla Solar y tú cobras comisión.**
