from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='img/avatar/', default='img/avatar/avatar.jpg')
    gender = models.CharField(max_length=1, blank=True)
    intro = models.CharField(max_length=500, blank=True)
    photo_count = models.IntegerField(default=0)
    rep_count = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_ip = models.GenericIPAddressField(default='127.0.0.1')
    last_access_ip = models.GenericIPAddressField(default='127.0.0.1')
    last_access_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    def get_avatar(self):
        avatar = settings.DEFAULT_AVATAR_IMAGE
        if self.avatar:
            avatar = self.avatar;
        return avatar


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)


# Followers and Following of a User
# class Follow(models.Model):
#     follower = models.ForeignKey(User, related_name='follower')
#     following = models.ForeignKey(User, related_name='following')
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return self.follower.username + ' following ' + self.following.username


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "avatar", "gender", "intro", "followers", 'following']


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_active", "is_superuser"]


admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Follow)
