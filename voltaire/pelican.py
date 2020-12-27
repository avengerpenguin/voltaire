import os

PATH = "content"
PAGE_PATHS = ["."]
ARTICLE_PATHS = ["posts"]
STATIC_PATHS = []

SLUGIFY_SOURCE = "basename"

PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

TIMEZONE = "Europe/London"

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None

PLUGINS = [
    "pelican_webassets",
    "voltaire.wikilinks",
]

THEME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "theme")
THEME_STATIC_PATHS = [
    os.path.join(THEME, "static"),
    os.path.join(os.getcwd(), "static"),
]

LOCAL_SCSS = os.path.join(os.getcwd(), "static", "css", "style.scss")
if not os.path.exists(LOCAL_SCSS):
    LOCAL_SCSS = False

MARKDOWN = {
    "extension_configs": {
        "voltaire.mermaid": {},
        "markdown.extensions.extra": {},
    },
    "output_format": "html5",
}

TYPOGRIFY = True
