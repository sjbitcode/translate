from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^$',
        views.index,
        name='index'
    ),

    url(
        r'^translations/$',
        views.TranslationEventList.as_view(),
        name='translations'
    ),

    url(
        r'^phrase/(?P<pk>\d+)/$',
        views.PhraseDetail.as_view(),
        name='phrase-detail'
    ),

    url(
        r'languages/$',
        views.LanguageList.as_view(),
        name='languages'
    ),

    url(
        r'translate/$',
        views.Translate.as_view(),
        name='translate'
    ),
]
