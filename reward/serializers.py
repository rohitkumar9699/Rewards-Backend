from rest_framework import serializers
from .models import *


class RewardSerializer(serializers.Serializer):
     class Meta:
        model = RewardCards
        fields = "__all__"
   

class RewardWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardWallet
        fields = "__all__"
