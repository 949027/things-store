from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Item(models.Model):
    name = models.CharField('Наименование', max_length=100)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField(
        'Стоимость',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField('Наименование', max_length=100)
    amount = models.IntegerField(
        'Размер скидки',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return self.name


class Tax(models.Model):
    name = models.CharField('Наименование', max_length=100)
    amount = models.IntegerField(
        'Размер налога, %',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    discount = models.ForeignKey(
        Discount,
        verbose_name='Скидка',
        related_name='orders',
        blank=True,
        on_delete=models.CASCADE,
    )
    tax = models.ForeignKey(
        Tax,
        verbose_name='Налог',
        related_name='orders',
        blank=True,
        on_delete=models.CASCADE,
    )
    total_price = models.DecimalField(
        'Общая стоимость',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f'Заказ № {self.id}'

    @property
    def total_price(self):
        total_price = 0
        for item in self.order_items.all():
            total_price += item.price * item.quantity
        if self.discount:
            total_price -= total_price * self.discount.amount / 100
        if self.tax:
            total_price += total_price * self.tax.amount / 100
        return total_price

    def str(self):
        return self.pk


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='order_items',
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name='Товар',
        related_name='items',
    )
    quantity = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)],
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )


@receiver(pre_save, sender=OrderItem)
def calculate_price(instance, **kwargs):
    instance.price = instance.item.price * instance.quantity
