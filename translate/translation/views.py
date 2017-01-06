from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from .googletranslate import GoogleTranslate
from .models import Phrase, TranslateEvent
from .serializers import (
    PhraseSerializer,
    TranslateEventSerializer,
    InputSerializer
)
from translate.paginators import CustomPagination


class TranslationEventList(generics.GenericAPIView):
    '''
    Returns all TranslateEvent objects.
    '''
    def get(self, request, format=None):
        translations = TranslateEvent.objects.all()
        translation_serializer = TranslateEventSerializer(
            translations,
            context={'request': request},
            many=True
        )
        return Response(
            translation_serializer.data,
            status=status.HTTP_200_OK
        )


class PhraseDetail(generics.GenericAPIView):
    '''
    Get Phrase detail.
    '''
    def get(self, request, pk):
        phrase = get_object_or_404(Phrase, pk=pk)
        phrase_serializer = PhraseSerializer(phrase)

        return Response(
            phrase_serializer.data,
            status=status.HTTP_200_OK
        )


class LanguageList(generics.GenericAPIView):
    '''
    Returns list of supported languages.
    '''
    pagination_class = CustomPagination

    def get(self, request, format=None):
        g = GoogleTranslate()
        language_list = g.language_list(target='en')

        page = self.paginate_queryset(language_list)
        if page is not None:
            return self.get_paginated_response(language_list)

        return Response(
            language_list,
            status=status.HTTP_200_OK
        )


class Translate(generics.GenericAPIView):
    '''
    Translates given text and returns
    input, source language, translated text,
    and language translated to.
    '''
    def post(self, request, format=None):
        input_serializer = InputSerializer(data=request.data)

        if input_serializer.is_valid():
            g = GoogleTranslate()

            # Get data from serializer
            input_text = input_serializer.data.get('text')
            target_language = input_serializer.data.get('language') or 'en'

            # Translate text and create Phrase, TranslateEvent models.
            result = g.translate_text(input_text, target_language)

            p1, created = Phrase.objects.get_or_create(
                text=result.get('input'),
                language_code=result.get('detectedSourceLanguage')
            )

            p2, created = Phrase.objects.get_or_create(
                text=result.get('translatedText'),
                language_code=target_language
            )

            te, created = TranslateEvent.objects.get_or_create(
                input_text=p1,
                translated_text=p2,
            )

            # Add target language to response.
            result['targetLanguage'] = target_language
            return Response(
                result,
                status=status.HTTP_200_OK
            )

        return Response(
            input_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
