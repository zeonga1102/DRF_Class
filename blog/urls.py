from django.urls import path
from . import views

urlpatterns = [
    path('title/', views.BlogView.as_view()),
]
