#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'hitsumabushi'
SITENAME = 'ひつまぶし食べたい'
SITEURL = 'http://www.hitsumabushi.org/blog'

#THEME = 'themes/tuxlite_tbs'
#THEME = 'themes/gum'
THEME = 'themes/pelican-bootstrap3'
PATH = 'content'
# These are optional settings
STATIC_PATHS = ['images']
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}{date:%d}_{date:%H%M}.html'
ARTICLE_URL = '{date:%Y}/{date:%m}{date:%d}_{date:%H%M}.html'
#ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
#ARTICLE_URL = '{date:%Y}/{slug}.html'


TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = 'ja'
DEFAULT_PAGINATION = 10
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True

# Feed generation is usually not desired when developing
FEED_MAX_ITEMS = 10
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Tag cloud
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100

GOOGLE_ANALYTICS = 'UA-24727901-9'
DISQUS_SITENAME = "hitsumabushi"

GITHUB_URL = 'https://github.com/hitsumabushi/blog/tree/gh-pages'
TWITTER_USERNAME = '__hitsumabushi__'
TWITTER_CARDS = True

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/_hitsumabushi_'),
        ('Github', 'https://github.com/hitsumabushi'),)

# Blogroll
LINKS = (('Old my blog', 'http://blog.hitsumabushi.org/'),
        ('Old my blog2',
            'http://hitsumabushi-pc.blogspot.jp/2011/07/blogger.html'),
         )


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Default Settings
DEFAULT_CATEGORY = 'blog'

# Extentions
# See http://qiita.com/5t111111/items/d745af778969bf00f038
MD_EXTENSIONS = [
    'fenced_code', 'codehilite(css_class=highlight)', 'tables',
    'extra', 'nl2br', 'toc']


