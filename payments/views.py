import stripe
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

from payments.models import Order


@api_view(['GET'])
def get_payment_id(request, order_id):
    try:
        order = Order.objects.select_related('discount', 'tax').get(id=order_id)
    except Order.DoesNotExist:
        return Response('Order does not exist')

    discounts = []
    taxes = []
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if order.discount:
        coupon = stripe.Coupon.create(
            percent_off=order.discount.amount,
            duration="once",
        )
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
                'unit_amount': int(order_item.item.price * 100),
            },
            'quantity': order_item.quantity,
            'tax_rates': taxes,
        }
        for order_item in order.order_items.select_related('item')
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
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response('Order does not exist')

    context = {
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'order': order,
        'items': order.order_items.all(),
    }
    return render(request, 'checkout.html', context=context)
