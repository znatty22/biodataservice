from rest_framework import serializers
from biodata.api.models import Study


class StudySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Study
        fields = '__all__'
