from django.db import models
from django.contrib.auth.models import User

User._meta.get_field("email")._unique = True


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Boat(models.Model):
    class Meta:
        db_table = "boat"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boats")
    boat = models.CharField(max_length=50)
    price = models.FloatField(null=False, blank=True)

    def __str__(self):
        return "{}".format(self.boat)


class OrderBoat(models.Model):
    class Meta:
        db_table = "orders"

    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_order')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.boat)
