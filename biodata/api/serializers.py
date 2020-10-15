from rest_framework import serializers
from biodata.api.models import Study

COMMON_FIELDS = ['kf_id', 'url', 'created', 'modified']


class StudySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Study
        fields = COMMON_FIELDS + ['name', 'short_name']
