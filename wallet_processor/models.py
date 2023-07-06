from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets

class Customer(models.Model):
    customer_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    balance = models.FloatField()

    def __str__(self):
        return f"{self.customer_id}: {self.first_name} {self.last_name}"

class APIKey(models.Model):
    key = models.CharField(max_length=64)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.key}"

@receiver(post_save, sender=Customer)
def assign_api_key(sender, instance, created, **kwargs):
    if created:
        api_key = secrets.token_hex(32)
        APIKey.objects.create(key=api_key, customer=instance)