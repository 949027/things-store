from django.urls import path

from .views import get_payment_id, get_payment_page

urlpatterns = [
    path('buy/<int:item_id>', get_payment_id, name='get_payment_id'),
    path('item/<int:item_id>', get_payment_page, name='get_payment_page'),
]
