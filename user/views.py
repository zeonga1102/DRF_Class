from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from user.serializers import UserSerializer

class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'signup.html'

    def get(self, request):
        # return render(request, 'signup.html')
        return Response({"message": "정상"}, status=status.HTTP_200_OK)
    
    # 회원가입
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
            
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        return Response({'message': 'put method'})
    
    def delete(self, request):
        return Response({'message': 'delete method'})

class UserApiView(APIView):
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)

    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({'message': '로그아웃 성공'})

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    # 유저 기본 정보 및 프로필 조회
    def get(self, request):
        user = request.user
        # serializer에 queryset을 인자로 줄 경우 many=True 옵션을 사용해야 한다.
        serialized_user_data = UserSerializer(user).data
        return Response(serialized_user_data, status=status.HTTP_200_OK)