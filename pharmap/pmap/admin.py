from django.contrib import admin
from .models import Pharmacy, Medicine, InventoryMed, MedList, ListItem

# Register your models here.
admin.site.register(Pharmacy)
admin.site.register(Medicine)
admin.site.register(InventoryMed)
admin.site.register(MedList)
admin.site.register(ListItem)