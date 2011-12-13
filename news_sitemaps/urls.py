from django.conf.urls.defaults import *

from news_sitemaps import registry


urlpatterns = patterns('news_sitemaps.views',
    url(r'^index\.xml$',
        'index',
        {'sitemaps': registry},
        name='news_sitemaps_index'),

    url(r'^(?P<section>.+)\.xml',
        'render_sitemap',
        {'sitemaps': registry},
        name='news_sitemaps_sitemap'),
)
