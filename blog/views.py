from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from .models import Article, Category
from drfClass.permissions import IsAdminOrRegisteredMoreThanAWeekUserOrIsAuthenticatedReadOnly

# Create your views here.
class BlogView(APIView):
    permission_classes = [IsAdminOrRegisteredMoreThanAWeekUserOrIsAuthenticatedReadOnly]

    def get(self, request):
        time = timezone.now()
        articles = Article.objects.filter(author=request.user, start_date__lt=time, end_date__gt=time).order_by('-create_date')
        print(articles)
        titles = [ article.title for article in articles ]
        return Response({'titles': titles})
    
    def post(self, request):
        author = request.user
        title = request.data.get('title', '')
        category_name = request.data.get('category_name', '')
        content = request.data.get('content', '')

        if len(title) <= 5:
            return Response({'message': '제목은 5글자를 넘아야 합니다.'})
        
        if len(content) <= 20:
            return Response({'message': '내용은 20글자를 넘어야 합니다.'})
        
        if category_name:
            category = [ Category.objects.get(name=name) for name in category_name.split(',') ]
        else:
            return Response({'message': '카테고리를 지정해야 합니다.'})

        new_article = Article.objects.create(author=author, title=title, content=content)
        new_article.category.set(category)

        return Response({'message': '업로드 성공!'})
