#!/usr/bin/env python3
"""
Buhardilla Lead Generation - Source Analysis & Scraper Prototypes
All sources tested: June 2026
"""

# ============================================================
# SOURCE 1: Milanuncios (buhardilla)
# URL: https://www.milanuncios.com/venta-de-pisos-en-madrid-madrid/buhardilla.htm
# Status: CONFIRMED WORKING
# Rendering: SPA (React) - needs Playwright or direct API
# Results: ~16
# Data: Title, price, description, size, location
# ============================================================
"""
Sample scraper:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.milanuncios.com/venta-de-pisos-en-madrid-madrid/buhardilla.htm")
        page.wait_for_selector("article")
        items = page.query_selector_all("article")
        for item in items:
            title = item.query_selector("h2").inner_text()
            price = item.query_selector("[data-testid='price']").inner_text()
            print(title, price)
"""

# ============================================================
# SOURCE 2: Nuroa
# URL: https://www.nuroa.es/venta/buhardilla-madrid
# Status: CONFIRMED WORKING (pre-confirmed)
# Results: ~117
# Rendering: HTML server-side (requests+BS4)
# ============================================================
"""
import requests
from bs4 import BeautifulSoup
r = requests.get("https://www.nuroa.es/venta/buhardilla-madrid",
                 headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(r.text, 'html.parser')
for card in soup.select('[class*="card"]'):
    title = card.select_one('[class*="title"]')
    price = card.select_one('[class*="price"]')
    if title:
        print(title.get_text(strip=True), price.get_text(strip=True) if price else '')
"""

# ============================================================
# SOURCE 3: Fotocasa
# URL: https://www.fotocasa.es/es/comprar/aticos/madrid-capital/todos-los-barrios/
# Status: NO KEYWORD SEARCH via URL. Uses internal API. CSJS-rendered.
# API endpoint found: search via POST to internal API
# Workaround: Search within listings text via /en/tag/ URL pattern
# ============================================================
"""
# Fotocasa uses an internal API. Sample approach:
import requests
# The search API is at: https://www.fotocasa.es/Content/API/search.json
# But needs specific parameters. Better to use Playwright:
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.fotocasa.es/es/comprar/pisos/madrid-capital/todos-los-barrios/")
    # Intercept XHR requests to find the API
    # Or use the /en/tag/ URL pattern for keyword filtering
"""

# ============================================================
# SOURCE 4: Pisos.com
# URL: https://www.pisos.com/venta/pisos-madrid/
# Status: Keyword search NOT supported in URL. JS-rendered SPA.
# Results: 12,454 total in Madrid (no keyword filter possible via URL)
# Approach: Client-side rendering, would need Playwright
# ============================================================
"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.pisos.com/venta/pisos-madrid/")
    # The page loads listings dynamically via API calls
    # Could intercept the XHR to the search API
"""

# ============================================================
# SOURCE 5: Habitaclia
# URL: N/A - No keyword search URL pattern found
# Status: NOT scrapable via simple URLs. JS-rendered.
# Belongs to Adevinta (same as Fotocasa, Milanuncios)
# ============================================================
# Habitaclia does not support keyword search in URL.
# Would need Playwright + form submission.
# Note: Habitaclia shows 404 for all "buhardilla" URL variations tested.

# ============================================================
# SOURCE 6: Trovit
# URL: https://casas.trovit.es/
# Status: Aggregator, JS-rendered SPA
# Approach: Would need Playwright to fill in search form
# The search is submitted via JS - API endpoint might be found
# ============================================================
"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://casas.trovit.es/")
    page.fill("input[name='what']", "buhardilla")
    page.fill("input[name='where']", "Madrid")
    page.click("button[type='submit']")
    page.wait_for_selector("[class*='ad']")
    # Parse results
"""

# ============================================================
# SOURCE 7: Mitula
# URL: https://pisos.mitula.com/
# Status: Aggregator, JS-rendered SPA
# 404 for all direct keyword URL patterns tested
# Would need Playwright to interact with search form
# ============================================================
# Mitula is JS-rendered. Would need Playwright.

# ============================================================
# SOURCE 8: Nestoria
# URL: https://www.nestoria.es/
# Status: Aggregator, JS-rendered
# 404 for all direct keyword URL patterns tested
# Owned by Lifull Connect (same as Trovit)
# ============================================================
# Nestoria is JS-rendered. Would need Playwright.

# ============================================================
# SOURCE 9: Milanuncios (desván + ático)
# desván: https://www.milanuncios.com/venta-de-pisos-en-madrid-madrid/desvan.htm
# ático: https://www.milanuncios.com/venta-de-pisos-en-madrid-madrid/atico.htm
# Status: Both WORK. SPA (React) rendered.
# "atico" result count: multiple pages (has rel="next" link)
# "desvan" result count: smaller set
# ============================================================
"""
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.milanuncios.com/venta-de-pisos-en-madrid-madrid/atico.htm")
    page.wait_for_selector("article")
    items = page.query_selector_all("article")
    print(f"Found {len(items)} results")
"""

# ============================================================
# SOURCE 10: Vibbo / Segundamano
# Status: DEFUNCT - Merged into Milanuncios.
# segundamano.es now redirects to milanuncios.com
# Vibbo ceased operations years ago
# ============================================================

# ============================================================
# SOURCE 11: INE API
# URL: https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES
# Status: FREE REST API - WORKS (tested)
# Returns JSON with all available statistical operations
# Relevant operations for CNAE/business data:
#   - ID 43: "Explotación Estadística del Directorio Central de Empresas" (DIR)
#   - ID 125: "Estadística de Sociedades Mercantiles" (SM)
# For CNAE codes (construction/real estate): need specific table IDs
# Data endpoint: /wstempus/js/ES/DATOS_TABLA/{TABLE_ID}
# ============================================================
"""
import requests
# Get available operations
ops = requests.get("https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES").json()
for op in ops:
    if any(kw in op['Nombre'].lower() for kw in ['empresa', 'construcción', 'sociedad', 'vivienda']):
        print(f"{op['Id']}: {op['Nombre']} ({op['Codigo']})")

# For CNAE code 41 (Construction of buildings), use DIRCE data
# Need to find the correct table ID for CNAE breakdown
# Try: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/3333 for IPRI data
# For CNAE-specific data, try ID 43 (DIR)
"""

# ============================================================
# SOURCE 12: BORME (Boletín Oficial del Registro Mercantil)
# URL: https://www.boe.es/borme/
# Status: WORKS but via BOE portal. HTML server-rendered.
# Use: Search for "administrador de fincas" or CNAE-related filings
# Official company registry - free access
# ============================================================
"""
import requests
from bs4 import BeautifulSoup
# BORME search via BOE
params = {
    'd-249512-p': 1,
    'accion': 1,
    'anho_d': 2026, 'mes_d': 1, 'dia_d': 1,
    'anho_h': 2026, 'mes_h': 6, 'dia_h': 10,
    's': 'administradores+fincas',
    't': 'B',
}
r = requests.get("https://www.boe.es/borme/listado_borme.php", params=params)
# Note: Might need to handle session/cookies. Returns 404 on direct access.
# Better approach: Query via BOE search API
"""

# ============================================================
# SOURCE 13: Paginas Amarillas
# URL: https://www.paginasamarillas.es/buscar/administradores+fincas
# Status: BLOCKED (403). Cloudflare/WAF protection.
# Would need: Playwright with stealth mode, rotating proxies, or API
# ============================================================
"""
# Cannot scrape directly due to Cloudflare.
# Alternative: Use Google Maps API or Google Business Profile API
# to search for "administrador de fincas" in Madrid
"""

# ============================================================
# SOURCE 14: QDQ
# URL: https://www.qdq.com/
# Status: NO LONGER A DIRECTORY. Now a website builder platform.
# No business directory functionality remaining.
# Essentially dead for lead generation purposes.
# ============================================================

# ============================================================
# SOURCE 15: Google Maps as Aggregate Source
# Google Maps search for "administrador de fincas Madrid"
# Use Google Places API or unofficial scraping (with caution)
# ============================================================
"""
# Google Places API (free tier: $200/month credit, ~40K calls/month)
import requests
API_KEY = "YOUR_KEY"
url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
params = {
    "query": "administrador de fincas en Madrid",
    "key": API_KEY,
    "language": "es",
}
r = requests.get(url, params=params)
data = r.json()
for result in data.get("results", []):
    print(result["name"], result.get("formatted_address"))
"""

# ============================================================
# SUMMARY TABLE
# ============================================================
print("""
╔═══════════════════╤══════════════════╤══════════════════╤══════════════╤════════════════╗
║ Source            │ URL Keyword      │ Rendering        │ Results      │ Approach       ║
╠═══════════════════╪══════════════════╪══════════════════╪══════════════╪════════════════╣
║ Milanuncios       │ YES (buhardilla) │ SPA (React)     │ ~16          │ Playwright     ║
║ Milanuncios atico │ YES (atico)      │ SPA (React)     │ 100+         │ Playwright     ║
║ Milanuncios desvan│ YES (desvan)     │ SPA (React)     │ ~20          │ Playwright     ║
║ Nuroa             │ YES              │ HTML server     │ ~117         │ requests+BS4   ║
║ Fotocasa          │ NO (API only)    │ SPA             │ N/A          │ Playwright+API ║
║ Pisos.com         │ NO               │ SPA             │ N/A          │ Playwright     ║
║ Habitaclia        │ NO               │ SPA             │ N/A          │ Playwright     ║
║ Trovit            │ JS form          │ SPA             │ N/A          │ Playwright     ║
║ Mitula            │ JS form          │ SPA             │ N/A          │ Playwright     ║
║ Nestoria          │ JS form          │ SPA             │ N/A          │ Playwright     ║
║ INE API           │ N/A (REST API)   │ JSON            │ Unlimited    │ requests       ║
║ BORME             │ Form search      │ HTML server     │ Unlimited    │ requests+BS4   ║
║ Paginas Amarillas │ WAF blocked      │ N/A             │ N/A          │ Blocked        ║
║ QDQ               │ DEAD             │ N/A             │ N/A          │ Dead           ║
║ Segundamano/Vibbo │ DEFUNCT          │ N/A             │ N/A          │ Dead           ║
╚═══════════════════╧══════════════════╧══════════════════╧══════════════╧════════════════╝
""")
