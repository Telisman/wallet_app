from django.db import models
from wallet_processor.models import Customer

class Transaction(models.Model):
    value = models.FloatField()
    latency = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.value}: {self.latency} {self.customer}"
