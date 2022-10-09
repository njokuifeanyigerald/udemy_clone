from django.contrib import admin
from .models import Payment, PaymentIntent


admin.site.register(Payment)
admin.site.register(PaymentIntent)

