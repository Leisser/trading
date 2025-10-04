from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    alert_type = models.CharField(max_length=20)
    target_price = models.DecimalField(max_digits=20, decimal_places=8)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.symbol} {self.alert_type}"
