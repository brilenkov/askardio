from django.conf.urls.i18n import i18n_patterns
from django.conf import settings


from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.contrib import admin
from bookmarks.views import *
import os
site_media = os.path.join(os.path.dirname(__file__), 'site_media')

admin.autodiscover()


urlpatterns = patterns('',
  # Example:
  # (r'^django_bookmarks/',
      #include('django_bookmarks.foo.urls')),
      
      # Browsing
      (r'^$', main_page),
      (r'^user/(\w+)/$', user_page),
      
      # Session management
      (r'^login/$', 'django.contrib.auth.views.login'),
      (r'^logout/$', logout_page),
      (r'^register/$', register_page),
      (r'^register/success/$', direct_to_template,
        {'template': 'registration/register_success.html'}),
      
      # Account management
      (r'^save/$', bookmark_save_page),
      
      # Site media
      (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': site_media}),
  
      # Uncomment this for admin:
      url(r'^admin/', include(admin.site.urls)),
      
      (r'^tag/([^\s]+)/$', tag_page),
      (r'^tag/$', tag_cloud_page),
      (r'^search/$', search_page),
)