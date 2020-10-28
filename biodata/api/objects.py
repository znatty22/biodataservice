from graphene_django import DjangoObjectType

from biodata.api import models as m


class StudyType(DjangoObjectType):
    class Meta:
        model = m.Study
        fields = ("kf_id", "name", "short_name")


class ParticipantType(DjangoObjectType):
    class Meta:
        model = m.Participant
        fields = (
            "kf_id", "gender", "race", "ethnicity", "biospecimens", "study"
        )


class BiospecimenType(DjangoObjectType):
    class Meta:
        model = m.Biospecimen
        fields = (
            "kf_id", "analyte_type", "participant"
        )
