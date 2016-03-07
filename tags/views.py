from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.conf import settings

from .models import Tag
from post.display import votes_and_favorites

# Create your views here.
N_POSTS = settings.POSTS_PER_PAGE

languages = ['Language', 'English', 'Hindi', 'Telugu', 'Tamil', 'Kannada']


# def tag_search(request, tag):
#     upvotes, downvotes, favorites_list = [], [], []
#     request_user = request.user  # The user who sent the request
#
#     if 'lang' in request.COOKIES:
#         lang = request.COOKIES['lang']
#     else:
#         lang = 1
#
#     tag = get_object_or_404(Tag, name=tag)
#     context = RequestContext(request)
#     posts = tag.post_set.all().order_by("-created")
#     paginator = Paginator(posts, N_POSTS)
#     profile = []
#     if not request.user.is_anonymous():
#         upvotes, downvotes, favorites_list = votes_and_favorites(request_user)
#
#     try:
#         offset = int(request.GET.get('older', 1))
#     except ValueError:
#         offset = 1
#
#     try:
#         latest_items = paginator.page(offset)
#     except PageNotAnInteger:
#         latest_items = paginator.page(1)
#     except EmptyPage:
#         return HttpResponse(0)
#
#     if request.is_ajax():
#         return render_to_response('feed.html',
#                                   {'media_url': settings.MEDIA_URL, 'profile': profile, 'posts': latest_items,
#                                    'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
#                                    'offset': latest_items.number + 1},
#                                     context)
#
#     else:
#         return render_to_response('home.html', {'profile': profile, 'posts': latest_items,
#                                                 'offset': latest_items.number + 1,
#                                                 'media_url': settings.MEDIA_URL, 'lang': languages[int(lang)]},
#                                   context)
#

def tag_search(request, tag):
    upvotes, downvotes, favorites_list = [], [], []
    request_user = request.user  # The user who sent the request

    if 'lang' in request.COOKIES:
        lang = request.COOKIES['lang']
    else:
        lang = 1
    tag = get_object_or_404(Tag, name=tag)
    if not request.user.is_anonymous():
        upvotes, downvotes, favorites_list = votes_and_favorites(request_user)

    posts = tag.post_set.all().order_by("-created")
    paginator = Paginator(posts, N_POSTS)

    try:
        offset = int(request.GET.get('older', 1))
    except ValueError:
        offset = 1

    try:
        latest_items = paginator.page(offset)
        print "Inside Page"
    except PageNotAnInteger:
        print "Inside Page not an Integer Page"
        latest_items = paginator.page(1)
    except EmptyPage:
        print "Inside Empty Page"
        return HttpResponse(0)

    if request.is_ajax():
        return render_to_response('feed.html', {
            'media_url': settings.MEDIA_URL, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1},
                                  RequestContext(request))

    else:
        response = render_to_response('home.html', {
            'media_url': settings.MEDIA_URL, 'posts': latest_items,
            'upvotes': upvotes, 'downvotes': downvotes, 'favorites': favorites_list,
            'offset': latest_items.number + 1,
            'lang': languages[int(lang)],},
                                      RequestContext(request))
        response.set_cookie('lang', lang)
        return response
