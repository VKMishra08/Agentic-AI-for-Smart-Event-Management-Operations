import os
from fastapi import Header, HTTPException, Request

AUTH_ENABLED = os.getenv('AUTH_ENABLED', 'false').lower() == 'true'
ADMIN_KEY = os.getenv('EVENTOPS_ADMIN_KEY', '')
VIEWER_KEY = os.getenv('EVENTOPS_VIEWER_KEY', '')
PUBLIC_PATHS = {'/', '/api/health', '/docs', '/openapi.json', '/redoc'}

def _key_role(key):
    if key and ADMIN_KEY and key == ADMIN_KEY:
        return 'admin'
    if key and VIEWER_KEY and key == VIEWER_KEY:
        return 'viewer'
    return None

def require_read(request: Request, x_api_key: str | None = Header(default=None)):
    if not AUTH_ENABLED or request.url.path in PUBLIC_PATHS:
        return 'demo'
    role = _key_role(x_api_key)
    if not role:
        raise HTTPException(401, 'Valid X-API-Key required')
    return role

def require_write(request: Request, x_api_key: str | None = Header(default=None)):
    if not AUTH_ENABLED:
        return 'demo'
    role = _key_role(x_api_key)
    if not role:
        raise HTTPException(401, 'Valid X-API-Key required')
    if role != 'admin':
        raise HTTPException(403, 'Admin API key required for write operations')
    return role
