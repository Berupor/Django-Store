from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from item.models import Item


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True, through="ProfileItem")

    class Meta:
        db_table = "profile"


class ProfileItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "profile_item"


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    user_profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(post_save_profile_create, sender=User)
