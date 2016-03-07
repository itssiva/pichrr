# Create your views here.
import json
import uuid
import os
import random
import logging
import mimetypes
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from .models import Post, Vote, Favorite, Report
from .forms import PostForm, ReportForm
from utils.image_utils import reduce_quality_and_make_thumbs
from utils.common_utils import txt2set

# Create your views here.
languages = ['Language', 'English', 'Hindi', 'Telugu', 'Tamil', 'Kannada']
N_POSTS = settings.POSTS_PER_PAGE
MEDIA_URL = settings.MEDIA_URL


# Create your views here.
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_ref_id():
    ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
    try:
        Post.objects.get(ref_id=ref_id)
        logging.log('CRITICAL', 'refid repeated')
        get_ref_id()
    except:
        return ref_id
    return ref_id


def store_in_s3(filename, content):
    conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
    b = conn.get_bucket("itssiva")
    mime = mimetypes.guess_type(filename)[0]
    k = Key(b)
    k.key = filename
    k.set_metadata("Content-Type", mime)
    k.set_contents_from_string(content)
    k.set_acl("public-read")


def upload_photo(photo, ext, photo_size, attribution):
    """
    Upload pictures, return the image name
     Pictures distributed in 100 folders,
     To prevent an excessive number of files in a single folder within
    """
    sub_folder_name = str(random.randint(0, 100))
    path = os.path.join(settings.MEDIA_ROOT, sub_folder_name)

    if not os.path.exists(path):  # If the folder does not exist, create a folder
        os.mkdir(path)
    import time
    filename = str(time.time()).replace('.', '_') + str(random.randrange(0, 99999, 1)) + '.' + ext
    ret_filename = os.path.join(sub_folder_name, filename)
    filename = os.path.join(path, filename)

    imgfile = open(filename, 'wb')
    for chunk in photo.chunks():
        imgfile.write(chunk)
    imgfile.close()

    type, width, height = reduce_quality_and_make_thumbs(filename, path, photo_size, attribution)
    return ret_filename, type, width, height


@login_required
def post(request):
    user = request.user
    form = PostForm()

    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["photo"]
            file.seek(0)
            photo_size = file.size
            filename = file.name
            content = file.read()
            # store_in_s3(filename, content)
            data = form.cleaned_data
            post = Post()
            post.ref_id = get_ref_id()
            post.user = user
            post.title = data['title']
            post.txt_tags = data['txt_tags']
            post.language1 = int((data['languages'])[0])
            if len(data['languages']) == 2:
                post.language2 = int(data['languages'][1])
            post.is_anonymous = data['is_anonymous']
            post.attribution = data['creator']
            post.photo_url, post.post_type, post.width, post.height = \
                upload_photo(data['photo'], data['photo'].name.split('.')[-1], photo_size, post.attribution)
            if post.post_type == 1:
                print "inside"
                post.photo_url = post.photo_url.replace('.gif', '.mp4')
            uploaded_ip = get_ip(request)
            post.uploaded_ip = uploaded_ip
            txt_tags = data['txt_tags']
            post.save()
            post.add_txt_tags(txt2set(txt_tags))
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Your photo has been added')
            return HttpResponseRedirect('/')
        else:
            render_to_response('post.html', {'form': form}, RequestContext(request))

    return render_to_response('post.html', {'form': form}, RequestContext(request))


def view_post(request, id):
    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request
    report_form = 0

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1

    post = get_object_or_404(Post, ref_id=id)

    if not request.user.is_anonymous():
        report_form = ReportForm()
        try:
            vote = Vote.objects.get(post=post, user=request_user)
            if vote.type is True:
                upvotes.append(post.id)
            else:
                downvotes.append(post.id)
            if Favorite.objects.filter(post=post, user=request_user).exists():
                favorites_list.append(post.id)
        except Vote.DoesNotExist:
            pass

    if post.active == False:
        raise Http404
    else:
        post.view_count = post.view_count + 1
        post.save()

    return render_to_response('post_view.html', {
        'media_url': MEDIA_URL, 'report_form': report_form,
        'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
        'post': post, 'lang': languages[int(lang)]},
                              RequestContext(request))


def rules(request):
    return render_to_response('post_rules.html', RequestContext(request))

@login_required
def delete_post(request, id):
    if request.POST:
        post = get_object_or_404(Post, ref_id=id)
        u = request.user
        if (post.user != u):
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

        try:
            if post.active:
                for t in post.tags.all():
                    t.obj_count -= 1
                    if len(t.post_set.all()) > 1:  # = 1 for the current picture
                        t.save()
                    else:
                        t.delete()
            import os
            os.remove(os.path.join(settings.PHOTO_ROOT, post.photo_name()))
            os.remove(os.path.join(settings.PHOTO_ROOT, post.thumb_big_photo_name()))
            os.remove(os.path.join(settings.PHOTO_ROOT, post.thumb_small_photo_name()))
        except Exception:
            pass
        post.delete()
    return HttpResponseRedirect('/')


@login_required
def upvote(request, id):
    logging.log(logging.DEBUG, "In Upvote!!")
    request_user = request.user
    liked_flag = 0
    try:
        post = get_object_or_404(Post, ref_id=id)
        current_upvotes = post.upvotes
        current_downvotes = post.downvotes
        like_object, created = Vote.objects.get_or_create(user=request_user, post=post)
        if created:
            liked_flag = 1
            current_upvotes += 1
            like_object.type = True
            like_object.save()
        else:
            if like_object.type == False:
                current_upvotes += 1
                current_downvotes -= 1
                liked_flag = 1
                like_object.type = True
                like_object.save()
            else:
                current_upvotes -= 1
                liked_flag = -1
                like_object.delete()
        rep_count = (current_upvotes - current_downvotes)
        rep_count = rep_count if rep_count > 0 else 0
        Post.objects.filter(ref_id=id).update(upvotes=current_upvotes, downvotes=current_downvotes, rep_count=rep_count)

        if request.is_ajax():
            data = [{'rep_count': rep_count, 'liked_flag': liked_flag}]
            print json.dumps(data)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponseRedirect('/view_post/%s' % id)
    except Post.DoesNotExist:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def downvote(request, id):
    request_user = request.user
    disliked_flag = 0
    try:
        post = get_object_or_404(Post, ref_id=id)
        current_downvotes = post.downvotes
        current_upvotes = post.upvotes
        like_object, created = Vote.objects.get_or_create(user=request_user, post=post)
        if created:
            disliked_flag = 1
            current_downvotes += 1
            like_object.type = False
            like_object.save()
        else:
            if like_object.type is True:
                current_downvotes += 1
                current_upvotes -= 1
                disliked_flag = 1
                like_object.type = False
                like_object.save()
            else:
                current_downvotes -= 1
                disliked_flag = -1
                like_object.delete()
        rep_count = (current_upvotes - current_downvotes)
        rep_count = rep_count if rep_count > 0 else 0
        Post.objects.filter(ref_id=id).update(upvotes=current_upvotes, downvotes=current_downvotes, rep_count=rep_count)

        if request.is_ajax():
            data = [{'disliked_flag': disliked_flag, 'rep_count': rep_count}]
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponseRedirect('/view_post/%s' % id)
    except Post.DoesNotExist:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])




@login_required
def favorite(request, id):
    request_user = request.user
    favorite_flag = 0
    try:
        post = get_object_or_404(Post, ref_id=id)
        current_favorites = post.favorites
        favorite_obj, created = Favorite.objects.get_or_create(user=request_user, post=post)
        if created:
            favorite_flag = 1
            current_favorites += 1
            favorite_obj.type = True
            favorite_obj.save()
        else:
            current_favorites -= 1
            favorite_flag = -1
            favorite_obj.delete()
        # rep_count = (current_upvotes - current_downvotes)
        # rep_count = rep_count if rep_count > 0 else 0
        Post.objects.filter(ref_id=id).update(favorites=current_favorites)

        if request.is_ajax():
            data = [{ 'favorite_flag': favorite_flag}]
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponseRedirect('/view_post/%s' % id)
    except Post.DoesNotExist:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])



#
# @login_required
# def favorite(request, id):
#     collect_flag = 1
#
#     request_user = request.user
#     try:
#         post = get_object_or_404(Post, ref_id=id)
#         current_favorites = post.favorites
#         favorite_object, created = Favorite.objects.get_or_create(post=post, user=request_user)
#         if created:
#             current_favorites += 1
#             collect_flag = 1
#
#         else:
#             current_favorites -= 1
#             collect_flag = -1
#
#         Post.objects.filter(ref_id=id).update(favorites=current_favorites)
#
#         if request.is_ajax():
#             data = [{'collect_flag': collect_flag}]
#             return HttpResponse(json.dumps(data))
#         else:
#             return HttpResponseRedirect('/view_post/%s' % id)
#
#     except Post.DoesNotExist:
#         return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def report(request, id):
    if request.POST:

        form = ReportForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, ref_id=id)
            type = int(form.cleaned_data['report_type'])
            object, created = Report.objects.get_or_create(post=post, user=request.user, type=type)
            if created:
                messages.add_message(request, messages.SUCCESS, 'Reported, Thank you .')
            else:
                messages.add_message(request, messages.SUCCESS, 'You have already reported this image')

    return HttpResponseRedirect('/view_post/' + id)


from django_comments.signals import comment_was_posted
from django.dispatch import receiver


@receiver(comment_was_posted)
def update_count(sender, comment, request, **kwargs):
    post = Post.objects.get(id=comment.object_pk)
    post.comments += 1
    post.save()


"""
        # following = Follow.objects.filter(follower=request_user).values_list('following', flat=True)
        # for x in following:
        #     follow_posts = Post.objects.filter(user=x)
        #     following_posts.extend(follow_posts)
"""
