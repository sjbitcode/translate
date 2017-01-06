from rest_framework import serializers

from .googletranslate import GoogleTranslate
from .models import Phrase, TranslateEvent


class TranslateEventSerializer(serializers.HyperlinkedModelSerializer):
    input_text = serializers.HyperlinkedRelatedField(
        view_name='phrase-detail',
        lookup_field='pk',
        read_only=True
    )

    translated_text = serializers.HyperlinkedRelatedField(
        view_name='phrase-detail',
        lookup_field='pk',
        read_only=True
    )

    class Meta:
        model = TranslateEvent
        fields = ('input_text', 'translated_text')


class PhraseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Phrase
        fields = ('text', 'language_code')


class InputSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500, required=True)
    language = serializers.CharField(
        max_length=10,
        allow_blank=True,
        required=False
    )

    def validate_language(self, value):
        if value:
            g = GoogleTranslate()
            if not g.language_supported(value):
                raise serializers.ValidationError('Language not supported')
        return value
