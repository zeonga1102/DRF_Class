from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Article

# Create your views here.
class BlogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        titles = [ t['title'] for t in articles.values() ]
        return Response({'titles': titles})
