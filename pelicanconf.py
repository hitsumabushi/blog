#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'hitsumabushi'
SITENAME = 'ひつまぶし食べたい'
SITEURL = 'https://www.hitsumabushi.org'

THEME = 'themes/pelican-bootstrap3'
PATH = 'content'

# Content Lisence
CC_LICENSE = "CC-BY-NC"

# TIMEZONE
TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = 'ja'

# Setting article URLs
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{date:%H%M}.html'
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{date:%H%M}.html'
# Default Settings
DEFAULT_CATEGORY = 'blog'

# Custom CSS
CUSTOM_CSS = 'static/custom.css'

# Top page summary
DISPLAY_ARTICLE_INFO_ON_INDEX = True
SUMMARY_MAX_LENGTH = 25
DEFAULT_PAGINATION = 10

# Feed generation is usually not desired when developing
FEED_MAX_ITEMS = 10
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Sidebar
## Recent post
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 5

# Social
GITHUB_URL = 'https://github.com/hitsumabushi/blog/tree/gh-pages'
TWITTER_USERNAME = '__hitsumabushi__'
TWITTER_WIDGET_ID = '564098693729492992'
TWITTER_CARDS = True
USE_OPEN_GRAPH = True
OPEN_GRAPH_IMAGE = 'static/icon.jpg'

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/_hitsumabushi_'),
        ('Github', 'https://github.com/hitsumabushi'),)

# Blogroll
LINKS = (
    ('Old blog', 'http://hitsumabushi-pc.blogspot.jp/2011/07/blogger.html'),
    )

# External Services
GOOGLE_ANALYTICS_UNIVERSAL = 'UA-24727901-9'
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'auto'
DISQUS_SITENAME = "hitsumabushi"
GOOGLE_SITE_SEARCH = '009966809170133509931:4vsx-mk1ktu'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# These are optional settings
STATIC_PATHS = [
    'images', 'extra/robots.txt', 'extra/favicon.ico',
    'extra/CNAME', 'extra/icon.jpg', 'extra/custom.css',
    'extra/my.js'
    ]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'static/favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/icon.jpg': {'path': 'static/icon.jpg'},
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/my.js': {'path': 'static/js/my.js'}
}
FAVICON = 'static/favicon.ico'

# For Adding Sitemap
# default value is ('index', 'tags', 'categories', 'archives')
DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'archives', 'sitemap')
SITEMAP_SAVE_AS = 'sitemap.xml'

# Extentions
# See http://qiita.com/5t111111/items/d745af778969bf00f038
MD_EXTENSIONS = [
    'fenced_code', 'codehilite(css_class=highlight)', 'tables',
    'extra', 'nl2br', 'toc']

# Plugins
PLUGIN_PATHS = ['plugins/pelican-plugins']
PLUGINS = ['sitemap',
           'related_posts',
           'tag_cloud',
           'render_math',
           'pelican_gist']

BOOTSTRAP_FLUID = True
# Plugin Settings
## sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}
## related_posts
RELATED_POSTS_MAX = 5
## Tag cloud
DISPLAY_TAGS_ON_SIDEBAR = True
TAG_CLOUD_STEPS = 3
TAG_CLOUD_MAX_ITEMS = 30
TAG_CLOUD_SORTING = 'random'
DISPLAY_TAGS_INLINE = 'inline'
