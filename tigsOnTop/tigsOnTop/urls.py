from django.conf.urls import patterns, include, url
from rest_framework import routers

from gameTracker.viewsets import GameViewSet

router = routers.SimpleRouter()
router.register(r'games', GameViewSet)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gameTracker.views.home', name='home'),
    # url(r'^tigsOnTop/', include('tigsOnTop.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls, namespace='api:v1')),
)
