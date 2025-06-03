from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import RewardWallet, RewardCards

from decimal import Decimal

COIN_EXCHANGE_RATE =  0.2  # Float 
WALLET_EXCHANGE_RATE = Decimal(0.2)


class CreateCardView(APIView):
    def post(self, request):
        data = request.data

        print(data)

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
            reward_rate = COIN_EXCHANGE_RATE
            reward_amount = final_amount * reward_rate

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
                processed=data.get('processed', False)
            )

            return Response({'message': 'Reward card created successfully.'}, status=status.HTTP_201_CREATED)

        except KeyError as missing_key:
            return Response({'error': f'Missing required field: {missing_key}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class CardScratchView(APIView):
    def post(self, request):
        try:
            card_id = request.data.get('id')
            username = request.data.get('username')

            if not card_id or not username:
                return Response({"error": "Both 'id' and 'username' are required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                card = RewardCards.objects.get(id=card_id, order_by__wallet_username=username)
            except RewardCards.DoesNotExist:
                return Response({"error": "Reward card not found for this user."}, status=status.HTTP_404_NOT_FOUND)

            now = timezone.now()

           
            # Check if card has already been scratched
            if card.scratch_status:
                return Response({"error": "Card has already been scratched."}, status=status.HTTP_400_BAD_REQUEST)

            # Check scratch time window
            if card.scratch_from and card.scratch_to:
                if not (card.scratch_from <= now <= card.scratch_to):
                    print(now)
                    return Response({"error": "Current time is outside the scratch time window."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Scratch time window not defined."}, status=status.HTTP_400_BAD_REQUEST)

            # Mark the card as scratched
            card.scratch_status = True
            card.is_active = True
            card.valid_from = now 
            card.valid_to = now + timedelta(days=30)

            
            try:
                card.save()
            except Exception as e:
                return Response({"error": f"Failed to update card data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "message": "Card scratched successfully.",
                "card_id": card.id,
                "product_name": card.product_name,
                "reward_amount": str(card.reward_amount),
                "scratch_time": now.isoformat()
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class CardReedomView(APIView):
    def post(self, request):
        try:
            card_id = request.data.get('id')
            username = request.data.get('username')

            if not card_id or not username:
                return Response({"error": "Both 'id' and 'username' are required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                card = RewardCards.objects.get(id=card_id, order_by__wallet_username=username)
            except RewardCards.DoesNotExist:
                return Response({"error": "Reward card not found for this user."}, status=status.HTTP_404_NOT_FOUND)

            try:
                wallet = RewardWallet.objects.get(wallet_username=username)
            except RewardWallet.DoesNotExist:
                return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

            now = timezone.now()

            # Status checks
            if not card.is_active:
                return Response({"error": "Reward card is not active."}, status=status.HTTP_400_BAD_REQUEST)

            if  card.processed:
                return Response({"error": "Reward card has not been processed yet."}, status=status.HTTP_400_BAD_REQUEST)

            if not card.scratch_status:
                return Response({"error": "Card must be scratched before redemption."}, status=status.HTTP_400_BAD_REQUEST)

            if card.valid_from and card.valid_to:
                if not (card.valid_from <= now <= card.valid_to):
                    return Response({"error": "Reward card is not currently valid."}, status=status.HTTP_400_BAD_REQUEST)


            card.is_active= False
            card.processed= True
            card.save()

            try:
                old_wallet_balance = wallet.wallet_balance or Decimal("0")
                wallet.wallet_balance = old_wallet_balance + card.reward_amount
                wallet.save()
            except Exception as e:
                return Response({"error": f"Failed to update wallet balance: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                "wallet_username": wallet.wallet_username,
                "old_wallet_balance": str(old_wallet_balance),
                "reward_added": str(card.reward_amount),
                "new_wallet_balance": str(wallet.wallet_balance),
                "card_id": card_id,
                "message": "Reward redeemed successfully."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import requests

class ReedomCoinView(APIView):
    def post(self, request):
        wallet_username = request.data.get('wallet_username')

        try:
            wallet = RewardWallet.objects.get(wallet_username=wallet_username)
            wallet_balance = wallet.wallet_balance * WALLET_EXCHANGE_RATE 

            data = {
                "wallet_username": wallet_username,
                "wallet_balance": str(wallet_balance)  # Convert Decimal to string
            }

            try:
                response = requests.post("http://localhost:8000/add-money-to-wallet/", json=data)
                if response.status_code == 200:
                    wallet.wallet_balance = 0
                    wallet.save()

                    return Response(response.json(), status=status.HTTP_200_OK)
                else:
                    return Response({"error": f"Wallet API returned status {response.status_code}", "body": response.text}, status=response.status_code)

            except Exception as e:
                return Response({"error": f"Failed to reach wallet API: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        except RewardWallet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)
