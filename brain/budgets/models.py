from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


DECIMAL_PLACES = 2
MAX_DECIMAL_DIGITS = 14
MIN_DECIMAL_VALUE = '0.01'

MAX_NAME_LENGTH = 32


class Profile(models.Model):
    CURRENCY_CHOICES = [('CZK', 'CZK'), ('EUR', 'EUR'), ('USD', 'USD'), ('TRY', 'TRY')]

    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        default='CZK',
        max_length=3,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )


class Account(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    balance = models.DecimalField(
        decimal_places=DECIMAL_PLACES,
        default=Decimal('0'),
        max_digits=MAX_DECIMAL_DIGITS,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )
    profile = models.ForeignKey(
        'budgets.Profile',
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )


class Budget(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    limit = models.DecimalField(
        decimal_places=DECIMAL_PLACES,
        max_digits=MAX_DECIMAL_DIGITS,
        validators=[MinValueValidator(Decimal(MIN_DECIMAL_VALUE))],
    )
    period_in_months = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )
    profile = models.ForeignKey(
        'budgets.Profile',
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )


class Activity(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    amount = models.DecimalField(
        decimal_places=DECIMAL_PLACES,
        max_digits=MAX_DECIMAL_DIGITS,
        validators=[MinValueValidator(Decimal(MIN_DECIMAL_VALUE))],
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
    )
    account = models.ForeignKey(
        'budgets.Account',
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )


class Income(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    activity = models.ForeignKey(
        'budgets.Activity',
        on_delete=models.PROTECT,
    )


class Expense(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    activity = models.ForeignKey(
        'budgets.Activity',
        on_delete=models.PROTECT,
    )
    budget = models.ForeignKey(
        'budgets.Budget',
        on_delete=models.PROTECT,
    )


class Transfer(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
    )
    activity = models.ForeignKey(
        'budgets.Activity',
        on_delete=models.PROTECT,
    )
    account = models.ForeignKey(
        'budgets.Account',
        on_delete=models.PROTECT,
    )
