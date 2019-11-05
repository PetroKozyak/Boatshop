from django.contrib.auth.models import User
from rest_framework import serializers

from boatshop_api.models import Boat, OrderBoat


class BoatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boat
        fields = "__all__"


class OrderBoatSerializer(serializers.ModelSerializer,):

    class Meta:
        model = OrderBoat
        fields = "__all__"
