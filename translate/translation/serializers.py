from rest_framework import serializers

from .googletranslate import GoogleTranslate
from .models import Language, Phrase, TranslateEvent


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
    # language = serializers.HyperlinkedRelatedField(
    #     view_name='language-detail',
    #     lookup_field='pk',
    #     read_only=True
    # )
    language_name = serializers.ReadOnlyField()

    class Meta:
        model = Phrase
        # fields = ('text', 'language')
        fields = ('text', 'language_name')


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ('name', 'code')


class InputSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500, required=True)
    language = serializers.CharField(
        max_length=10,
        allow_blank=True,
        required=False
    )

    def validate_language(self, value):
        '''
        If language is supplied, check to see if it exists.
        Check if a valid.
        '''
        if value:
            # if value is a language name, return the language code
            if Language.objects.filter(name__iexact=value).exists():
                return Language.objects.get(name__iexact=value).code
            # if value is a language code, return the language code
            elif Language.objects.filter(code__iexact=value).exists():
                return value
            # else language doesn't exist, so raise exception
            else:
                raise serializers.ValidationError('Language not supported')
            return value
