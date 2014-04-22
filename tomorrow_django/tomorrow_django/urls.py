from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login
admin.autodiscover()

from oil_and_gas import views as oil_and_gas_views
from oil_and_gas.urls import oil_and_gas_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tomorrow_django.views.home', name='home'),
    # url(r'^tomorrow_django/', include('tomorrow_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^login/?$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/$', oil_and_gas_views.api_root),
    url(r'^api/', include(oil_and_gas_urlpatterns)),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', oil_and_gas_views.oil_and_gas_base, name="tomorrow-base"),
)

if settings.DEBUG:
    urlpatterns = patterns(
        '',
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}
        ),
        url(
            r'',
            include('django.contrib.staticfiles.urls')
        ),
    ) + urlpatterns
