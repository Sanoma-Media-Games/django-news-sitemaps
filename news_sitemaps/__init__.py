from django.conf import settings
from sitemaps import NewsSitemap, VideoSitemap, Sitemap

registry = {}

def register(**kwargs):
    for name,sitemap in kwargs.items():
        registry[name] = sitemap
