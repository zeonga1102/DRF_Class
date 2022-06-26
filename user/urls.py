from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='signup'),
    path('login/', views.UserApiView.as_view(), name='login'),
    path('logout/', views.UserApiView.as_view()),
    path('info/', views.UserInfoView.as_view(), name='user_info'),
    path('', views.IndexView.as_view(), name='index')
]
