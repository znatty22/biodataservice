from django.db import models
from .base import KFIDField, Base, NOT_REPORTED



def study_id():
    return kf_id_generator('SD')


class Study(Base):
    kf_id = KFIDField(default=study_id)
    short_name = models.CharField(max_length=25)
    name = models.CharField(
        max_length=100, blank=True, default=NOT_REPORTED
    )

    def __str__(self):
        return self.kf_id
