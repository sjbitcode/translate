import json

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Language, Phrase, TranslateEvent
from .serializers import (
    LanguageSerializer,
    PhraseSerializer,
    InputSerializer,
    TranslateEventSerializer
)


class TranslationTest(APITestCase):
    def setUp(self):

        # Define headers
        self.post_headers = {
            'content-type': 'application/json',
            'accept': 'application/json'
        }

        self.get_headers = {
            'accept': 'application/json'
        }

    # Helper Functions #
    def get_language_english(self):
        return Language.objects.get(code='en')

    def get_language_spanish(self):
        return Language.objects.get(code='es')

    def get_language_italian(self):
        return Language.objects.get(code='it')

    def get_language_french(self):
        return Language.objects.get(code='fr')

    def create_phrase(self, **kwargs):
        phrase = Phrase.objects.create(
            text=kwargs.get('text'),
            language=kwargs.get('language')
        )
        return phrase
    # Helper Functions #

    def test_get_languages(self):
        '''
        Test the GET method on /api/languages endpoint.
        '''
        url = reverse('languages')

        response = self.client.get(url, **self.get_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_translations(self):
        '''
        Test the GET method on /api/translations endpoint.
        '''
        url = reverse('translations')

        response = self.client.get(url, **self.get_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_a_language(self):
        '''
        Test the GET method on /api/language/<pk>
        with valid and invalid pk.
        '''
        url = reverse('language-detail', kwargs={'pk': 10})

        response = self.client.get(url, **self.get_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get a language that does not exist.
        url = reverse('language-detail', kwargs={'pk': 1000})

        response = self.client.get(url, **self.get_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_phrase(self):
        '''
        Test the GET method on /api/phrase/<pk>
        with valid and invalid pk.
        '''
        # Create a phrase.
        language = self.get_language_english()

        phrase = self.create_phrase(text='Hello', language=language)

        url = reverse('phrase-detail', kwargs={'pk': phrase.pk})

        response = self.client.get(url, **self.get_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get a phrase that does not exist.
        url = reverse('phrase-detail', kwargs={'pk': 2})

        response = self.client.get(url, **self.get_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_translate_to_same_language(self):
        '''
        Test the POST method on /api/translate.
        Send valid POST data where language is 
        the same language as input text.
        '''
        url = reverse('translate')
        data = {
            'text': 'bonjour',
            'language': 'french'
        }

        response = self.client.post(url, data, **self.post_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Phrase.objects.count(), 1)
        self.assertEqual(TranslateEvent.objects.count(), 1)

        # Inspect response object.
        # Validate that detected language is same as translated language.
        response_object = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_object
            .get('input_text')
            .get('language_name'), 'French'
        )
        self.assertEqual(response_object
            .get('input_text')
            .get('language_code'), 'fr'
        )
        self.assertEqual(response_object
            .get('translated_text')
            .get('language_name'), 'French'
        )
        self.assertEqual(response_object
            .get('translated_text')
            .get('language_code'), 'fr'
        )

    def test_translate_valid_data_1(self):
        '''
        Test the POST method on /api/translate.
        Send valid POST data where language spelled out.
        '''
        url = reverse('translate')
        data = {
            'text': 'Hello how are you',
            'language': 'Spanish'
        }

        response = self.client.post(url, data, **self.post_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Phrase.objects.count(), 2)
        self.assertEqual(TranslateEvent.objects.count(), 1)

    def test_translate_valid_data_2(self):
        '''
        Test the POST method on /api/translate.
        Send valid POST data where language is code.
        '''
        url = reverse('translate')
        data = {
            'text': 'Hello how are you',
            'language': 'es'
        }

        response = self.client.post(url, data, **self.post_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Phrase.objects.count(), 2)
        self.assertEqual(TranslateEvent.objects.count(), 1)

    def test_translate_no_language(self):
        '''
        Test the POST method on /api/translate.
        Send no language in POST data
        Input should be translated to English by default.
        '''
        url = reverse('translate')
        data = {
            'text': 'la casa blanca',
            'language': ''
        }

        response = self.client.post(url, data, **self.post_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure response's translated text's
        # language is English.
        response_object = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_object
            .get('translated_text')
            .get('language_name'), 'English'
        )
        self.assertEqual(response_object
            .get('translated_text')
            .get('language_code'), 'en'
        )

    def test_translate_invalid_data(self):
        '''
        Test the POST method on /api/translate.
        Do not send any POST data.
        '''
        url = reverse('translate')
        data = {
            'text': '',
            'language': ''
        }

        response = self.client.post(url, data, **self.post_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
