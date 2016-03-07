from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from user_profile.models import UserProfile
from .forms import UserProfileForm
from post.models import Post
from post.display import votes_and_favorites
from django.contrib import messages

N_POSTS = settings.POSTS_PER_PAGE
languages = ['Language', 'English', 'Hindi', 'Telugu', 'Tamil', 'Kannada']


@login_required
def update_profile(request):
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1
    userprofile = UserProfile.objects.get(user=request_user)

    if request.POST:
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            userprofile.gender = data['gender']
            userprofile.intro = data['intro']
            if request.FILES:
                userprofile.avatar.delete()
                userprofile.avatar = data['avatar']
            userprofile.first_name = data['first_name']
            userprofile.last_name = data['last_name']
            userprofile.save()
            messages.add_message(request, messages.SUCCESS, "Profile Successfully updated")
    else:
        data = {'first_name': userprofile.first_name,
                'last_name': userprofile.last_name,
                'avatar': userprofile.avatar,
                'gender': userprofile.gender,
                'intro': userprofile.intro
                }
        form = UserProfileForm(initial=data)
    return render_to_response('update_profile.html', {'form': form, 'media_url':settings.MEDIA_URL}, RequestContext(request))


def profile(request, username):

    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1

    user_param = User.objects.get(username=username)
    post_list = Post.objects.filter(user=user_param, active=True, is_anonymous=False)
    profile = UserProfile.objects.get(user=user_param)

    following_posts = []
    if not request.user.is_anonymous():
        upvotes, downvotes, favorites_list = votes_and_favorites(request_user)

    try:
        offset = int(request.GET.get('older', 1))
    except ValueError:
        offset = 1
    paginator = Paginator(post_list, N_POSTS)

    try:
        latest_items = paginator.page(offset)
    except PageNotAnInteger:
        latest_items = paginator.page(1)
    except EmptyPage:
        return HttpResponse(0)

    if request.is_ajax():
        return render_to_response('posts_in_profile.html', {
                                'media_url': settings.MEDIA_URL, 'profile': profile, 'posts': latest_items,
                                'upvotes': upvotes, 'downvotes':downvotes, 'favorites': favorites_list,
                                'offset': latest_items.number + 1},
                                RequestContext(request))

    else:
        return render_to_response('profile.html', {
                                    'profile': profile, 'posts': latest_items, 'media_url': settings.MEDIA_URL,
                                    'upvotes': upvotes, 'downvotes':downvotes, 'favorites': favorites_list,
                                    'offset': latest_items.number + 1,
                                    'type': 1, 'lang': languages[int(lang)]},
                                    RequestContext(request))

@login_required
def delete_account(request):
    if request.POST:
        user = User.objects.filter(id=request.user.id)
        user.delete()
        messages.add_message(request, messages.SUCCESS, 'Your account has been successfully deleted, We are sorry, you have to leave.')
        return HttpResponseRedirect('/')

    return render_to_response('delete_account.html', RequestContext(request))



"""
def followers(request, username):
    lang = request.COOKIES['lang']
    lid = []
    fid = []
    user = User.objects.get(username=username)
    context = RequestContext(request)
    can_edit, is_following = False, False
    if not request.user.is_anonymous():
        lid, fid = collection(request.user)
        can_edit, is_following = perms(request, username)
        print "!!!!!!!!", can_edit, is_following
    profile = UserProfile.objects.get(user=user)
    list = Follow.objects.filter(following=user)
    followers_list = [element.follower for element in list]
    return render_to_response('profile.html', {'profile': profile, 'people': followers_list,
                                               'can_edit': can_edit, 'is_following': is_following,
                                               'media_url': settings.MEDIA_URL,
                                               'type': 6, 'lang': languages[int(lang)]}, context)


def following(request, username):
    lang = request.COOKIES['lang']
    lid = []
    fid = []
    user = User.objects.get(username=username)
    context = RequestContext(request)
    can_edit, is_following = False, False
    if not request.user.is_anonymous():
        lid, fid = collection(request.user)
        can_edit, is_following = perms(request, username)
    profile = UserProfile.objects.get(user=user)
    list = Follow.objects.filter(follower=user)
    following_list = [element.following for element in list]

    return render_to_response('profile.html', {'profile': profile, 'people': following_list, 'can_edit': can_edit,
                                               'is_following': is_following, 'media_url': settings.MEDIA_URL,
                                               'type': 5, 'lang': languages[int(lang)]}, context)


@login_required
def follow(request, username):
    follower = request.user

    try:
        user = get_object_or_404(User, username=username)
        following = Follow.objects.filter(follower=follower, following=user).count()
        follow_flag = 0

        if not following:
            follow_flag = 1
            follow_obj = Follow(follower=follower, following=user)
            follow_obj.save()
            user.userprofile.followers += 1
            user.userprofile.save()
            follower.userprofile.following += 1
            follower.userprofile.save()

        else:
            follow_flag = -1;
            follow_obj = Follow.objects.get(follower=follower, following=user)
            follow_obj.delete()
            user.userprofile.followers -= 1
            user.userprofile.save()
            follower.userprofile.following -= 1
            follower.userprofile.save()
        return HttpResponseRedirect('/profile/' + username)

    except User.DoesNotExist:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
"""

