from rest_framework import serializers
from .models import Article, Comment, Category

class CommentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Comment
      # all 보다는 구체적인 필드를 명시하는 것이 좋음
      fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
   comment_set = CommentSerializer(many=True, read_only=True)
   author_name = serializers.SerializerMethodField(read_only=True)
   category_name = serializers.SerializerMethodField(read_only=True)

   def get_category_name(self, obj):
      return [ category.name for category in obj.category.all() ]

   def get_author_name(self, obj):
      return obj.author.username


   def validate(self, data):
      if len(data.get('title')) <= 5:
        raise serializers.ValidationError(
                   # custom validation error message
                   detail={"error": "제목은 5글자를 넘아야 합니다."},
               )

      if len(data.get('content')) <= 20:
         raise serializers.ValidationError(
                  # custom validation error message
                  detail={"error": "내용은 20글자를 넘어야 합니다."},
               )
      if not data.get('category', None):
         raise serializers.ValidationError(
                  # custom validation error message
                  detail={"error": "카테고리를 지정해야 합니다."},
               )

      return data

   
   def create(self, validated_data):
      categories = validated_data.pop('category')
      
      article = Article(**validated_data)
      article.save()
      article.category.set(categories)
      
      return validated_data


   class Meta:
      model = Article
      fields = ['id', 'category', 'category_name', 'title', 'author', 'author_name', 'content', 'comment_set']
