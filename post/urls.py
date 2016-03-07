from django.conf.urls import  url, patterns
from . import api
urlpatterns = patterns('post.views',
		url(r'^post/$', 'post', name='post'),
        url(r'^rules/$', 'rules', name='rules'),

        url(r'^view_post/(?P<id>\w+)/$', 'view_post', name='view_post'),
        url(r'^delete_post/(?P<id>\w+)/$', 'delete_post', name='delete_post'),
        url(r'^like/(?P<id>\w+)/$', 'upvote', name='like'),
        url(r'^dislike/(?P<id>\w+)/$', 'downvote', name='dislike'),
        url(r'^favorite/(?P<id>\w+)/$', 'favorite', name='favorite'),
        url(r'^report/(?P<id>\w+)/$', 'report', name='report'),
        # url(r'^api/$', api.PostList.as_view()),
        # url(r'^api/post/(?P<pk>[a-zA-Z0-9]+)/$', api.PostDetail.as_view()),
        # url(r'^api/likes/$', api.LikeList.as_view()),
        # url(r'^api/favorites/$', api.FavoriteList.as_view()),
	)

urlpatterns += patterns('post.display',
        url(r'^$', 'home', name='home'),
        url(r'^new/$', 'new', name='new'),
        url(r'^(?P<lang>\d+)/$', 'home', name='home_lang'),
        url(r'^search/$', 'search', name='search'),
        url(r'^favorites/(?P<username>\w+)/$', 'favorites', name='favorites'),
        url(r'^likes/(?P<username>\w+)/$', 'likes', name='liked'),
        url(r'^commented/(?P<username>\w+)/$', 'commented', name='commented'),
        url(r'^about/$', 'about', name='about'),
        url(r'^contact/$', 'contact', name='contact'),
        url(r'^blog/$', 'blog', name='blog'),
)