from django.conf import settings
from sitemaps import NewsSitemap, VideoSitemap

registry = {}

def register(**kwargs):
    for name,sitemap in kwargs.items():
        registry[name] = sitemap
