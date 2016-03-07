from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Tag(models.Model):
    name = models.TextField()#keep max length to 20
    obj_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "obj_count"]


admin.site.register(Tag, TagAdmin)