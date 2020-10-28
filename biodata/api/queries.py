import graphene

from biodata.api import models as m
from biodata.api import objects as o


class Query(graphene.ObjectType):
    all_studies = graphene.List(o.StudyType)
    all_participants = graphene.List(
        o.ParticipantType, study_id=graphene.String(required=False)
    )
    all_biospecimens = graphene.List(
        o.BiospecimenType, study_id=graphene.String(required=False)
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
