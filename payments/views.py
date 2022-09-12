from contextlib import suppress
import stripe
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payments.models import Item, Order


@api_view(['GET'])
def get_payment_id(request, order_id):
    discounts = []
    taxes = []
    stripe.api_key = settings.STRIPE_SECRET_KEY
    with suppress(Item.DoesNotExist):
        order = Order.objects.get(id=order_id)

        if order.discount:
            coupon = stripe.Coupon.create(percent_off=order.discount.amount, duration="once")
            discounts.append({'coupon': coupon.id})

        if order.tax:
            tax = stripe.TaxRate.create(
                display_name=order.tax.name,
                inclusive=False,
                percentage=order.tax.amount,
            )
            taxes.append(tax.id)

        line_items = [
            {
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': order_item.item.name,
                    },
                    'unit_amount': int(order_item.price * 100),
                },
                'quantity': order_item.quantity,
                'tax_rates': taxes,
            }
            for order_item in order.order_items.all()
        ]

        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            discounts=discounts,
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        return Response(session.id)


@api_view(['GET'])
def get_payment_page(request, order_id):
    with suppress(Item.DoesNotExist):
        order = Order.objects.get(id=order_id)
        context = {
            'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'order': order,
            'items': order.order_items.all(),
        }
        return render(request, 'checkout.html', context=context)
