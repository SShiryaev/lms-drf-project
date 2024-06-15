from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

router = DefaultRouter()

urlpatterns = [
    path('payment/', views.PaymentListAPIView.as_view(), name='payment-list'),
    path('registration/', views.UserCreateAPIView.as_view(), name='user-registration'),
    path('', views.UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user-retrieve'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', views.UserDestroyAPIView.as_view(), name='user-delete'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('subscription/', views.SubscriptionCreateAPIView.as_view(), name='subscription'),
] + router.urls
