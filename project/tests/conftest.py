import os

import pytest
import json
import requests
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from fastapi.security import SecurityScopes, HTTPBearer, HTTPAuthorizationCredentials

from app.config import Settings, get_settings
from app.main import create_application
from app.auth import auth
from fastapi_auth0 import Auth0User

# testing user password database:
testingUsers = {
    'test@test.de': '1ZxU&9^e2Oi@x9Fl'
}


def get_user_token(user_name):
    #  client id and secret come from LogIn (Test Client)! which has password enabled under "Client > Advanced > Grant Types > Tick Password"
    url = 'https://climbing-diary.eu.auth0.com/oauth/token'
    headers = {'content-type': 'application/json'}
    password = testingUsers[user_name]
    parameter = {"client_id": "FnK5PkMpjuoH5uJ64X70dlNBuBzPVynE",
                 "client_secret": "MSnQoFF28iCMZgKsfKiBdvOgErzA9cy3FKTUcfYuDkfpKJSlR4RN1pJuj5lQlsb6",
                 "audience": 'climbing-diary-API',
                 "grant_type": "password",
                 "username": user_name,
                 "password": password, "scope": "openid"}
    #  do the equivalent of a CURL request from https://auth0.com/docs/quickstart/backend/python/02-using#obtaining-an-access-token-for-testing
    responseDICT = json.loads(requests.post(url, json=parameter, headers=headers).text)
    return responseDICT['access_token']


def get_user_token_headers(user_name='test@test.de'):
    return {'authorization': "Bearer " + get_user_token(user_name)}


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        # testing
        yield test_client
    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        # testing
        yield test_client
    # tear down


@pytest.fixture(scope="module")
def headers():
    # setup
    headers = get_user_token_headers()
    yield headers
    #  teardown
