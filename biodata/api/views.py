from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from biodata.api import models as m
from biodata.api import serializers as s


class StudyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = m.Study.objects.all()
    serializer_class = s.StudySerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = m.Participant.objects.all()
    serializer_class = s.ParticipantSerializer


