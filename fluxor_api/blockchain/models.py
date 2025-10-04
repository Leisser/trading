from django.db import models

class BlockchainData(models.Model):
    network = models.CharField(max_length=50)
    block_height = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.network} - {self.block_height}"
