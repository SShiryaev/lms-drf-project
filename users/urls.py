from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('payment/', views.PaymentListAPIView.as_view(), name='payment-list'),
] + router.urls
