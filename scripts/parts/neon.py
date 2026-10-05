"""Tiny Neon client over the HTTP SQL endpoint (no driver needed). Reads DATABASE_URL from the
environment or .env.local."""
import json, os, re, urllib.request

def database_url():
    url = os.environ.get('DATABASE_URL')
    if not url and os.path.exists('.env.local'):
        for line in open('.env.local'):
            if line.startswith('DATABASE_URL='):
                url = line.split('=', 1)[1].strip()
    if not url:
        raise SystemExit('DATABASE_URL is not set (environment or .env.local)')
    return url

def sql(query, params=None, url=None):
    url = url or database_url()
    host = re.match(r'postgres(?:ql)?://[^@]+@([^/:?]+)', url).group(1)
    req = urllib.request.Request(
        f'https://{host}/sql',
        data=json.dumps({'query': query, 'params': params or []}).encode(),
        headers={'Neon-Connection-String': url, 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f'Neon {e.code}: {e.read().decode()[:500]}')
