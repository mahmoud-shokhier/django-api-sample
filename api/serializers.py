
from rest_framework import serializers
from django.conf import settings


# models

from api.models import TestModelApi

date_form = getattr(settings, "DATE_FORMAT", None)
datetime_form = getattr(settings, "DATETIME_FORMAT", None)
datetime_uts_form = getattr(settings, "DATETIME_UTC_FORMAT", None)

# serializers

date_form = getattr(settings, "DATE_FORMAT", None)
datetime_form = getattr(settings, "DATETIME_FORMAT", None)
datetime_uts_form = getattr(settings, "DATETIME_UTC_FORMAT", None)


class TestModelApiSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    value = serializers.CharField()
    state = serializers.CharField(max_length=16)
    created_at = serializers.DateTimeField(format=date_form)
    updated_at = serializers.DateTimeField(format=date_form)

    class Meta:
        model = TestModelApi
        fields = '__All__'
