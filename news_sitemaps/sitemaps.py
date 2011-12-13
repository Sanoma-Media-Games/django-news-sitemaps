import datetime

from django.contrib.sitemaps import Sitemap as DjangoSitemap
from django.shortcuts import render_to_response
from django.template import loader, Context


class Sitemap(DjangoSitemap):
    @classmethod
    def render(cls, urlset, *args, **kwargs):
        """Render sitemap, excluding the header.

        Options are::

            * template: Template to render
            * urlset: List of items containing the sitemap data
        """
        tmpl = loader.get_template(cls.template)
        context = kwargs
        context.update({
            'urlset': urlset
        })
        return tmpl.render(Context(context))

    def get_urls(self, page=1):
        from django.contrib.sites.models import Site
        domain = Site.objects.get_current().domain
        get = self._Sitemap__get

        for item in self.paginator.page(page).object_list:
            lastmod = get('lastmod', item, None)
            if isinstance(lastmod, datetime.time) or isinstance(lastmod, datetime.datetime):
                lastmod = lastmod.replace(microsecond=0)

            yield item, {
                'location':     "http://%s%s" % (domain, get('location', item)),
                'lastmod':      lastmod,
                'changefreq':   get('changefreq', item, None),
                'priority':     get('priority', item, None),
            }

    def title(self, obj):
        """
        Returns the title of the news article.
        Note: The title may be truncated for space reasons when shown on Google News.
        """
        if hasattr(obj, 'title'):
            return obj.title
        elif hasattr(obj, 'name'):
            return obj.name
        elif hasattr(obj, 'headline'):
            return obj.headline

    def keywords(self, obj):
        """
        Returns a comma-separated list of keywords describing the topic of the
        content item.

        For Google News sitemaps::

          * Keywords may be drawn from, but are not limited to, the list of existing Google News keywords.
        """
        if hasattr(obj, 'keywords'):
            return obj.keywords
        elif hasattr(obj, 'tags'):
            return obj.tags


class NewsSitemap(Sitemap):
    template =  'sitemaps/news_sitemap.xml'

    def genres(self, obj):
        """
        Returns a comma-separated list of properties characterizing the content of the article,
        such as "PressRelease" or "UserGenerated." Your content must be labeled accurately,
        in order to provide a consistent experience for our users.

        Options are::

            * PressRelease (default, visible): an official press release.
            * Satire (visible): an article which ridicules its subject for didactic purposes.
            * Blog (visible): any article published on a blog, or in a blog format.
            * OpEd: an opinion-based article which comes specifically from the Op-Ed section of your site.
            * Opinion: any other opinion-based article not appearing on an Op-Ed page, i.e., reviews, interviews, etc.
            * UserGenerated: newsworthy user-generated content which has already gone through a formal editorial review process on your site.
        """
        return 'PressRelease'


    def access(self, obj):
        """
        Returns description of the accessibility of the article.
        If the article is accessible to Google News readers without a registration or subscription,
        this function should return None

        Options are::

            * Subscription (visible): an article which prompts users to pay to view content.
            * Registration (visible): an article which prompts users to sign up for an unpaid account to view content.
        """

    def stock_tickers(self, obj):
        """
        Returns a comma-separated list of up to 5 stock tickers of the companies,
        mutual funds, or other financial entities that are the main subject of the article.
        Relevant primarily for business articles.
        Each ticker must be prefixed by the name of its stock exchange,
        and must match its entry in Google Finance.
        For example, "NASDAQ:AMAT" (but not "NASD:AMAT"), or "BOM:500325" (but not "BOM:RIL").
        """


    def get_urls(self, page=1):
        get = self._Sitemap__get

        for item, attrs in super(NewsSitemap, self).get_urls(page):
            attrs.update({
                # News attrs
                'title':        get('title', item, None),
                'access':       get('access', item, None),
                'keywords':     get('keywords', item, None),
                'genres':       get('genres', item, None),
                'stock_tickers':get('stock_tickers', item, None),
            })
            yield attrs


class VideoSitemap(Sitemap):
    template =  'sitemaps/video_sitemap.xml'

    def get_urls(self, page=1):
        get = self._Sitemap__get

        for item, attrs in super(VideoSitemap, self).get_urls(page):
            attrs.update({
                # Video attrs
                'title':        get('title', item, None),
                'description':  get('description', item, None),
                'keywords':     get('keywords', item, None),
                'genres':       get('genres', item, None),
                'thumbnail_loc':get('thumbnail_loc', item, None),
                'content_loc':  get('content_loc', item, None),
                'player_loc':  get('player_loc', item, None),
                'publication_date':  get('publication_date', item, None),
                'duration':  get('duration', item, None),
            })
            yield attrs

    def categories(self, obj):
        """ The video's category. For example, cooking. The value should be a string no longer than 256 characters. In general, categories are broad groupings of content by subject. Usually a video will belong to a single category. For example, a site about cooking could have categories for Broiling, Baking, and Grilling.
        """
        return getattr(obj, 'categories', [])

    def player_loc(self, obj):
        """At least one of <video:player_loc> or <video:content_loc> is required. A URL pointing to a Flash player for a specific video. In general, this is the information in the src element of an <embed> tag and should not be the same as the content of the <loc> tag. Since each video is uniquely identified by its content URL (the location of the actual video file) or, if a content URL is not present, a player URL (a URL pointing to a player for the video), you must include either the <video:player_loc> or <video:content_loc> tags. If these tags are omitted and we can't find this information, we'll be unable to index your video.

        The optional attribute allow_embed specifies whether Google can embed the video in search results. Allowed values are Yes or No.

        The optional attribute autoplay has a user-defined string (in the example above, ap=1) that Google may append (if appropriate) to the flashvars parameter to enable autoplay of the video. For example: <embed src="http://www.example.com/videoplayer.swf?video=123" autoplay="ap=1"/>.

        Example:

        Dailymotion: http://www.dailymotion.com/swf/x1o2g
        """
        return None

    def content_loc(self, obj):
        """ You must specify at least one of <video:player_loc> or <video:content_loc>. The URL should point to a .mpg, .mpeg, .mp4, .m4v, .mov, .wmv, .asf, .avi, .ra, .ram, .rm, .flv, or other video file format, and can be omitted if <video:player_loc> is specified. However, because Google needs to be able to check that the Flash object is actually a player for video (as opposed to some other use of Flash, e.g. games and animations), it's helpful to provide both.
        """
        return None
