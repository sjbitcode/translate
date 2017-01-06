from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^translations/$',
        views.translation_list,
        name='translations'
    ),
]
