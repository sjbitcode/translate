from rest_framework import serializers

from .models import TranslateEvent


class TranslateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslateEvent
        fields = ('input_text', 'translated_text')

        read_only_fields = ('id', 'input_text', 'translated_text')
