from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),

    url(
        r'^api/translations/$',
        views.TranslationEventList.as_view(),
        name='translations'
    ),

    url(
        r'^api/language/(?P<pk>\d+)$',
        views.LanguageDetail.as_view(),
        name='language-detail'
    ),

    url(
        r'^api/phrase/(?P<pk>\d+)/$',
        views.PhraseDetail.as_view(),
        name='phrase-detail'
    ),

    url(
        r'api/languages/$',
        views.LanguageList.as_view(),
        name='languages'
    ),

    url(
        r'api/translate/$',
        views.Translate.as_view(),
        name='translate'
    ),
]
