from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register("category", CategoryViewSet, basename="category" )
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    
]
urlpatterns += router.urls