import re
from typing import Match

from pelican import signals
from pelican.contents import Content
from pelican.utils import slugify

SETTINGS_NAME = "WIKILINKS"


def replace_wikilinks(text: str) -> str:
    def repl(group: Match):
        href, text = group.groups()
        if not text:
            text = href
        href = slugify(
            href,
            regex_subs=[
                (
                    r"[^\w\s-]",
                    "",
                ),  # remove non-alphabetical/whitespace/'-' chars
                (r"(?u)\A\s*", ""),  # strip leading whitespace
                (r"(?u)\s*\Z", ""),  # strip trailing whitespace
                (
                    r"[-\s]+",
                    "-",
                ),  # reduce multiple whitespace or '-' to single '-'
            ],
        )
        return f'<a href="/{href}/">{text}</a>'

    if text:
        return re.sub(r"\[\[([^|\]]+)\|?(.*?)\]\]", repl, text)
    else:
        return text


def content_object_init(instance: Content):
    instance._content = replace_wikilinks(instance._content)


def register():
    signals.content_object_init.connect(content_object_init)
