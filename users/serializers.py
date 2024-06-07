from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        model = User
        fields = ('email', 'phone', 'town', 'avatar',)


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежей."""

    class Meta:
        model = Payment
        fields = ('user', 'date', 'course', 'lesson', 'amount', 'method',)
