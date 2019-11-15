from django.contrib.auth.models import User
from rest_framework import serializers
from boatshop_api.models import Boat, OrderBoat
from boatshop_api.helpers.serializer_helpers import UserSerializerHelper


class UserSerializer(UserSerializerHelper, serializers.ModelSerializer):
    password_confirm = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirm",
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        action = self.context['view'].action

        if action in ['update', 'partial_update'] and data.get('password_confirm'):
            data.pop('password_confirm')
        return data


class BoatSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def save(self, **kwargs):
        """Include default for read_only user field"""
        kwargs["owner"] = self.fields["owner"].get_default()
        return super().save(**kwargs)

    class Meta:
        model = Boat
        fields = "__all__"


class OrderBoatSerializer(serializers.ModelSerializer, ):
    buyer = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = OrderBoat
        fields = ("id", "boat", "buyer", "approved")

        extra_kwargs = {
            'approved': {'read_only': True},
            'boat': {'read_only': False}
        }

    def __init__(self, *args, **kwargs):
        super(OrderBoatSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['boat'].queryset = Boat.objects.exclude(owner=request_user)

    def get_extra_kwargs(self):
        extra_kwargs = super(OrderBoatSerializer, self).get_extra_kwargs()
        action = self.context['view'].action

        if action in ['update', 'partial_update'] and self.instance.boat.owner == self.context['request'].user:
            kwargs = extra_kwargs.get('approved', {})
            kwargs['read_only'] = False
            extra_kwargs['approved'] = kwargs

            kwargs = extra_kwargs.get('boat', {})
            kwargs['read_only'] = True
            extra_kwargs['boat'] = kwargs

        return extra_kwargs

    def to_representation(self, instance):
        data = super(OrderBoatSerializer, self).to_representation(instance)
        data['boat'] = BoatSerializer(instance.boat).data
        return data

    def save(self, **kwargs):
        kwargs["buyer"] = self.context['request'].user
        return super().save(**kwargs)
