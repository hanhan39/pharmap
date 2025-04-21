from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pharmacy(models.Model):
    name = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} - {self.branch}'

class Medicine(models.Model):
    brand = models.CharField(max_length=50)
    generic = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.brand} ({self.generic})'

class InventoryMed(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, null=False)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.pharmacy}: {self.medicine} - PHP {self.price}'

class MedList(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField()

    def __str__(self):
        return f'{self.name} ({self.user}) - {self.created_at}'

class ListItem(models.Model):
    medlist = models.ForeignKey(MedList, on_delete=models.CASCADE, null=False)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.medlist}: {self.medicine}'