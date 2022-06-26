from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='product'),
    path('<obj_id>/', views.ProductView.as_view(), name='product_update'),
]
