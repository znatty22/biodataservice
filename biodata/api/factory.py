import factory

from .models import Study
from .base import kf_id_generator

COUNTS = {
    Study: 10,
}

class StudyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Study

    kf_id = factory.LazyAttribute(lambda study_id: kf_id_generator('SD'))
    short_name = factory.Sequence(lambda n: f'Study-{n}')
    name = factory.Sequence(lambda n: f'Long Name for Study-{n}')
