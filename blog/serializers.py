from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
   comment_set = CommentSerializer(many=True)
   class Meta:
      model = Article
      fields = "__all__"
