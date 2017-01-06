from django.contrib import admin

from .models import Phrase, TranslateEvent

# Register your models here.
admin.site.register(Phrase)
admin.site.register(TranslateEvent)
