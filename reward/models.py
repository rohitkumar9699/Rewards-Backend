from django.db import models
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class RewardWalletManager(BaseUserManager):
    def create_user(self, wallet_username, password=None, **extra_fields):
        if not wallet_username:
            raise ValueError('The wallet_username must be set')
        user = self.model(wallet_username=wallet_username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, wallet_username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(wallet_username, password, **extra_fields)

class RewardWallet(AbstractBaseUser, PermissionsMixin):
    wallet_username = models.CharField(max_length=100, unique=True)
    wallet_fullname = models.CharField(max_length=100)
    wallet_communication_email = models.EmailField()
    wallet_balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'wallet_username'
    REQUIRED_FIELDS = []

    objects = RewardWalletManager()

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
    
    def save(self, *args, **kwargs):
        if self.reward_rate and self.final_amount:
            self.reward_amount = self.final_amount * self.reward_rate
            self.scratch_from = timezone.now()
            self.scratch_to = self.scratch_from + timedelta(days=7)
        super().save(*args, **kwargs)

