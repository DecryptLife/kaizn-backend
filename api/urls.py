from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, CategoryViewSet, TagViewSet, register, login, logout
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'tags', TagViewSet )

urlpatterns = [
     path(r'register/', register, name='register'),

    path(r'login/', login, name='login'),
    # path(r'login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'logout/', logout, name="logout"),
    path('', include(router.urls)),
]