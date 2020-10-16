from django.db import models
from .base import KFIDField, kf_id_generator, Base, NOT_REPORTED

PREFIX_DICT = {
    'study': 'SD',
    'participant': 'PT',
    'biospecimen': 'BS'
}


def study_id():
    return kf_id_generator(PREFIX_DICT['study'])


def participant_id():
    return kf_id_generator(PREFIX_DICT['participant'])


class Study(Base):
    kf_id = KFIDField(default=study_id)
    short_name = models.CharField(max_length=25)
    name = models.CharField(
        max_length=100, blank=True, default=NOT_REPORTED
    )

    def __str__(self):
        return self.kf_id


class Participant(Base):
    GENDER = {'Male', 'Female', 'Other'}
    ETHNICITY = {'Hispanic or Latino',
                 'Not Hispanic or Latino'}
    RACE = {
        'White', 'American Indian or Alaska Native',
        'Black or African American', 'Asian',
        'Native Hawaiian or Other Pacific Islander',
        'Other', 'More Than One Race'
    }
    GENDER_CHOICES = [(c, c) for c in GENDER]
    RACE_CHOICES = [(c, c) for c in RACE]
    ETHNICITY_CHOICES = [(c, c) for c in ETHNICITY]

    kf_id = KFIDField(default=participant_id)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=NOT_REPORTED,
        max_length=50,
    )
    race = models.CharField(
        choices=RACE_CHOICES,
        default=NOT_REPORTED,
        max_length=50,
        null=True
    )
    ethnicity = models.CharField(
        choices=ETHNICITY_CHOICES,
        default=NOT_REPORTED,
        max_length=50,
        null=True
    )
    study = models.ForeignKey(Study, related_name='participants', on_delete=models.CASCADE)
