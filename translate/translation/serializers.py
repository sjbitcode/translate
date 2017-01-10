from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .googletranslate import GoogleTranslate
from .models import Language, Phrase, TranslateEvent


# class TranslateEventSerializer(serializers.HyperlinkedModelSerializer):
#     input_text = serializers.HyperlinkedRelatedField(
#         view_name='phrase-detail',
#         lookup_field='pk',
#         read_only=True
#     )

#     translated_text = serializers.HyperlinkedRelatedField(
#         view_name='phrase-detail',
#         lookup_field='pk',
#         read_only=True
#     )

#     class Meta:
#         model = TranslateEvent
#         fields = ('input_text', 'translated_text')

class TranslateEventSerializer(serializers.ModelSerializer):

    input_text = serializers.SerializerMethodField('get_input_phrase_info')
    translated_text = serializers.SerializerMethodField('get_translated_phrase_info')

    def get_input_phrase_info(self, translate_event):
        phrase = translate_event.input_text
        return {
            'text': phrase.text,
            'language_name': phrase.language_name,
            'language_code': phrase.language_code
        }

    def get_translated_phrase_info(self, translate_event):
        phrase = translate_event.translated_text
        return {
            'text': phrase.text,
            'language_name': phrase.language_name,
            'language_code': phrase.language_code
        }

    class Meta:
        model = TranslateEvent
        fields = ('id', 'input_text', 'translated_text')


class PhraseSerializer(serializers.HyperlinkedModelSerializer):
    # language = serializers.HyperlinkedRelatedField(
    #     view_name='language-detail',
    #     lookup_field='pk',
    #     read_only=True
    # )
    language_name = serializers.ReadOnlyField()
    language_code = serializers.ReadOnlyField()

    class Meta:
        model = Phrase
        # fields = ('text', 'language')
        fields = ('id', 'text', 'language_name', 'language_code')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name', 'code')


class InputSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=500, required=True)
    language = serializers.CharField(
        max_length=10,
        allow_blank=True,
        required=False
    )

    def validate_text(self, value):
        '''
        Check if text can be translated.
        1. Use googletranslate to detect language of given text.
        2. If language is found, ok. If not, raise exception.
        '''
        g = GoogleTranslate()
        language_code = g.detect_language(text=value).get('language')

        if not Language.objects.filter(code=language_code).exists():
            raise serializers.ValidationError('Unable to recognize text')
        return value

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
