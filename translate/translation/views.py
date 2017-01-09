import html

from django.shortcuts import render, render_to_response
from django.template import RequestContext

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .googletranslate import GoogleTranslate
from .models import Language, Phrase, TranslateEvent
from .serializers import (
    LanguageSerializer,
    PhraseSerializer,
    TranslateEventSerializer,
    InputSerializer
)


def errorHandler(request, template, status):
    response = render_to_response(template, context=RequestContext(request))
    response.status_code = status
    return response


def handler404(request):
    return errorHandler(request, "translation/404.html", 404)


def handler500(request):
    return errorHandler(request, 'translation/500.html', 500)


def index(request):
    return render(request, 'translation/index.html')


class TranslationEventList(generics.ListAPIView):
    '''
    Returns all TranslateEvent objects.
    '''
    queryset = TranslateEvent.objects.all()
    serializer_class = TranslateEventSerializer


class PhraseDetail(generics.RetrieveAPIView):
    '''
    Get Phrase detail.
    '''
    queryset = Phrase.objects.all()
    serializer_class = PhraseSerializer


class LanguageDetail(generics.RetrieveAPIView):
    '''
    Get Language detail.
    '''
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageList(APIView):
    '''
    Returns list of supported languages.
    '''
    def get(self, request, format=None):
        g = GoogleTranslate()
        language_list = g.language_list()

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
    serializer_class = InputSerializer

    def post(self, request, format=None):
        input_serializer = self.get_serializer_class()(data=request.data)

        if input_serializer.is_valid():
            g = GoogleTranslate()

            # Get data from serializer
            input_text = input_serializer.data.get('text')
            target_language = input_serializer.data.get('language') or 'en'

            # Translate text and create Phrase, TranslateEvent models.
            result = g.translate_text(input_text, target_language)

            # Unescape html characters, ex. change "&#39" to "'"
            for key, value in result.items():
                result[key] = html.unescape(value)

            # Get or create models to create a TranslateEvent object.
            l1 = Language.objects.get(
                    code=result.get('detectedSourceLanguage')
            )

            l2 = Language.objects.get(
                    code=target_language
            )

            p1, created = Phrase.objects.get_or_create(
                text=result.get('input'),
                language=l1
            )

            p2, created = Phrase.objects.get_or_create(
                text=result.get('translatedText'),
                language=l2
            )

            te, created = TranslateEvent.objects.get_or_create(
                input_text=p1,
                translated_text=p2,
            )

            return Response(
                TranslateEventSerializer(te).data,
                status=status.HTTP_200_OK
            )

        return Response(
            input_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
