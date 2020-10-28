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


def biospecimen_id():
    return kf_id_generator(PREFIX_DICT['biospecimen'])


class Study(Base):
    """
    A research effort studying a particular rare disease 
    """
    kf_id = KFIDField(default=study_id)
    short_name = models.CharField(max_length=25)
    name = models.CharField(
        max_length=100, blank=True, null=True, default=NOT_REPORTED
    )


class Participant(Base):
    """
    A research subject participating in a research study
    """
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
    study = models.ForeignKey(
        Study, related_name='participants', on_delete=models.CASCADE
    )


class Biospecimen(Base):
    """
    A sample drawn from a research subject participating in a research study
    """
    ANALYTE = {'DNA', 'RNA', 'Other'}
    ANALYTE_CHOICES = [(c, c) for c in ANALYTE]
    kf_id = KFIDField(default=biospecimen_id)
    analyte_type = models.CharField(
        choices=ANALYTE_CHOICES,
        default=NOT_REPORTED,
        max_length=50,
    )
    participant = models.ForeignKey(
        Participant, related_name='biospecimens', on_delete=models.CASCADE)
