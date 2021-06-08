from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.serializers import ModelSerializer

from brain.budgets import models


class CheckUserMixin(object):

    @classmethod
    def check_user(cls, obj, user):
        if obj.user != user:
            raise ValidationError(_('User mismatch in a foreign field.'), code='user_mismatch')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = models.Profile
        fields = (
            'created',
            'currency',
            'id',
            'user',
        )
        read_only_fields = (
            'id',
        )


class AccountSerializer(CheckUserMixin, ModelSerializer):
    class Meta:
        model = models.Account
        fields = (
            'balance',
            'created',
            'id',
            'name',
            'profile',
            'user',
        )
        read_only_fields = (
            'id',
        )

    @transaction.atomic
    def create(self, validated_data):
        self.check_user(validated_data['profile'], validated_data['user'])

        return models.Account.objects.create(**validated_data)


class BudgetSerializer(CheckUserMixin, ModelSerializer):
    class Meta:
        model = models.Budget
        fields = (
            'created',
            'id',
            'limit',
            'name',
            'period_in_months',
            'profile',
            'user',
        )
        read_only_fields = (
            'id',
        )

    @transaction.atomic
    def create(self, validated_data):
        self.check_user(validated_data['profile'], validated_data['user'])

        return models.Budget.objects.create(**validated_data)


class ActivitySerializer(ModelSerializer):
    class Meta:
        model = models.Activity
        fields = (
            'account',
            'amount',
            'created',
            'id',
            'name',
            'user',
        )
        read_only_fields = (
            'id',
        )


class IncomeSerializer(CheckUserMixin, ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = models.Income
        fields = (
            'activity',
            'id',
        )
        read_only_fields = (
            'id',
        )

    @transaction.atomic
    def create(self, validated_data):
        amount = validated_data['activity']['amount']
        account = validated_data['activity']['account']

        self.check_user(account, validated_data['activity']['user'])

        activity = models.Activity.objects.create(**validated_data.pop('activity'))

        account.balance = account.balance + amount
        account.save()

        return models.Income.objects.create(activity=activity, **validated_data)


class ExpenseSerializer(CheckUserMixin, ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = models.Expense
        fields = (
            'activity',
            'budget',
            'id',
        )
        read_only_fields = (
            'id',
        )

    @transaction.atomic
    def create(self, validated_data):
        amount = validated_data['activity']['amount']
        account = validated_data['activity']['account']

        self.check_user(account, validated_data['activity']['user'])

        activity = models.Activity.objects.create(**validated_data.pop('activity'))

        account.balance = account.balance - amount
        account.save()

        return models.Expense.objects.create(activity=activity, **validated_data)


class TransferSerializer(CheckUserMixin, ModelSerializer):
    activity = ActivitySerializer()

    class Meta:
        model = models.Transfer
        fields = (
            'account',
            'activity',
            'id',
        )
        read_only_fields = (
            'id',
        )

    @transaction.atomic
    def create(self, validated_data):
        amount = validated_data['activity']['amount']
        account_from = validated_data['activity']['account']
        account_to = validated_data['account']

        self.check_user(account_from, validated_data['activity']['user'])
        self.check_user(account_to, validated_data['activity']['user'])

        activity = models.Activity.objects.create(**validated_data.pop('activity'))

        account_from.balance = account_from.balance - amount
        account_from.save()

        account_to.balance = account_to.balance + amount
        account_to.save()

        return models.Transfer.objects.create(activity=activity, **validated_data)
