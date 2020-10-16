import pytest
from pprint import pprint
from biodata.api.models import Study


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint,expected_count',
    [
        ('/studies/', 10),
    ]
)
def test_api_get(api_client, endpoint, expected_count):
    """
    Test API GET /<entity type> and GET /<entity type>/<kf_id>
    """
    response = api_client.get(endpoint)
    r = response.json()
    assert response.status_code == 200
    assert len(r) == expected_count
    kf_id = r[0]["kf_id"]
    endpoint = f'{endpoint}{kf_id}/'
    response = api_client.get(endpoint)
    assert response.status_code == 200
    r = response.json()
    assert r['kf_id'] == kf_id


@ pytest.mark.django_db
@ pytest.mark.parametrize(
    'endpoint,expected_count,update_fields',
    [
        ('/studies/', 10, {'short_name': 'foobaz'}),
    ]


)
def test_api_patch(api_client, endpoint, expected_count, update_fields):
    """
    Test API PATCH by getting all entities and updating something
    """
    response = api_client.get(endpoint)
    r = response.json()
    kf_id = r[0]["kf_id"]
    endpoint = f'{endpoint}{kf_id}/'
    response = api_client.patch(endpoint, update_fields)
    assert response.status_code == 200
    r = response.json()
    assert r['kf_id'] == kf_id
    for k, v in update_fields.items():
        assert r[k] == v


@ pytest.mark.django_db
@ pytest.mark.parametrize(
    'endpoint,update_fields',
    [
        ('/studies/', {'short_name': 'foobaz',
                       'name': 'Long foobaz'}),
    ]


)
def test_api_post(api_client, endpoint, update_fields):
    """
    Test API POST 
    """
    count_before = len(api_client.get(endpoint).json())
    response = api_client.post(endpoint, update_fields)
    assert response.status_code == 201
    r = response.json()
    for k, v in update_fields.items():
        assert r[k] == v
    count_after = len(api_client.get(endpoint).json())
    assert (count_before + 1) == count_after


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint',
    [
        ('/studies/'),
    ]
)
def test_api_delete(api_client, endpoint):
    """
    Test API DELETE
    """
    results = api_client.get(endpoint).json()
    count_before = len(results)
    kf_id = results[0]['kf_id']
    del_endpoint = f'{endpoint}{kf_id}/'
    response = api_client.delete(del_endpoint)
    assert response.status_code == 204
    count_after = len(api_client.get(endpoint).json())
    assert (count_before - 1) == count_after
