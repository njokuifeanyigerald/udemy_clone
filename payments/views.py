from decimal import Decimal
import os
import json



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import PaymentIntent,Payment
from courses.models import Course

import stripe


stripe_api_key = os.environ.get("STRIPE_API_KEY")
endpoint_secret = 'whsec_f469efacfdbff7ea7cc49c0888d53f470f910fe9cd2b8d3f545f3da03a65204e'

stripe.api_key =stripe_api_key


class PaymentHandler(APIView):
    def post(self, request):
        if request.body:
            body = json.loads(request.body)
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
                        cart_courses.append(course)

                    except Course.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            
            checkout_session =stripe.checkout.Session.create(
                payment_method_types = ["card"],
                line_items = course_line_items,
                mode="payment",
                success_url='http://localhost:3000/success',
                cancel_url='http://localhost:3000/failure',
            )

            intent = PaymentIntent.objects.create(
                payment_intent_id = checkout_session.payment_intent,
                checkout_id = checkout_session.id,
                user=request.user
            )
            intent.course.add(*cart_courses)

            return Response({"url": checkout_session.url})


class Webhook(APIView):
    def post(self, request):
        
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
             # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=status.HTTP_400_BAD_REQUEST)

        

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            try:
                intent = PaymentIntent.objects.get(checkout_id=session.id, payment_intent_id=session.payment_intent)

            except PaymentIntent.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            Payment.objects.create(
                payment_intent=intent,
                total_amount=Decimal(session.amount_total/100)
            )

            intent.user.paid_courses.add(*intent.course.all())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #  if event['type'] == 'checkout.session.completed':
        #     session = event['data']['object']

        #     # Save an order in your database, marked as 'awaiting payment'
        #     create_order(session)

        #     # Check if the order is already paid (for example, from a card payment)
        #     #
        #     # A delayed notification payment will have an `unpaid` status, as
        #     # you're still waiting for funds to be transferred from the customer's
        #     # account.
        #     if session.payment_status == "paid":
        #     # Fulfill the purchase
        #     fulfill_order(session)

        # elif event['type'] == 'checkout.session.async_payment_succeeded':
        #     session = event['data']['object']

        #     # Fulfill the purchase
        #     fulfill_order(session)

        # elif event['type'] == 'checkout.session.async_payment_failed':
        #     session = event['data']['object']

        #     # Send an email to the customer asking them to retry their order
        #     email_customer_about_failed_payment(session)

        # Passed signature verification
        return Response(status=status.HTTP_200_OK)

                


       

        