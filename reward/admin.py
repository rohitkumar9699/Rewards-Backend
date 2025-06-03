
# from django.contrib import admin
# from .models import RewardWallet, RewardCards

# @admin.register(RewardWallet)
# class RewardWalletAdmin(admin.ModelAdmin):
#     list_display = ('wallet_username', 'wallet_fullname', 'wallet_communication_email', 'wallet_balance')
#     search_fields = ('wallet_username', 'wallet_fullname', 'wallet_communication_email')

# @admin.register(RewardCards)
# class RewardCardsAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in RewardCards._meta.fields]


from django.contrib import admin
from .models import RewardWallet, RewardCards


@admin.register(RewardWallet)
class RewardWalletAdmin(admin.ModelAdmin):
    list_display = ('wallet_username', 'wallet_fullname', 'wallet_communication_email', 'wallet_balance')
    search_fields = ('wallet_username', 'wallet_fullname', 'wallet_communication_email')
    list_filter = ('wallet_communication_email',)
    readonly_fields = ('wallet_balance',)

    fieldsets = (
        ('User Info', {
            'fields': ('wallet_username', 'wallet_fullname', 'wallet_communication_email')
        }),
        ('Balance Details', {
            'fields': ('wallet_balance',)
        }),
    )


@admin.register(RewardCards)
class RewardCardsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order_by', 'product_name', 'product_id', 'final_amount',
        'reward_rate', 'reward_amount', 'is_active', 'processed', 'scratch_status',
        'created_at'
    )
    list_filter = ('category', 'is_active', 'processed', 'scratch_status', 'created_at')
    search_fields = ('product_name', 'product_id', 'order_by__wallet_username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'scratch_from')

    fieldsets = (
        ('Product Info', {
            'fields': ('order_by', 'product_name', 'product_id', 'category')
        }),
        ('Transaction Info', {
            'fields': ('final_amount', 'reward_rate', 'reward_amount')
        }),
        ('Status Flags', {
            'fields': ('is_active', 'processed', 'scratch_status')
        }),
        ('Scratch Timing', {
            'fields': ('scratch_from', 'scratch_to')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
