import pytest

from django.core.management import call_command
from django.test.client import Client

BASE_URL = 'http://testserver'


def make_url(endpoint):
    return f'{BASE_URL}/{endpoint.strip("/")}'


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('fake_data')


@pytest.fixture(scope='session')
def client():
    return Client(
        HTTP_CONTENT_TYPE='application/json',
    )


@pytest.fixture(scope='session')
def requests_client():
    from rest_framework.test import RequestsClient
    c = RequestsClient()
    #c.headers.update({'content_type': 'application/json'})
    return c


@pytest.fixture(scope='session')
def api_client():
    from rest_framework.test import APIClient
    return APIClient(
        HTTP_CONTENT_TYPE='application/json',
    )
