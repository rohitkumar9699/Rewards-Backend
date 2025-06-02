from django.db import models

class RewardWallet(models.Model):
    wallet_username = models.CharField(max_length=100, unique=True)
    wallet_fullname = models.CharField(max_length=100)
    wallet_communication_email = models.EmailField()
    wallet_balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.wallet_username


class RewardOrders(models.Model):
    order_by = models.ForeignKey(RewardWallet, to_field='wallet_username', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=50)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    reward_rate = models.FloatField(default=0.00)

    def __str__(self):
        return f"Reward #{self.id} - {self.product_name}"
