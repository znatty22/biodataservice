from django.db import models
from django.utils import timezone

import random
import base32_crockford as b32

NOT_REPORTED = 'Not Reported'
REPORTED_UNKNOWN = 'Reported Unknown'
COMMON_ENUM = {NOT_REPORTED, REPORTED_UNKNOWN}


def kf_id_generator(prefix):
    """
    Returns a function to generator
    (Crockford)[http://www.crockford.com/wrmg/base32.html] base 32
    encoded number up to 8 characters left padded with 0 and prefixed with
    a two character value representing the entity type and delimited by
    an underscore

    Ex:
    'PT_0004PEDE'
    'SA_D167JSHP'
    'DM_ZZZZZZZZ'
    'ST_00000000'
    """
    assert len(prefix) == 2, 'Prefix must be two characters'
    prefix = prefix.upper()

    return '{0}_{1:0>8}'.format(
        prefix,
                                b32.encode(random.randint(0, 32**8-1))
    )


class KFIDField(models.CharField):
    description = 'A Kids First Identifier'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 11
        kwargs['unique'] = True
        kwargs['editable'] = False
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)


class Base(models.Model):
    created = models.DateTimeField(
        'created', default=timezone.now, null=True,
        editable=False
    )
    modified = models.DateTimeField(
        'modified', default=timezone.now, null=True,
        editable=False
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.kf_id

