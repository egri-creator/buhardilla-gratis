"""Nuroa scraper — busca anuncios con buhardilla/atico/desvan.
Agrega Fotocasa, pisos.com, habitaclia, etc. Gratis, HTML publico.
Las listings se extraen del JSON-LD SearchResultsPage + HTML.
"""
import requests, re, time, json
from datetime import datetime
from src.config.config_template import Config
from src.utils.helpers import setup_logging, generate_lead_id

log = setup_logging(__name__)

BASE_URL = 'https://www.nuroa.es'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
]
_ua_idx = 0
_session = None

def _get_session():
    global _session, _ua_idx
    if _session is None:
        _session = requests.Session()
    _session.headers.update({
        'User-Agent': USER_AGENTS[_ua_idx % len(USER_AGENTS)],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': 'https://www.google.com/',
    })
    _ua_idx += 1
    return _session

KEYWORDS = ['buhardilla', 'atico']
MAX_PAGES = 1

def slugify(s):
    t = s.lower().strip()
    t = re.sub(r'[^\w\s-]', '', t)
    t = re.sub(r'[-\s]+', '-', t)
    return t.strip('-')

def extract_listing_data(html):
    """Extract listing data from Nuroa HTML page.
    Returns list of dicts with: title, price, address, source, description, url, beds.
    """
    leads = []
    seen_ids = set()

    # Method 1: Extract from JSON-LD (cleanest if available)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL):
        try:
            data = json.loads(m.group(1))
            if isinstance(data, dict) and data.get('@type') == 'SearchResultsPage':
                items = data.get('mainEntity', {}).get('itemListElement', [])
                for item in items:
                    it = item.get('item', {})
                    lid = item.get('@id', '') or item.get('position', '')
                    if lid and lid in seen_ids:
                        continue
                    seen_ids.add(lid)
                    offers = it.get('offers', {})
                    if isinstance(offers, list):
                        offers = offers[0] if offers else {}
                    price = offers.get('price', '') if isinstance(offers, dict) else ''
                    addr = it.get('address', {})
                    leads.append({
                        'id': str(lid),
                        'titulo': '',
                        'descripcion': it.get('description', ''),
                        'precio': str(price),
                        'url': '',
                        'ciudad': addr.get('addressLocality', ''),
                        'provincia': addr.get('addressRegion', ''),
                        'fuente': 'nuroa',
                        'palabra_clave': '',
                        'score': 0,
                        'fecha': datetime.now().isoformat(),
                    })
            if leads:
                return leads
        except (json.JSONDecodeError, TypeError):
            continue

    # Method 2: Parse HTML blocks
    ids = [m.group(1) for m in re.finditer(r'id="(nu_flat_\d+)"', html)]
    for bid in ids:
        if bid in seen_ids:
            continue
        seen_ids.add(bid)
        idx = html.index(bid)
        start = html.rindex('<div class="group', 0, idx)
        block = html[start:start+20000]

        # Price
        price_m = re.search(r'itemprop="price" content="(\d+)"', block)
        price = price_m.group(1) if price_m else ''

        # Address
        addr_m = re.search(r'class="nu_address_text">(.*?)</div>', block)
        addr = addr_m.group(1).strip() if addr_m else ''

        # Title from h3
        title_m = re.search(r'itemprop="url"[^>]*>(.*?)</a>', block)
        title = ''
        if title_m:
            title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip()
        if not title:
            title_m = re.search(r'<h3[^>]*itemprop="name"[^>]*>(.*?)</h3>', block, re.DOTALL)
            if title_m:
                title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip()

        # Source portal
        source = 'fotocasa' if 'Fotocasa' in block else 'idealista' if 'Idealista' in block else 'nuroa'

        # Description from block
        desc_m = re.search(r'<p[^>]*>(.*?)</p>', block)
        desc = desc_m.group(1).strip() if desc_m else ''

        leads.append({
            'id': generate_lead_id(addr[:3].upper(), 'NUR'),
            'titulo': title,
            'descripcion': desc[:500],
            'precio': price,
            'url': f'https://www.nuroa.es/property/{bid.replace("nu_flat_","")}',
            'ciudad': addr,
            'provincia': '',
            'fuente': f'nuroa-{source}',
            'palabra_clave': '',
            'score': 0,
            'fecha': datetime.now().isoformat(),
        })
    return leads

def search_city(keyword, city_name):
    """Search Nuroa for properties matching keyword in a city."""
    slug = slugify(city_name)
    all_leads = []
    seen_urls = set()

    for page in range(1, MAX_PAGES + 1):
        url = f'{BASE_URL}/venta/{keyword}-{slug}'
        if page > 1:
            url += f'?page={page}'
        try:
            sess = _get_session()
            r = sess.get(url, timeout=20)
            if r.status_code != 200:
                break
        except Exception as e:
            log.warning(f'Nuroa {city_name}/{keyword} page {page}: {e}')
            break

        leads = extract_listing_data(r.text)
        for l in leads:
            if l['url'] not in seen_urls:
                seen_urls.add(l['url'])
                l['palabra_clave'] = keyword
                l['ciudad'] = city_name
                all_leads.append(l)

        if not leads:
            break
        time.sleep(1.5)

    log.info(f'Nuroa {keyword}/{city_name}: {len(all_leads)}')
    return all_leads

def batch_complete():
    total = []
    seen = set()
    # Skip 'desvan' - returns 0 everywhere, wastes time
    active_kws = [kw for kw in KEYWORDS if kw != 'desvan']
    saved = 0
    for ciudad, key, provincia in Config.ALL_MUNICIPIOS():
        for kw in active_kws:
            leads = search_city(kw, ciudad)
            for l in leads:
                if l['url'] not in seen:
                    seen.add(l['url'])
                    total.append(l)
        # Save progressively
        if len(total) > saved + 50:
            saved = len(total)
            from src.utils.helpers import save_json
            save_json('data/leads/nuroa_partial.json', total)
    log.info(f'Nuroa total: {len(total)} anuncios unicos')
    return total
