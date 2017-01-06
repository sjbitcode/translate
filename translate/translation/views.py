from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TranslateEvent
from .serializers import TranslateEventSerializer


@api_view(['GET'])
def translation_list(request):
    translations = TranslateEvent.objects.all()
    serializer = TranslateEventSerializer(translations, many=True)
    return Response(serializer.data)
