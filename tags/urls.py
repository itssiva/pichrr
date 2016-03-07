from django.conf.urls import include, url, patterns
import tags
# Myghtyboard URLs
urlpatterns = patterns('tags.views',
    url(r'(?P<tag>\w+)/$', 'tag_search', name="tag_search"),
)
