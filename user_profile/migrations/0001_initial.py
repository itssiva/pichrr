# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20, blank=True)),
                ('last_name', models.CharField(max_length=20, blank=True)),
                ('avatar', models.ImageField(default=b'img/avatar/avatar.jpg', upload_to=b'img/avatar/')),
                ('gender', models.CharField(max_length=1, blank=True)),
                ('intro', models.CharField(max_length=500, blank=True)),
                ('photo_count', models.IntegerField(default=0)),
                ('rep_count', models.IntegerField(default=0)),
                ('followers', models.IntegerField(default=0)),
                ('following', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('created_ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('last_access_ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('last_access_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
