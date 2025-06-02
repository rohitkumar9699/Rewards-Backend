
from django.contrib import admin
from .models import RewardWallet, RewardOrders

@admin.register(RewardWallet)
class RewardWalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_username', 'wallet_fullname', 'wallet_communication_email', 'wallet_balance')
    search_fields = ('wallet_username', 'wallet_fullname', 'wallet_communication_email')

@admin.register(RewardOrders)
class RewardOrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_by', 'product_name', 'product_id', 'final_amount', 'order_date', 'status', 'payment_status', 'category', 'reward_rate')
    list_filter = ('status', 'payment_status', 'category')
    search_fields = ('product_name', 'product_id', 'order_by__wallet_username')
    ordering = ('-order_date',)
