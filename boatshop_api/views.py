from rest_framework import viewsets
from boatshop_api.models import Boat, OrderBoat
from boatshop_api.serializers import BoatSerializer, OrderBoatSerializer
from rest_framework.permissions import IsAuthenticated


class BoatViewSet(viewsets.ModelViewSet):
    queryset = Boat.objects.all()
    serializer_class = BoatSerializer
    permission_classes = (IsAuthenticated,)


class OrderBoatViewSet(viewsets.ModelViewSet):
    queryset = OrderBoat.objects.all()
    serializer_class = OrderBoatSerializer
    permission_classes = (IsAuthenticated,)

