
from django.contrib import admin
from .models import RewardWallet, RewardCards

@admin.register(RewardWallet)
class RewardWalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_username', 'wallet_fullname', 'wallet_communication_email', 'wallet_balance')
    search_fields = ('wallet_username', 'wallet_fullname', 'wallet_communication_email')

@admin.register(RewardCards)
class RewardCardsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RewardCards._meta.fields]
