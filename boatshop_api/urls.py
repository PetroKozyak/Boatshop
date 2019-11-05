from rest_framework import routers
from .views import BoatViewSet, OrderBoatViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"boats", BoatViewSet, basename="boats")
router.register(r"orders", OrderBoatViewSet, basename="orders")

urlpatterns = [
    path(r'', include(router.urls))
]