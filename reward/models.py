from django.db import models
from django.utils import timezone


class RewardWallet(models.Model):
    wallet_username = models.CharField(max_length=100, unique=True)
    wallet_fullname = models.CharField(max_length=100)
    wallet_communication_email = models.EmailField()
    wallet_balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.wallet_username



class RewardCards(models.Model):
    order_by = models.ForeignKey('RewardWallet', to_field='wallet_username', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=50)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100)
    reward_rate = models.DecimalField(max_digits=2, decimal_places=2)  # Percentage or multiplier
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2)  # reward = final_amount * rate

    is_active = models.BooleanField(default=False)    # default rue hona chaiye
    processed = models.BooleanField(default=False)

    scratch_status = models.BooleanField(default=False)
    scratch_from  =  models.DateTimeField(auto_now_add=True)
    scratch_to =  models.DateTimeField(null= True, blank=True)

    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Reward #{self.id} - {self.product_name}"

