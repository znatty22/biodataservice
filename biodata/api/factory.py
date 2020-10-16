import factory
import factory.fuzzy

from biodata.api import models as m
from .base import kf_id_generator

COUNTS = {
    m.Study: 10,
    m.Participant: 3,
    m.Biospecimen: 2,
}


class BiospecimenFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = m.Biospecimen

    kf_id = factory.LazyAttribute(
        lambda study_id:
        kf_id_generator(m.PREFIX_DICT['biospecimen'])
    )
    analyte_type = factory.fuzzy.FuzzyChoice(m.Biospecimen.ANALYTE)


class ParticipantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = m.Participant

    kf_id = factory.LazyAttribute(
        lambda study_id:
        kf_id_generator(m.PREFIX_DICT['participant'])
    )
    gender = factory.fuzzy.FuzzyChoice(m.Participant.GENDER)
    race = factory.fuzzy.FuzzyChoice(m.Participant.RACE)
    ethnicity = factory.fuzzy.FuzzyChoice(m.Participant.ETHNICITY)
    biospecimens = factory.RelatedFactoryList(
        BiospecimenFactory,
        size=COUNTS[m.Biospecimen],
        factory_related_name='participant'
    )


class StudyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = m.Study

    kf_id = factory.LazyAttribute(
        lambda study_id:
        kf_id_generator(m.PREFIX_DICT['study'])
    )
    short_name = factory.Sequence(lambda n: f'm.Study-{n}')
    name = factory.Sequence(lambda n: f'Long Name for m.Study-{n}')
    participants = factory.RelatedFactoryList(
        ParticipantFactory,
        size=COUNTS[m.Participant],
        factory_related_name='study'
    )
