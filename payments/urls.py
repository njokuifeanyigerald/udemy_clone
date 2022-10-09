from django.urls import path 
from .views import PaymentHandler, Webhook


urlpatterns = [
    path("", PaymentHandler.as_view(), name="payment_handler"),
    path("webhook/", Webhook.as_view(), name="webhook"),

]
