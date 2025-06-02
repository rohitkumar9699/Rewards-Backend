from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import RewardWallet, RewardCards

class CreateCardView(APIView):
    def post(self, request):
        data = request.data

        try:
            # 1. Get or create the wallet user
            wallet, created = RewardWallet.objects.get_or_create(
                wallet_username=data['username'],
                defaults={
                    'wallet_fullname': data.get('full_name', ''),
                    'wallet_communication_email': data.get('communication_email', ''),
                    'wallet_balance': 0
                }
            )

            # 2. Extract and compute fields
            final_amount = float(data['final_amount'])
            reward_rate = 0.2  # Default 20%
            reward_amount = final_amount * reward_rate

            # 3. Compute date fields
            skrech_from = timezone.now()
            skrech_to = skrech_from + timedelta(days=7)
            valid_from = skrech_to + timedelta(days=30)
            valid_to = skrech_from + timedelta(days=30)
            removed_date = valid_from + timedelta(days=10)

            # 4. Create Reward Card entry
            RewardCards.objects.create(
                order_by=wallet,
                product_name=data['product_name'],
                product_id=data['product_id'],
                final_amount=final_amount,
                order_date=data.get('order_date', timezone.now()),
                category=data['category'],
                reward_rate=reward_rate,
                reward_amount=reward_amount,
                is_active=data.get('is_active', False),
                processed=data.get('processed', False),
                skrech_from=skrech_from,
                skrech_to=skrech_to,
                valid_from=valid_from,
                valid_to=valid_to,
                removed_date=removed_date
            )

            return Response({'message': 'Reward card created successfully.'}, status=status.HTTP_201_CREATED)

        except KeyError as missing_key:
            return Response({'error': f'Missing required field: {missing_key}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)







from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from .models import RewardWallet, RewardCards

class CreateReedomView(APIView):
    def post(self, request):
        order_id = request.data.get('id')
        username = request.data.get('username')

        if not order_id or not username:
            return Response({"error": "Both 'id' and 'username' are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            card = RewardCards.objects.get(id=order_id)
        except RewardCards.DoesNotExist:
            return Response({"error": "Reward card not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            wallet = RewardWallet.objects.get(wallet_username=username)
        except RewardWallet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now()

        # Check if reward card is active and processed
        if not card.is_active:
            return Response({"error": "Reward card is not active."}, status=status.HTTP_400_BAD_REQUEST)

        if not card.processed:
            return Response({"error": "Reward card has not been processed yet."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if current time is within scratch period
        if not (card.skrech_from <= now <= card.skrech_to):
            return Response({"error": "Current time is outside scratch period."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if current time is within validity period
        if not (card.valid_from <= now <= card.valid_to):
            return Response({"error": "Reward card is not currently valid."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if removed date has passed
        if card.removed_date and now > card.removed_date:
            return Response({"error": "Reward card has been removed and cannot be redeemed."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate reward amount (use stored reward_amount if exists)
        reward_amount = card.reward_amount if card.reward_amount else (card.final_amount * Decimal(str(card.reward_rate)))

        # Ensure reward_amount is Decimal
        if not isinstance(reward_amount, Decimal):
            reward_amount = Decimal(str(reward_amount))

        # Ensure wallet_balance is Decimal and add reward_amount
        old_wallet_balance = wallet.wallet_balance
        wallet.wallet_balance = (wallet.wallet_balance or Decimal('0')) + reward_amount
        wallet.save()

        return Response({
            "wallet_username": wallet.wallet_username,
            "old_wallet_balance": str(old_wallet_balance),
            "reward_added": str(reward_amount),
            "new_wallet_balance": str(wallet.wallet_balance),
            "card_id": order_id,
            "message": "Reward redeemed successfully."
        }, status=status.HTTP_200_OK)
