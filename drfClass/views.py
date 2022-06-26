from django.shortcuts import redirect, render
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class IndexView(APIView):
    permission_classes = [permissions.AllowAny]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):
        return Response({"message": "정상"}, status=status.HTTP_200_OK)