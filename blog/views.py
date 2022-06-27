from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.utils import timezone
from .models import Article
from drfClass.permissions import IsAdminOrRegisteredMoreThanAWeekUserOrIsAuthenticatedReadOnly
from .serializers import ArticleSerializer

class BlogView(APIView):
    permission_classes = [IsAdminOrRegisteredMoreThanAWeekUserOrIsAuthenticatedReadOnly]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'article.html'

    def get(self, request):
        time = timezone.now()
        articles = Article.objects.filter(author=request.user, start_date__lt=time, end_date__gt=time).order_by('-create_date')
        article_serializer = ArticleSerializer(articles, many=True).data

        return Response({'articles': article_serializer}, status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data['author'] = request.user.id
        article_serializer = ArticleSerializer(data=request.data)

        if article_serializer.is_valid():
            article_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        
        return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
