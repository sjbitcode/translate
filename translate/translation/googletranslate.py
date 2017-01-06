from google.cloud import translate


class GoogleTranslate():
    def __init__(self):
        self.translate_client = translate.Client()

    def detect_language(self, text):
        '''
        Detect the language of a given text.
        Returns dict with input, confidence, and language.

        Ex.
        {
            'input': 'hola como estás',
            'confidence': 0.4317437708377838,
            'language': 'es'
        }
        '''
        return self.translate_client.detect_language(text)

    def translate_text(self, text, target_lang):
        '''
        Translates a given text to target language.
        Returns dict with translatedText, input, detectedSourceLanguage.

        Ex.
        {
            'translatedText': 'Hello how are you',
            'input': 'hola como estás',
            'detectedSourceLanguage': 'es'
        }
        '''
        return self.translate_client.translate(
            text,
            target_language=target_lang
        )

    def language_list(self, target_lang='en'):
        '''
        Returns all supported languages for API.

        Ex.
        [
            {'name': 'Afrikaans', 'language': 'af'},
            {'name': 'Albanian', 'language': 'sq'},
            {'name': 'Zulu', 'language': 'zu'}
        ]
        '''
        return self.translate_client.get_languages(target_language=target_lang)

    def language_supported(self, target_lang):
        '''
        Determines if given language is supported.
        '''
        language_list = self.language_list()

        return any(d['language'] == target_lang for d in language_list) 
