from dataclasses import field
from rest_framework import serializers
from .models import User, UserProfile
from blog.serializers import ArticleSerializer

class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = UserProfile
      fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
#    article_set = ArticleSerializer(many=True, read_only=True)
    userprofile = UserProfileSerializer(read_only=True)

    def create(self, validated_data):
        validated_data['is_active'] = True
        password = validated_data.pop('password')
        new_user = User(**validated_data)
        new_user.set_password(password)
        new_user.save()

        return validated_data

    class Meta:
        # serializer에 사용될 model, field지정
        model = User
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = "__all__"

        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True}, # default : False
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            'fullname': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이름을 입력해주세요.',
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            }