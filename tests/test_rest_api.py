import pytest
from pprint import pprint
from biodata.api import models as m
from biodata.api.factory import COUNTS


def get_kf_id(model_cls):
    return model_cls.objects.all().first().kf_id


@pytest.mark.django_db
@pytest.mark.parametrize(
    'endpoint,expected_count',
    [
        ('/studies/', COUNTS[m.Study]),
        ('/participants/', COUNTS[m.Study] * COUNTS[m.Participant]),
        ('/biospecimens/', (
            COUNTS[m.Study] * COUNTS[m.Participant] * COUNTS[m.Biospecimen]
        )),
    ]
)
def test_api_get(api_client, endpoint, expected_count):
    """
    Test API GET /<entity type> and GET /<entity type>/<kf_id>
    """
    response = api_client.get(endpoint)
    r = response.json()['results']
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
        ('/studies/', COUNTS[m.Study], {'short_name': 'foobaz'}),
        ('/participants/', COUNTS[m.Participant], {'gender': 'Female'}),
        ('/biospecimens/', COUNTS[m.Biospecimen], {'analyte_type': 'DNA'}),
    ]


)
def test_api_patch(api_client, endpoint, expected_count, update_fields):
    """
    Test API PATCH by getting all entities and updating something
    """
    response = api_client.get(endpoint)
    r = response.json()['results']
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
        ('/participants/', {
            'gender': 'Female',
            'race': 'Asian',
            'study': lambda: get_kf_id(m.Study)
        }),
        ('/biospecimens/', {
            'analyte_type': 'RNA',
            'participant': lambda: get_kf_id(m.Participant)
        }),
    ]
)
def test_api_post(api_client, endpoint, update_fields):
    """
    Test API POST
    """
    count_before = len(api_client.get(endpoint).json()['results'])
    for k, v in update_fields.items():
        if callable(v):
            update_fields[k] = v()
    response = api_client.post(endpoint, update_fields)
    pprint(response.request)
    assert response.status_code == 201
    r = response.json()
    for k, v in update_fields.items():
        assert r[k] == v
    count_after = len(api_client.get(endpoint).json()['results'])
    assert (count_before + 1) == count_after


@ pytest.mark.django_db
@ pytest.mark.parametrize(
    'endpoint',
    [
        ('/studies/'),
        ('/participants/'),
        ('/biospecimens/'),
    ]
)
def test_api_delete(api_client, endpoint):
    """
    Test API DELETE
    """
    results = api_client.get(endpoint).json()['results']
    count_before = len(results)
    kf_id = results[0]['kf_id']
    del_endpoint = f'{endpoint}{kf_id}/'
    response = api_client.delete(del_endpoint)
    assert response.status_code == 204
    count_after = len(api_client.get(endpoint).json()['results'])
    assert (count_before - 1) == count_after
