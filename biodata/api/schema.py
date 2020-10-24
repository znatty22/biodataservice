import graphene
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


class Query(graphene.ObjectType):
    all_studies = graphene.List(StudyType)
    all_participants = graphene.List(
        ParticipantType, study_id=graphene.String(required=False)
    )
    all_biospecimens = graphene.List(
        BiospecimenType, study_id=graphene.String(required=False)
    )

    def resolve_all_studies(root, info):
        return m.Study.objects.all()

    def resolve_all_participants(root, info, study_id=None):
        objects = m.Participant.objects
        if study_id:
            objects = objects.filter(study=study_id)

        return (
            objects.select_related('study').all()
        )

    def resolve_all_biospecimens(root, info, study_id=None):
        objects = m.Biospecimen.objects
        if study_id:
            objects = objects.filter(study=study_id)

        return (
            objects.select_related('participant').all()
        )


schema = graphene.Schema(query=Query)
