"""
URLs for user authentication endpoints.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, RegisterView, UserViewSet, me_view

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', me_view, name='me'),
    path('', include(router.urls)),
]
