from rest_framework import serializers

from users.models import User, Payment, Subscription


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежей."""

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    payment = PaymentSerializer(source='payment_set', many=True, read_only=True)

    def get_payment(self, instance):
        return instance.payment_set.all()

    class Meta:
        model = User
        fields = ('email', 'phone', 'town', 'avatar', 'payment',)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписки"""

    class Meta:
        model = Subscription
        fields = '__all__'

