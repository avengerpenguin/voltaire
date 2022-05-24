import os
from pathlib import Path
from typing import List, Optional

PATH = "content"
PAGE_PATHS = ["."]
ARTICLE_PATHS = ["posts"]
STATIC_PATHS: List[str] = []

SLUGIFY_SOURCE = "basename"

PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
ARTICLE_URL = "{slug}/"
ARTICLE_SAVE_AS = "{slug}/index.html"

TIMEZONE = "Europe/London"

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None

PLUGINS = [
    "pelican.plugins.webassets",
    "pelican.plugins.sitemap",
    "voltaire.stats",
    "voltaire.wikilinks",
]
SITEMAP = {
    "format": "xml",
    "exclude": ["search/"],
}

THEME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "theme")
THEME_STATIC_PATHS = [
    os.path.join(THEME, "static"),
    os.path.join(os.getcwd(), "static"),
]

# LOCAL_SCSS: Optional[str] = os.path.join(os.getcwd(), "static", "css", "style.scss")
LOCAL_SCSS: Optional[str] = None
path: Path = Path.cwd() / "static" / "css" / "style.scss"
if path.exists():
    LOCAL_SCSS = str(path)

MARKDOWN = {
    "extension_configs": {
        "voltaire.mermaid": {},
        "plantuml_markdown": {},
        "markdown.extensions.extra": {},
        "markdown.extensions.toc": {},
    },
    "output_format": "html5",
}

TYPOGRIFY = True
