#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'hitsumabushi'
SITENAME = 'ひつまぶし食べたい'
SITEURL = 'https://www.hitsumabushi.org'
SITESUBTITLE = 'メモ代わりのブログ'

THEME = 'themes/Flex'
PATH = 'content'

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
SUMMARY_MAX_LENGTH = 150
DEFAULT_PAGINATION = 10

# Feed generation is usually not desired when developing
FEED_MAX_ITEMS = 10
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
        ('twitter', 'https://twitter.com/_hitsumabushi_'),
        ('github', 'https://github.com/hitsumabushi'),
        ('rss', 'feeds/all.atom.xml'),
        )

# もう古いのはいいか、ということで削除
#LINKS = (
#    ('Old blog', 'https://hitsumabushi-pc.blogspot.com/'),
#    )

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# These are optional settings
STATIC_PATHS = [
    'images', 'extra/robots.txt', 'extra/favicon.ico',
    'extra/CNAME', 'extra/icon.jpg', 'extra/profile.jpg','extra/custom.css',
    'extra/my.js',
    'extra/_well-known/nostr.json'
    ]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'static/favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
    'extra/icon.jpg': {'path': 'static/icon.jpg'},
    'extra/profile.jpg': {'path': 'static/profile.jpg'},
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/my.js': {'path': 'static/js/my.js'},
    'extra/_well-known/nostr.json': {'path': '.well-known/nostr.json'}
}
FAVICON = '/static/favicon.ico'

# For Adding search and sitemap
DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'archives', 'search', 'sitemap')
SITEMAP_SAVE_AS = 'sitemap.xml'

# Extentions
# See https://www.ainoniwa.net/pelican/2020/0830a.html
# See https://qiita.com/5t111111/items/d745af778969bf00f038
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.fenced_code': {},
        'markdown.extensions.nl2br': {},
        'markdown.extensions.tables': {},
        'markdown.extensions.admonition': {},
        #'mdx_linkify.mdx_linkify': {},
        #'markdown.extensions.toc': {},
        'toc': {}, # use extract_toc
    },
    'output_format': 'html5',
}

# Plugins
PLUGIN_PATHS = ['plugins/pelican-plugins']
PLUGINS = [
        'sitemap',
        'related_posts',
        'render_math',
        'tipue_search',
        'neighbors',
        'pelican_gist',
        'extract_toc',
        ]


# Plugin Settings
## sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 1.0,
        'pages': 1.0
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'weekly'
    }
}
## related_posts
RELATED_POSTS_MAX = 5

#---
# Flex Theme settings
#---
COPYRIGHT_NAME = AUTHOR
COPYRIGHT_YEAR = 2021
# 上部のメニュー表示
MAIN_MENU = True
MENUITEMS = (
    ("Archives", "/archives.html"),
)
# アイコン画像
SITELOGO = "/static/profile.jpg"
# コードハイライト指定
PYGMENTS_STYLE = "monokai"
# Analytics
GOOGLE_GLOBAL_SITE_TAG = 'G-JPYFS3RY30' # Your Google Analytics 4 Property ID
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-nc",
    "language": "ja"
}
