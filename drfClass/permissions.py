from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status
from datetime import timedelta
from django.utils import timezone


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


class RegistedMoreThanTreeDaysUser(BasePermission):
    """
    가입일 기준 3일 이상 지난 사용자만 접근 가능
    """
    message = '가입 후 3일 이상 지난 사용자만 사용하실 수 있습니다.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.join_date < (timezone.now() - timedelta(days=3)))


class IsAdminOrRegisteredMoreThanAWeekUserOrIsAuthenticatedReadOnly(BasePermission):

    message = '가입 후 7일 이상 지난 사용자만 글을 작성할 수 있습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.is_authenticated and user.is_admin:
                return True

        is_more_than_a_week_user = bool(request.user and request.user.join_date < (timezone.now() - timedelta(days=7)))

        if request.method == 'GET':
            if user.is_authenticated:
                return True

        if request.method == 'POST':
            if user.is_authenticated and is_more_than_a_week_user:
                return True
            
            return False


class IsAdminOrRegisteredMoreThanThreeDaysUserOrIsAuthenticatedReadOnly(BasePermission):

    message = '가입 후 3일 이상 지난 사용자만 상품을 등록할 수 있습니다.'

    def has_permission(self, request, view):
        user = request.user
        
        if user.is_authenticated and user.is_admin:
            return True

        if request.method == 'GET':
            return True

        if request.method == 'POST':
            if not user.is_authenticated:
                response ={
                        "detail": "상품을 등록하려면 로그인 해주세요.",
                    }
                raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

            is_more_than_three_days_user = bool(request.user and request.user.join_date < (timezone.now() - timedelta(days=3)))

            if user.is_authenticated and is_more_than_three_days_user:
                return True
            
            return False