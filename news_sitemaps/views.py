from django.http import HttpResponse, Http404
from django.contrib.sites.models import Site
from django.core import urlresolvers
from django.template import loader
from django.utils.encoding import smart_str
from django.shortcuts import render_to_response
from django.core.paginator import EmptyPage, PageNotAnInteger

from settings import LANG, NAME, TZ


def index(request, sitemaps):
    """
    View to create a sitemap index listing other sitemaps
    """
    current_site = Site.objects.get_current()
    sites = []
    protocol = request.is_secure() and 'https' or 'http'
    for section, site in sitemaps.items():
        if callable(site):
            pages = site().paginator.num_pages
        else:
            pages = site.paginator.num_pages
        sitemap_url = urlresolvers.reverse('news_sitemaps_sitemap', kwargs={'section': section})
        sites.append('%s://%s%s' % (protocol, current_site.domain, sitemap_url))
        if pages > 1:
            for page in range(2, pages+1):
                sites.append('%s://%s%s?p=%s' % (protocol, current_site.domain, sitemap_url, page))
    xml = loader.render_to_string('sitemaps/index.xml', {'sitemaps': sites})
    return HttpResponse(xml, mimetype='application/xml')


def render_sitemap(request, sitemaps, section=None):
    """
    A view for creating Google News or Video Sitemaps
    Optional section will filter down to just the passed section name
    """
    maps, urls, output = [], [], []
    if section is not None:
        if section not in sitemaps:
            raise Http404('No sitemap available for section: %r' % section)
        maps.append(sitemaps[section])
    else:
        maps = sitemaps.values()
    page = request.GET.get('p', 1)
    for site in maps:
        try:
            if callable(site):
                urls.extend(site().get_urls(page))
            else:
                urls.extend(site.get_urls(page))
        except EmptyPage:
            raise Http404('Page %s empty' % page)
        except PageNotAnInteger:
            raise Http404('No page "%s"' % page)

        output.append(site.render(
            **{
                'urlset': urls,
                'publication_name': NAME,
                'publication_lang': LANG,
                'publication_tz': TZ
            }
        ))

    return render_to_response(
        'sitemaps/header.xml',
        {
            'output': output
        },
        mimetype='application/xml'
    )
