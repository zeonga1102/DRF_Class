from django.forms import model_to_dict
from django.utils import timezone
from django.db.models import Avg
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
      # try-except 사용하는 것 별로 좋지 않음
      # [0]으로 인덱싱 하는 것보다 first() 사용하는게 좋음
      # 근데 first() 했을 때 오류가 발생하는지, 만약 생긴다면 어떤 오류일지는
      # 확인해봐야 함
      try:
         review = obj.review_set.all().order_by('-create_date')[0]
      except IndexError:
         return None
      return model_to_dict(review)

   def get_rating_avg(self, obj):
      review_list = obj.review_set.all()
      if review_list.count() == 0:
         return 0
      # 데이터가 적을 때는 상관없지만 많을 때는 이런 식으로 데이터를 전부 불러와서 계산하는 것이 비효율적임
      # aggregate 사용해볼 것. Sum, Avg, Count
      return review_list.aggregate(rating_avg=Avg('rating'))['rating_avg']
      # result = sum([review.rating for review in review_list]) / review_list.count()
      # return result


   def validate(self, data):
      # data.get('end_date')가 None인 경우는 보통 validation할 때 검증되긴 하는데
      # 현재 모델에 end_date 필드에 default가 적용되어 있어서 None이어도 검증이 통과됨
      # if ~ and 로 통째로 조건을 처리하지 말고 if문 두개로 분리해서
      # end_date가 None일 때는 날짜를 입력하라고 따로 처리해주는 것은 어떨까?
      # 그리고 data.get('end_date')가 중복되므로 변수를 하나 선언해주는 것이 좋음

      end_date = data.get('end_date')

      if not end_date:
         raise serializers.ValidationError(
                    # custom validation error message
                    detail={"error": "종료 일자를 입력하세요."},
                )

      if end_date < timezone.now().date():
         raise serializers.ValidationError(
                     # custom validation error message
                     detail={"error": "종료 일자는 과거일 수 없습니다."},
                  )

      # if data.get('end_date') and data.get('end_date') < timezone.now().date():
      #    raise serializers.ValidationError(
      #               # custom validation error message
      #               detail={"error": "종료 일자는 과거일 수 없습니다."},
      #           )
      return data

   def create(self, validated_data):
      # 굳이 pop하지 않고 validated_data['desc'] += f'문자열' 해도 됨
      validated_data['desc'] += f'\n{timezone.now().date()}에 등록된 상품입니다.'
      
      #desc = validated_data.pop('desc') + f'\n{timezone.now().date()}에 등록된 상품입니다.'
      #validated_data['desc'] = desc
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