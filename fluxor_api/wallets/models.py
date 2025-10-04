from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallets')
    address = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.address}"
