from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ComplianceCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.check_type}"
