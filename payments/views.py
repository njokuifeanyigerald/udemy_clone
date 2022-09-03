from django.shortcuts import render
import os


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json


from courses.models import Course

import stripe


stripe_api_key = os.environ.get("STRIPE_API_KEY")
endpoint_secret=""
stripe.api_key =stripe_api_key


class PaymentHandler(APIView):
    def post(self, request):
        if request.body:
            body = json.load(request.body)
            if body  and len(body):
                course_line_items=[]
                cart_courses=[]
                for item in body:
                    try:
                        course=Course.objects.get(course_uuid=item)
                        line_item ={
                            "price_data": {
                                "currency": "usd",
                                "unit_amount": int(course.price*100),
                                "product_data":{
                                    "name": course.title
                                },
                            },
                            "quantity": 1
                            
                        }
                        course_line_items.append(line_item)
                        cart_courses.append(line_item)

                    except Course.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            
            checkout_session =stripe.checkout.Session.create(
                payment_method = ["card"],
                lines_items = course_line_items,
                mode="payment",
                success_url='http://localhost:3000/success',
                cancel_url='http://localhost:3000/failure',
            )

            session, err := checkout_session.New(params)
