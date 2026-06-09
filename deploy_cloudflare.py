"""Deploy a Cloudflare Pages via API.
Sube landing_pages/ + dashboard/ + blog/.
"""
import os, json, requests, hashlib

TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN', '')
ACCOUNT = 'd6f81a9fb5eda35fc21e15f398cd47e3'
PROJECT = 'buhardilla-gratis'

def get_headers():
    return {'Authorization': 'Bearer ' + TOKEN}

# 1. Create project
r = requests.get(f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/pages/projects/{PROJECT}', headers=get_headers())
if r.status_code == 404:
    print('Creando proyecto...')
    r = requests.post(f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/pages/projects', headers=get_headers(), json={
        'name': PROJECT, 'production_branch': 'main',
    })
    print('Proyecto:', 'OK' if r.status_code in (200, 201) else 'FAIL')
    if r.status_code not in (200, 201):
        print(r.text[:500])
        exit()
else:
    print('Proyecto existe')

# 2. Collect files
files = {}
for base_dir in ['landing_pages', 'dashboard', 'blog']:
    if not os.path.exists(base_dir):
        continue
    for root, _, fnames in os.walk(base_dir):
        for f in fnames:
            if not f.endswith(('.html', '.xml', '.css', '.js', '.png', '.jpg', '.svg', '.ico', '.txt')):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base_dir).replace('\\', '/')
            upload_path = f'{base_dir}/{rel}'
            with open(full, 'rb') as fh:
                files[upload_path] = fh.read()

print(f'Archivos: {len(files)}')

# 3. Build manifest
manifest = {}
for path, content in files.items():
    manifest[path] = hashlib.sha256(content).hexdigest()

# 4. Upload via Direct Upload API
import http.client, json, io

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = io.BytesIO()

def add_field(name, value, filename=None):
    body.write(b'--' + boundary.encode() + b'\r\n')
    if filename:
        body.write(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode())
        body.write(b'Content-Type: application/octet-stream\r\n')
    else:
        body.write(f'Content-Disposition: form-data; name="{name}"\r\n'.encode())
        body.write(b'Content-Type: application/json\r\n')
    body.write(b'\r\n')
    if isinstance(value, str):
        body.write(value.encode())
    else:
        body.write(value)
    body.write(b'\r\n')

# Add manifest
add_field('manifest', json.dumps(manifest))
# Add branch for production deployment
add_field('branch', 'main')

# Add files
for path, content in files.items():
    add_field(path, content, filename=path)

body.write(b'--' + boundary.encode() + b'--\r\n')

# Make request
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/pages/projects/{PROJECT}/deployments'
headers = get_headers()
headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'

r = requests.post(url, headers=headers, data=body.getvalue())

print(f'Status: {r.status_code}')
result = r.json()
if r.status_code in (200, 201) and result.get('success'):
    deploy_url = result['result']['url']
    print(f'URL: {deploy_url}')
    print(f'\nLanding page Madrid: {deploy_url}/landing_pages/aislamiento-buhardilla-perdida-gratis-madrid.html')
    print(f'Dashboard: {deploy_url}/dashboard/')
    print(f'Gracias: {deploy_url}/landing_pages/gracias.html')
    print(f'Blog: {deploy_url}/blog/')
else:
    print('Error:', result.get('errors', result.get('messages', '')))
