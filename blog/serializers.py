from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      # all 보다는 구체적인 필드를 명시하는 것이 좋음
      fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
   comment_set = CommentSerializer(many=True)
   class Meta:
      model = Article
      fields = "__all__"
