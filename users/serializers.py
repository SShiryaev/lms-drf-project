from rest_framework import serializers

from users.models import User, Payment


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
