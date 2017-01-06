from django.db import models


class Phrase(models.Model):
    '''
    A phrase represents some text in a language
    and can have translations in other languages.
    '''
    text = models.TextField(
        max_length=500,
        verbose_name='Text field',
        help_text='The phrase text'
    )

    language_code = models.CharField(
        max_length=10,
        verbose_name='Language code',
        help_text='The ISO639-1 language code'
    )

    translation = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='TranslateEvent',
        related_name='translations',
        verbose_name='Phrase translation',
        help_text='The translation relations for this phrase'
    )

    def __str__(self):
        return '{} - {}'.format(self.text, self.language_code)


class TranslateEvent(models.Model):
    '''
    A translate event is the relation between
    an input text and a translated text.
    '''
    input_text = models.ForeignKey(
        Phrase,
        on_delete=models.SET_NULL,
        related_name='inputted',
        verbose_name='Input text',
        help_text='Phrase input for translation',
        null=True
    )

    translated_text = models.ForeignKey(
        Phrase,
        on_delete=models.SET_NULL,
        related_name='translated',
        verbose_name='Translated text',
        help_text='Phrase translation',
        null=True
    )

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(
            self.input_text.language_code, self.translated_text.language_code
        )
