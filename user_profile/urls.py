from django.conf.urls import include, url, patterns

urlpatterns = patterns('user_profile.views',
		url('^update_profile/$', 'update_profile', name='update_profile'),
		url(r'^profile/(?P<username>[0-9A-Za-z_\-]+)/$', 'profile', name='profile'),
		# url(r'^follow/(?P<username>[0-9A-Za-z_\-]+)/$', 'follow', name='follow'),
		# url(r'^followers/(?P<username>[0-9A-Za-z_\-]+)/$', 'followers', name='followers'),
        # url(r'^following/(?P<username>[0-9A-Za-z_\-]+)/$', 'following', name='following'),
		url(r'^delete_account/$', 'delete_account', name='delete_account'),
	)