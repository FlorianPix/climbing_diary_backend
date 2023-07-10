from fastapi_auth0 import Auth0

from app.config import get_settings

auth = Auth0(domain=get_settings().AUTH0_DOMAIN, api_audience=get_settings().AUTH0_API_AUDIENCE, scopes={
    'write:diary': 'write anything but media',
    'read:diary': 'read anything but media',
})
