from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from boatshop_api.models import Boat, OrderBoat
from boatshop_api.serializers import BoatSerializer, OrderBoatSerializer, User, UserSerializer
from rest_framework.viewsets import GenericViewSet
from boatshop_api.permissions import IsOwnerOrReadOnly, HasPermissionForUser, HasPermissionForOrder
from rest_framework import permissions


class BoatViewSet(viewsets.ModelViewSet):
    queryset = Boat.objects.all()
    serializer_class = BoatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class OrderBoatViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       GenericViewSet, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = OrderBoat.objects.all()
    serializer_class = OrderBoatSerializer
    permission_classes = (IsAuthenticated, HasPermissionForOrder,)

    def get_queryset(self):
        queryset = self.queryset.filter(Q(buyer=self.request.user) | Q(boat__owner=self.request.user))
        return queryset


class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin, GenericViewSet):
    queryset = User.objects.prefetch_related("profile").select_related(
        "profile"
    )
    serializer_class = UserSerializer
    permission_classes = (HasPermissionForUser,)
