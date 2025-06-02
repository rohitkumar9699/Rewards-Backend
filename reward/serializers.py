from rest_framework import serializers

class RewardSerializer(serializers.Serializer):
    order_by = serializers.CharField(max_length=100)
    product_name = serializers.CharField(max_length=100)
    product_id = serializers.CharField(max_length=50)
    final_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    order_date = serializers.DateTimeField()
    status = serializers.CharField(max_length=50)
    payment_status = serializers.BooleanField(default=False)
    category = serializers.CharField(max_length=100)
    reward_rate = serializers.FloatField(default=0.00)


# serializers.py

from rest_framework import serializers
from .models import RewardWallet

class RewardWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardWallet
        fields = [
            'id',
            'wallet_username',
            'wallet_fullname',
            'wallet_communication_email',
            'wallet_balance',
        ]
