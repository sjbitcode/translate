from django.contrib import admin

from .models import Phrase, TranslateEvent, Language

# Register your models here.
admin.site.register(Language)
admin.site.register(Phrase)
admin.site.register(TranslateEvent)
