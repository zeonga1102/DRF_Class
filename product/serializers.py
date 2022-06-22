from django.forms import model_to_dict
from django.utils import timezone
import datetime
from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
   class Meta:
      model = Review
      fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
   recent_review = serializers.SerializerMethodField()
   rating_avg = serializers.SerializerMethodField()

   def get_recent_review(self, obj):
      try:
         review = obj.review_set.all().order_by('-create_date')[0]
      except IndexError:
         return None
      return model_to_dict(review)

   def get_rating_avg(self, obj):
      review_list = obj.review_set.all()
      if review_list.count() == 0:
         return 0
      result = sum([review.rating for review in review_list]) / review_list.count()
      return result


   def validate(self, data):
      if data.get('end_date') and data.get('end_date') < timezone.now().date():
         raise serializers.ValidationError(
                    # custom validation error message
                    detail={"error": "종료 일자는 과거일 수 없습니다."},
                )
      return data

   def create(self, validated_data):
      desc = validated_data.pop('desc') + f'\n{timezone.now().date()}에 등록된 상품입니다.'
      validated_data['desc'] = desc
      product = Product(**validated_data)
      product.save()

      return product

   def update(self, instance, validated_data):
      for key, value in validated_data.items():
         if key == 'desc':
            value = f'{timezone.now()}에 수정되었습니다.\n' + value
         setattr(instance, key, value)

      instance.save()

      return instance

   class Meta:
      model = Product
      fields = "__all__"