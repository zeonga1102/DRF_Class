from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.BlogView.as_view()),
]
