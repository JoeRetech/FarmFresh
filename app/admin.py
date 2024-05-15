from django.contrib import admin
from .models import Product,Cart,Billing,FarmerRequest
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Billing)
admin.site.register(FarmerRequest)