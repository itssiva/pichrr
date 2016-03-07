from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.core.cache import cache
from user_profile.models import UserProfile
from django.db.models import Q
from django_comments.models import Comment
from .models import Post, Vote, Favorite
from tags.models import Tag

languages = ['Language', 'English', 'Hindi', 'Telugu', 'Tamil', 'Kannada']

N_POSTS = settings.POSTS_PER_PAGE
MEDIA_URL = settings.MEDIA_URL


def votes_and_favorites(user):
    votes = Vote.objects.values_list('post', 'type').filter(user=user)
    upvotes = [vote[0] for vote in votes if vote[1] is True]
    downvotes = [vote[0] for vote in votes if vote[1] is False]
    favorites = Favorite.objects.values_list('post', flat=True).filter(user=user)
    return upvotes, downvotes, favorites


def home(request, lang=0):
    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if lang == 0:

        if 'lang' in request.COOKIES:
            lang = request.COOKIES['lang']
        else:
            lang = 1

    if not request_user.is_anonymous():
        post_list = cache.get('feed' + str(lang))
        if post_list is None:
            post_list = list(
                Post.objects.select_related('user').filter(Q(language1=lang) | Q(language2=lang), active=True))
            cache.set('feed' + str(lang), post_list, 60)
        upvotes, downvotes, favorites_list = votes_and_favorites(request_user)

    else:
        post_list = cache.get('feed' + str(lang))
        if post_list is None:
            post_list = list(
                Post.objects.select_related('user').filter(Q(language1=lang) | Q(language2=lang), active=True))
            cache.set('feed' + str(lang), post_list, 3 * 60)

    paginator = Paginator(post_list, N_POSTS)

    try:
        offset = int(request.GET.get('older', 1))
    except ValueError:
        offset = 1

    try:
        latest_items = paginator.page(offset)
    except PageNotAnInteger:
        latest_items = paginator.page(1)
    except EmptyPage:
        return HttpResponse(0)

    if request.is_ajax():
        return render_to_response('feed.html', {
            'media_url': MEDIA_URL, 'r_user': request_user, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1},
                                  RequestContext(request))

    else:
        response = render_to_response('home.html', {
            'media_url': MEDIA_URL, 'r_user': request_user, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1, 'lang': languages[int(lang)]},
                                      RequestContext(request))

        response.set_cookie('lang', lang)
        return response


def new(request):
    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1

    if not request_user.is_anonymous():
        post_list = cache.get('feed' + str(lang))
        if post_list is None:
            post_list = list(
                Post.objects.select_related('user').filter(Q(language1=lang) | Q(language2=lang), active=True).order_by(
                    '-created'))
            cache.set('new' + str(lang), post_list, 10)
        upvotes, downvotes, favorites_list = votes_and_favorites(request_user)

    else:
        post_list = cache.get('feed' + str(lang))
        if post_list is None:
            post_list = list(
                Post.objects.select_related('user').filter(Q(language1=lang) | Q(language2=lang), active=True).order_by(
                    '-created'))
            cache.set('new' + str(lang), post_list, 3 * 10)

    paginator = Paginator(post_list, N_POSTS)

    try:
        offset = int(request.GET.get('older', 1))
    except ValueError:
        offset = 1

    try:
        latest_items = paginator.page(offset)
    except PageNotAnInteger:
        latest_items = paginator.page(1)
    except EmptyPage:
        return HttpResponse(0)

    if request.is_ajax():
        return render_to_response('feed.html', {
            'media_url': MEDIA_URL, 'r_user': request_user, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1},
                                  RequestContext(request))

    else:
        response = render_to_response('home.html', {
            'media_url': MEDIA_URL, 'r_user': request_user, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1, 'lang': languages[int(lang)]},
                                      RequestContext(request))
        response.set_cookie('lang', lang)
        return response


def search(request):
    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1

    if 'q' in request.GET:
        q = request.GET['q']
    else:
        q = ''

    if not request.user.is_anonymous():
        upvotes, downvotes, favorites_list = votes_and_favorites(request_user)

    posts = Post.objects.all().filter(active=True, title__icontains=q).order_by('-upvotes')
    paginator = Paginator(posts, N_POSTS)

    try:
        users = User.objects.values_list('username', flat=True).filter(username__icontains=q)
        tags = Tag.objects.values_list('name', flat=True).filter(name__icontains=q)
    except:
        users = []
        tags = []

    try:
        offset = int(request.GET.get('older', 1))
    except ValueError:
        offset = 1

    try:
        latest_items = paginator.page(offset)
        empty = False
        if len(latest_items) == 0:
            empty = True
    except PageNotAnInteger:
        latest_items = paginator.page(1)
        if len(latest_items) == 0:
            empty = True
    except EmptyPage:
        empty = True

    if request.is_ajax():
        return render_to_response('feed.html', {
            'media_url': MEDIA_URL, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1},
                                  RequestContext(request))

    else:
        response = render_to_response('search/search.html', {
            'media_url': MEDIA_URL, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1,
            'lang': languages[int(lang)], 'empty': empty, 'tags': tags, 'users': users},
                                      RequestContext(request))
        response.set_cookie('lang', lang)
        return response



# def likes(request, username):
#     upvotes, downvotes, favorites_list = [], [], []
#     request_user = request.user  # The user who sent the request
#
#     if 'lang' in request.COOKIES:
#         lang = request.COOKIES['lang']
#     else:
#         lang = 1
#     if not request.user.is_anonymous():
#         upvotes, downvotes, favorites_list = votes_and_favorites(request_user)
#
#     user_param = User.objects.get(username=username)
#     profile = UserProfile.objects.get(user=user_param)
#     likes = Vote.objects.filter(user=user_param, type=True)
#     posts = [c.post for c in likes]
#     return render_to_response('profile.html', {
#         'profile': profile, 'posts': posts,
#         'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
#         'media_url': settings.MEDIA_URL,
#         'type': 3, 'lang': languages[int(lang)]},
#                               RequestContext(request))
#

def likes(request, username):

    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1

    user_param = User.objects.get(username=username)
    likes = Vote.objects.filter(user=user_param, type=True)
    post_list = [c.post for c in likes]
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
                                    'type': 3, 'lang': languages[int(lang)]},
                                    RequestContext(request))



#
# def favorites(request, username):
#     upvotes, downvotes, favorites_list = [], [], []
#     request_user = request.user  # The user who sent the request
#
#     if 'lang' in request.COOKIES:
#         lang = request.COOKIES['lang']
#     else:
#         lang = 1
#
#     if not request.user.is_anonymous():
#         upvotes, downvotes, favorites_list = votes_and_favorites(request_user)
#
#     user_param = User.objects.get(username=username)
#     profile = UserProfile.objects.get(user=user_param)
#
#     favorites = Favorite.objects.filter(user=user_param)
#     posts = [c.post for c in favorites]
#     return render_to_response('profile.html', {
#         'profile': profile, 'posts': posts,
#         'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
#         'media_url': settings.MEDIA_URL,
#         'type': 2, 'lang': languages[int(lang)]},
#                               RequestContext(request))
#

def favorites(request, username):

    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1

    user_param = User.objects.get(username=username)
    favorites = Favorite.objects.filter(user=user_param)
    post_list = [c.post for c in favorites]
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
                                    'type': 2, 'lang': languages[int(lang)]},
                                    RequestContext(request))



#
# def commented(request, username):
#     upvotes, downvotes, favorites_list = [], [], []
#     request_user = request.user  # The user who sent the request
#
#     if 'lang' in request.COOKIES:
#         lang = request.COOKIES['lang']
#     else:
#         lang = 1
#
#     if not request.user.is_anonymous():
#         upvotes, downvotes, favorites_list = votes_and_favorites(request_user)
#
#     user_param = User.objects.get(username=username)
#     profile = UserProfile.objects.get(user=user_param)
#     commented = Comment.objects.filter(user=user_param)
#     posts = [c.content_object for c in commented]
#     posts = set(posts)
#     return render_to_response('profile.html', {
#         'profile': profile, 'posts': posts,
#         'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
#         'media_url': settings.MEDIA_URL,
#         'type': 4, 'lang': languages[int(lang)]},
#                               RequestContext(request))



def commented(request, username):

    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1

    user_param = User.objects.get(username=username)
    commented = Comment.objects.filter(user=user_param)
    post_list = [c.content_object for c in commented]
    profile = UserProfile.objects.get(user=user_param)

    # following_posts = []
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
                                    'type': 4, 'lang': languages[int(lang)]},
                                    RequestContext(request))


def about(request):
    return render_to_response('about.html', RequestContext(request))

def contact(request):
    return render_to_response('contact.html', RequestContext(request))

def blog(request):
    return render_to_response('blog.html', RequestContext(request))



