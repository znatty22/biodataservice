import graphene

from biodata.api import models as m
from biodata.api import objects as o


class CreateStudyMutation(graphene.Mutation):
    class Arguments:
        short_name = graphene.String(required=True)
        name = graphene.String(required=False)

    study = graphene.Field(o.StudyType)

    def mutate(self, info, short_name, name=None):
        study = m.Study(
            short_name=short_name, name=name
        )
        study.save()
        return CreateStudyMutation(study=study)


class CreateParticipantMutation(graphene.Mutation):
    class Arguments:
        study = graphene.String(required=True)
        gender = graphene.String(required=True)
        race = graphene.String(required=False)
        ethnicity = graphene.String(required=False)

    participant = graphene.Field(o.ParticipantType)

    def mutate(self, info, study, gender, race=None, ethnicity=None):
        participant = m.Participant(
            gender=gender, race=race, ethnicity=ethnicity, study_id=study
        )
        participant.save()
        return CreateParticipantMutation(participant=participant)


class CreateBiospecimenMutation(graphene.Mutation):
    class Arguments:
        participant = graphene.String(required=True)
        analyte_type = graphene.String(required=False)

    biospecimen = graphene.Field(o.BiospecimenType)

    def mutate(self, info, participant, analyte_type=None):
        biospecimen = m.Biospecimen(
            analyte_type=analyte_type, participant_id=participant
        )
        biospecimen.save()
        return CreateBiospecimenMutation(biospecimen=biospecimen)


class Mutation(graphene.ObjectType):
    create_participant_mutation = CreateParticipantMutation.Field()
    create_study_mutation = CreateStudyMutation.Field()
    create_biospecimen_mutation = CreateBiospecimenMutation.Field()
