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
                reward_rate=data.get('reward_rate', 0.00)
            )

            return Response({'message': 'Reward order created successfully.'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
