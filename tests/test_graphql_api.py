import pytest
from pprint import pprint
from biodata.api import models as m
from biodata.api.factory import COUNTS

from conftest import BASE_URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    'query,expected_count',
    [
        (
            """
            {
                allStudies {
                    kfId
                    shortName
                    name
                }
            }
            """,
            COUNTS[m.Study]
        ),
        (
            """
            {
                allParticipants {
                    kfId
                    gender
                    race
                }
            }
            """,
            COUNTS[m.Study] * COUNTS[m.Participant]
        ),
        (
            """
            {
                allBiospecimens {
                    kfId
                    analyteType
                }
            }
            """,
            COUNTS[m.Study] * COUNTS[m.Participant] * COUNTS[m.Biospecimen]
        ),
    ]
)
def test_query(client, query, expected_count):
    """
    Test GraphQL queries 
    """
    response = client.post(
        f'{BASE_URL}/graphql', data={'query': query.strip()},
        content_type='application/json'
    )
    pprint(response.json())
    assert response.status_code == 200
    data = response.json()['data']
    assert data
    for k, v in data.items():
        assert len(v) == expected_count


@pytest.mark.django_db
@pytest.mark.parametrize(
    'mutation,variables,model_cls',
    [
        (
            """
            mutation CreateStudyMutation($shortName: String!) {
                createStudyMutation(shortName: $shortName) {
                    study {
                        kfId
                    }
                }
            }
            """,
            {'shortName': 'Study Foobar'},
            m.Study,
        ),
        (
            """
            mutation CreateParticipantMutation($gender: String!, $study: String!) {
                createParticipantMutation(gender: $gender, study: $study) {
                    participant {
                        kfId
                    }
                }
            }
            """,
            {
                'gender': 'Female',
                'study': lambda: m.Study.objects.first().kf_id
            },
            m.Participant,
        ),
        (
            """
            mutation CreateBiospecimenMutation($at: String!, $pt: String!) {
                createBiospecimenMutation(analyteType: $at, participant: $pt) {
                    biospecimen {
                        kfId
                    }
                }
            }
            """,
            {
                'at': 'DNA',
                'pt': lambda: m.Participant.objects.first().kf_id
            },
            m.Biospecimen,
        ),
    ]
)
def test_mutation(client, mutation, variables, model_cls):
    """
    Test GraphQL mutations
    """
    before = model_cls.objects.count()
    for k, v in variables.items():
        if callable(v):
            variables[k] = v()
    response = client.post(
        "/graphql",
        data={
            "query": mutation,
            "variables": variables
        },
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json()['data']
    assert model_cls.objects.count() == before + 1
