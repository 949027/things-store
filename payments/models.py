from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField('Наименование', max_length=100)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField(
        'Стоимость',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    #currency

    def str(self):
        return self.name


class Discount(models.Model):
    name = models.CharField('Наименование', max_length=100)
    amount = models.DecimalField(
        'Размер скидки',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def str(self):
        return self.name


class Tax(models.Model):
    name = models.CharField('Наименование', max_length=100)
    amount = models.DecimalField(
        'Размер налога',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def str(self):
        return self.name


class Order(models.Model):
    item = models.ManyToManyField(
        Item,
        verbose_name='Товар',
        related_name='items',
    )
    discount = models.ManyToManyField(
        Discount,
        verbose_name='Скидка',
        related_name='discounts',
    )
    tax = models.ManyToManyField(
        Tax,
        verbose_name='Налог',
        related_name='taxes',
    )
    total_price = models.DecimalField(
        'Общая стоимость',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def str(self):
        return self.pk
