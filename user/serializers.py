from dataclasses import field
from rest_framework import serializers
from .models import User, UserProfile
from blog.serializers import ArticleSerializer

class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserProfile
      fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
   userprofile = UserProfileSerializer()
   article_set = ArticleSerializer(many=True)
   class Meta:
      # serializer에 사용될 model, field지정
      model = User
      # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
      fields = ["username", "userprofile", "article_set"]