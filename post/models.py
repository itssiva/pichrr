from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from tags.models import Tag
from utils.common_utils import txt2set

class Post(models.Model):
    ref_id = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    title = models.TextField()
    photo_url = models.TextField()  # max_length to 200
    post_type = models.SmallIntegerField(default=0) # for future usage 0 - image 1- image
    tags = models.ManyToManyField(Tag)
    txt_tags = models.TextField(blank=True)  # max_length = 50
    language1 = models.PositiveIntegerField(default=0) # implications are 1- English 2- Hindi 3-Telugu the rest will follow
    language2 = models.PositiveIntegerField(default=0, null=True)
    is_anonymous = models.BooleanField(default=False)
    attribution = models.TextField(blank=True, null=True)  # Keep max_length = 200
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    favorites = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    rep_count = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    is_safe = models.BooleanField(default=True)
    uploaded_ip = models.GenericIPAddressField(null=True)

    def __unicode__(self):
        return self.title

    def get_txt_tags_list(self):
        return self.txt_tags.replace(' ','').split(',')

    def txt_tag_set(self):
        return txt2set(self.txt_tags)

    # Adding tags when created or updated
    def add_txt_tags(self, txt_tag_set):
        for txt_tag in txt_tag_set:
            try:
                tag = Tag(name=txt_tag)
                try:
                    tag = Tag.objects.get(name=txt_tag)
                except:
                    pass
                if self.active:
                    tag.obj_count += 1
                tag.save()
                self.tags.add(tag)
            except Exception, e:
                print str(e)

    # Remove text tags when a photo is edited
    def remove_txt_tags(self, txt_tag_set):
        for txt_tag in txt_tag_set:
            try:
                tag = Tag.objects.get(name=txt_tag);
                self.tags.remove(tag)
                if self.active:
                    tag.obj_count -= 1
                if len(tag.photo_set.all()):
                    tag.save()
                else:
                    tag.delete()
            except:
                pass


class Vote(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    type = models.NullBooleanField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.post.title

class Favorite(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.post.title

class Report(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    type = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.post.title

class PostAdmin(admin.ModelAdmin):
    list_display = ["ref_id", "title", "user", "photo_url", "language1", "language2", "is_anonymous", "width", "height",
                    "created", "upvotes","downvotes", "favorites", "comments", "view_count"]

admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
admin.site.register(Favorite)
admin.site.register(Report)
