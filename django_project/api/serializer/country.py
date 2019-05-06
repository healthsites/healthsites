__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '03/05/19'

from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)
from localities.models import Country


class CountryAutoCompleteSerializer(ModelSerializer):
    label = SerializerMethodField()

    class Meta:
        model = Country
        fields = ['label', 'id']

    def get_label(self, instance):
        return instance.name
