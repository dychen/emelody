from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from mysite.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', homepage),
    (r'^get_started/$', get_started),
    (r'^about/$', about),
    (r'^contact/$', contact),
    
    # Account creation and management
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout_view),
    (r'^accounts/register/$', register),
    (r'^accounts/register/success/$', registration_successful),
                       #(r'^accounts/', include('registration.urls')),
                       
    # User pages
    (r'^accounts/profile/$', profile),
                       #(r'^rate/(?P<song_id>\d+)/$', rate),
                       #(r'^rate/\d+/success/$', rate_successful),
    # Development URLs
    # Deployment URLs
    (r'^create_playlist/(?P<song_id>\d+)/$', create_playlist),
    (r'^create_playlist/\d+/success/$', create_playlist_successful),
    (r'^listen/(?P<playlist_id>\d+)/$', listen),
                       
    # Administration scripts.
    (r'^admin/updatedb/$', update_db),
                       
                       
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
