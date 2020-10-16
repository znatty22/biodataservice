from rest_framework import serializers
from biodata.api import models as m

COMMON_FIELDS = ['kf_id', 'created', 'modified']


class StudySerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Study
        fields = COMMON_FIELDS + ['name', 'short_name', 'participants']
        read_only_fields = ['participants']


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Participant
        fields = COMMON_FIELDS + [
            'gender', 'race', 'ethnicity', 'study',
        ]
