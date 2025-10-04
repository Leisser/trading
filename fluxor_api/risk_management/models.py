from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RiskProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    risk_level = models.CharField(max_length=20, default='medium')
    max_loss = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.risk_level}"
