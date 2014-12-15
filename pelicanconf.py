#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'hitsumabushi'
SITENAME = 'ひつまぶし食べたい'
SITEURL = 'http://www.hitsumabushi.org/blog'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'
DEFAULT_LANG = 'ja'
DEFAULT_PAGINATION = 10

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

GITHUB_URL = 'https://github.com/hitsumabushi/blog/tree/gh-pages'
GOOGLE_ANALYTICS = 'UA-24727901-9'

# Blogroll
LINKS = (('Old my blog', 'http://blog.hitsumabushi.org/'),
        ('Old my blog2',
            'http://hitsumabushi-pc.blogspot.jp/2011/07/blogger.html'),
         )

TWITTER_USERNAME = '__hitsumabushi__'
# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/_hitsumabushi_'),
        ('Github', 'https://github.com/hitsumabushi'),)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Default Settings
DEFAULT_CATEGORY = 'misc'

