from django.db import models


class Language(models.Model):
    '''
    A language represents
        - name of language
        - language code
    '''
    name = models.CharField(
        max_length=100,
        verbose_name='Language name',
        help_text='Name of the language'
    )

    code = models.CharField(
        max_length=10,
        verbose_name='Language code',
        help_text='The ISO639-1 language code'
    )

    def __str__(self):
        return self.name


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

    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='phrases',
        verbose_name='Phrase language',
        help_text='The phrase language'
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
        return '{} - {}'.format(self.text, self.language.name)

    @property
    def language_name(self):
        return self.language.name

    @property
    def language_code(self):
        return self.language.code


class TranslateEvent(models.Model):
    '''
    A translate event is the relation between
    an input text and a translated text.
    '''
    input_text = models.ForeignKey(
        Phrase,
        on_delete=models.PROTECT,
        related_name='inputted',
        verbose_name='Input text',
        help_text='Phrase input for translation'
    )

    translated_text = models.ForeignKey(
        Phrase,
        on_delete=models.PROTECT,
        related_name='translated',
        verbose_name='Translated text',
        help_text='Phrase translation'
    )

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(
            self.input_text.text, self.translated_text.text
        )
