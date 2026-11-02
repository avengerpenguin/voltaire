import os
from pathlib import Path

PATH = "content"
PAGE_PATHS = ["."]
ARTICLE_PATHS = ["posts"]
STATIC_PATHS: list[str] = []

SLUGIFY_SOURCE = "basename"

PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
ARTICLE_URL = "{slug}/"
ARTICLE_SAVE_AS = "{slug}/index.html"

TIMEZONE = "Europe/London"

# Shared metadata defaults. Sites can set these to provide a concise fallback
# description and a default social-sharing image. OPEN_GRAPH_IMAGE may be an
# absolute URL, a root-relative path, or a path relative to SITEURL.
SITE_DESCRIPTION: str | None = None
OPEN_GRAPH_IMAGE: str | None = None

# Google Analytics 4. GOOGLE_TAG_ID remains supported as a legacy alias.
GA4_MEASUREMENT_ID: str | None = None
AFFILIATE_RULES: list[dict[str, str]] = []
# Enable when a certified IAB TCF CMP supplies consent choices. This sets
# denied regional defaults before Google tags load and enables Google's TCF
# integration; it does not itself provide a consent banner or CMP.
GOOGLE_TCF_CONSENT_MODE = False

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
WEBASSETS_CONFIG = [
    ("SASS_LOAD_PATHS", [str(Path.cwd() / "node_modules")]),
    ("SASS_BIN", str(Path.cwd() / "node_modules" / ".bin" / "sass")),
    ("SASS_USE_SCSS", True),
]

# LOCAL_SCSS: Optional[str] = os.path.join(os.getcwd(), "static", "css", "style.scss")
LOCAL_SCSS: str | None = None
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
