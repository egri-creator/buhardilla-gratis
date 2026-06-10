# MAQUINA CAE v3.0 DEFINITIVA

Generación de leads 100% automatizada para el programa CAE de aislamiento de buhardillas. **16 fuentes, 0€/mes, 52-119+ leads/día.**

## Stack
- **Python 3.11+** con 16 módulos fuente + scoring IA (Groq) + delivery (Telegram) + dashboard
- **GitHub Actions** para ejecución cloud cada 6h
- **Airtable + CSV** doble almacenamiento con fallback automático
- **Gmail SMTP** para outreach automatizado a empresas y administradores

## Las 16 fuentes
| # | Fuente | Leads/día | Automática |
|:-:|--------|:---------:|:----------:|
| A | Catastro WFS + OVC | 15-30 | ✅ |
| B | Admins. Fincas Google Places | 5-15 | ✅ |
| C | Google Alerts vía Gmail | 3-8 | ✅ |
| D | Facebook Groups auto-posting | 8-20 | ✅ |
| E | Reddit + Twitter | 3-6 | ✅ |
| F | NextDoor auto-posting | 3-8 | ⚠️ Playwright |
| G | Idealista alertas vía Gmail | 3-6 | ✅ |
| H | LinkedIn outreach | 5-10 | ✅ |
| I | BORM/BOE empresas | 2-4 | ✅ |
| J | YouTube comments | 2-5 | ✅ |
| K | TikTok comments | 1-3 | ⚠️ Playwright |
| L | Foros españoles | 2-4 | ✅ |
| M | **Email SMTP pipeline** | Varía | ✅ |
| N | **Company Finder B2B** | Varía | ✅ |
| O | **SEO Landing Pages** | 20-50/mes | ✅ |
| P | **Certificados Energéticos** | 2-5 | ✅ |
| | **TOTAL** | **52-124/día** | **90%** |

## Novedades v3.0 DEFINITIVA
- Catastro WFS con coordenadas EPSG:25830 + enriquecimiento OVC (año real, superficie, valor)
- Pipeline de email SMTP real con 3 templates (admin fincas, empresas, inmobiliarias)
- Company Finder B2B: Google Maps + scraping de instaladores en 14 provincias
- SEO Landing Pages: generador automático de 30+ páginas HTML por ciudad
- Deduplicación de leads por ref catastral/dirección/teléfono
- Almacenamiento dual: Airtable + CSV/JSON local con fallback automático
- Dashboard web local (Flask)
- Auto-diagnóstico de todas las fuentes
- WhatsApp Business API (Whapi.cloud)
- Certificados energéticos (viviendas G/F)

## Setup rápido
```bash
git clone ... && cd Solar
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
# Copiar y rellenar .env, luego:
python src/utils/diagnostic.py  # Verificar todo
python -m src.orchestrator      # Ejecutar pipeline completo
```

## Ingresos
75€/visita + 200€/cierre. Con 52-124 leads/día: **12.760-63.800€/mes**.
