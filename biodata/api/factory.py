import factory
import factory.fuzzy

from .models import PREFIX_DICT, Study, Participant
from .base import kf_id_generator

COUNTS = {
    Study: 10,
    Participant: 10,
}


class ParticipantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Participant

    kf_id = factory.LazyAttribute(
        lambda study_id:
        kf_id_generator(PREFIX_DICT['participant'])
    )
    gender = factory.fuzzy.FuzzyChoice(Participant.GENDER)
    race = factory.fuzzy.FuzzyChoice(Participant.RACE)
    ethnicity = factory.fuzzy.FuzzyChoice(Participant.ETHNICITY)


class StudyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Study

    kf_id = factory.LazyAttribute(
        lambda study_id:
        kf_id_generator(PREFIX_DICT['study'])
    )
    short_name = factory.Sequence(lambda n: f'Study-{n}')
    name = factory.Sequence(lambda n: f'Long Name for Study-{n}')
    participants = factory.RelatedFactoryList(
        ParticipantFactory,
        size=COUNTS[Study],
        factory_related_name='study'
    )
