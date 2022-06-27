from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.db.models.query_utils import Q
from django.utils import timezone
from drfClass.permissions import IsAdminOrRegisteredMoreThanThreeDaysUserOrIsAuthenticatedReadOnly
from .serializers import ProductSerializer
from .models import Product

# Create your views here.
class ProductView(APIView):
    permission_classes = [IsAdminOrRegisteredMoreThanThreeDaysUserOrIsAuthenticatedReadOnly]

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product.html'

    def get(self, request):
        time = timezone.now()
        if request.user.is_anonymous:
            query = Q(is_active=True) & Q(start_date__lt=time) & Q(end_date__gt=time)
        else:
            query = ( Q(is_active=True) & Q(start_date__lt=time) & Q(end_date__gt=time) ) | Q(author=request.user)
        products = Product.objects.filter(query)
        product_serializer = ProductSerializer(products, many=True).data
        
        return Response({'products': product_serializer}, status=status.HTTP_200_OK)


    def post(self, request):
        request.data['author'] = request.user.id
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)
        
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def put(self, request, obj_id):
        product = Product.objects.get(id=obj_id)

        product_serializer = ProductSerializer(product, data=request.data, partial=True)

        if product_serializer.is_valid():
            # validator를 통과했을 경우 데이터 저장
            product_serializer.save()
            return Response({"message": "정상"}, status=status.HTTP_200_OK)