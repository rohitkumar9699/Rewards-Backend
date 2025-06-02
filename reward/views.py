from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RewardOrders, RewardWallet
# from .serializers import RewardSerializer

class CreateRewardView(APIView):
    def post(self, request):
        data = request.data
        
        try:
            # Get or create the RewardWallet user
            wallet, created = RewardWallet.objects.get_or_create(
                wallet_username=data['username'],
                defaults={
                    'wallet_fullname': data['full_name'],
                    'wallet_communication_email': data['communication_email'],
                    'wallet_balance': 0  # default balance
                }
            )

            # Create RewardOrder
            RewardOrders.objects.create(
                order_by=wallet,
                product_name=data['product_name'],
                product_id=data['product_id'],
                final_amount=data['final_amount'],
                order_date=data['order_date'],
                status=data['status'],
                payment_status=data['payment_status'],
                category=data['category'],
                reward_rate=data.get('reward_rate', 0.1)
            )


            return Response({'message': 'Reward order created successfully.'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from .models import RewardWallet, RewardOrders

class CreateReedomView(APIView):
    def post(self, request):
        order_id = request.data.get('id')
        username = request.data.get('username')

        if not order_id or not username:
            return Response({"error": "Both 'id' and 'username' are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = RewardOrders.objects.get(id=order_id)
        except RewardOrders.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            wallet = RewardWallet.objects.get(wallet_username=username)
        except RewardWallet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        reward_rate = Decimal(order.reward_rate)
        amount = order.final_amount  # Already DecimalField
       
        reward = amount * reward_rate

        old_wallet_balance= wallet.wallet_balance
        new_wallet_balance= wallet.wallet_balance   + reward


        wallet.wallet_balance += reward
        wallet.save()

        return Response({
            "wallet_username": wallet.wallet_username,
            "old_wallet_balance" : old_wallet_balance,
            "reward_added": str(reward),
            "new_wallet_balance" : new_wallet_balance,
            "order_id": order_id,
        }, status=status.HTTP_200_OK)
