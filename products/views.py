from rest_framework import generics, exceptions
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsSellerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class CategoryList(generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

category_list = CategoryList.as_view()

class CategoryDetail(generics.GenericAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

category_detail = CategoryDetail.as_view()

class ProductList(generics.GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

product_list = ProductList.as_view()

class ProductDetail(generics.GenericAPIView):
        serializer_class = ProductSerializer
        queryset = Product.objects.all()
        permission_classes = [IsAuthenticated]
    
        def get(self, request, pk):
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
    
        def put(self, request, pk):
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        def delete(self, request, pk):
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

product_detail = ProductDetail.as_view()

class ProductUpload(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly]
    def get(self, request, *args, **kwargs):
        return Response()
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(seller=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            raise exceptions.PermissionDenied("You are not a seller")

product_upload = ProductUpload.as_view()
# Create your views here.
