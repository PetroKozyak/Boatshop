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
        write_only_fields = ('password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }


class BoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boat
        fields = "__all__"


class OrderBoatSerializer(serializers.ModelSerializer,):
    buyer = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        data = super(OrderBoatSerializer, self).to_representation(instance)
        data['boat'] = BoatSerializer(instance.boat).data
        data['approved'] = instance.approved
        return data

    def __init__(self, *args, **kwargs):
        super(OrderBoatSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        self.fields['boat'].queryset = Boat.objects.exclude(owner=request_user)

    class Meta:
        model = OrderBoat
        fields = ("id", "boat", "buyer")

    def save(self, **kwargs):
        kwargs["buyer"] = self.fields["buyer"].get_default()
        return super().save(**kwargs)
