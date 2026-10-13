from bs4 import BeautifulSoup
from pytest_shell.fs import create_files

TASKS_PY = """import voltaire

namespace = voltaire.site()
"""

PAGE_MD = """title: My Page
summary: A concise page summary.

This is my page.
"""

ARTICLE_MD = """title: My Article
date: 2026-01-02
summary: A concise article summary.

This is my article.
"""

PELICAN_CONF = """from voltaire.pelican import *
"""

SEO_PELICAN_CONF = """from voltaire.pelican import *

SITENAME = "Example Site"
SITEURL = "https://example.com/"
SITE_DESCRIPTION = "An example site description."
OPEN_GRAPH_IMAGE = "/images/social.jpg"
PAGE_PATHS = ["pages"]
TEMPLATE_PAGES = {"search.html": "search/index.html"}
"""


def test_single_page(shell, tmpdir):
    create_files(
        structure=[
            {"tasks.py": {"content": TASKS_PY}},
            {"pelicanconf.py": {"content": PELICAN_CONF}},
            {"content/page.md": {"content": PAGE_MD}},
        ],
        root=tmpdir,
    )

    result = shell.run("invoke", "build", cwd=tmpdir)
    pelican_output = result.stdout + result.stderr
    assert "ERROR" not in pelican_output
    assert "WARNING" not in pelican_output

    page_html = shell.run("cat", "output/page/index.html", cwd=tmpdir).stdout
    assert "<!DOCTYPE html>" in page_html
    assert "common.min.css" in page_html

    page = BeautifulSoup(page_html, "html.parser")
    assert (
        page.select_one('meta[name="description"]')["content"].replace(
            "\xa0", " "
        )
        == "A concise page summary."
    )
    assert page.select('meta[name="description"]') == [
        page.select_one('meta[name="description"]')
    ]
    assert page.select_one('link[rel="canonical"]') is None


def test_shared_seo_metadata(shell, tmpdir):
    create_files(
        structure=[
            {"tasks.py": {"content": TASKS_PY}},
            {"pelicanconf.py": {"content": SEO_PELICAN_CONF}},
            {"content/pages/page.md": {"content": PAGE_MD}},
            {"content/posts/article.md": {"content": ARTICLE_MD}},
            {"content/images/social.jpg": {"content": "placeholder"}},
        ],
        root=tmpdir,
    )

    result = shell.run("invoke", "build", cwd=tmpdir)
    pelican_output = result.stdout + result.stderr
    assert "ERROR" not in pelican_output

    expected = {
        "output/page/index.html": {
            "canonical": "https://example.com/page/",
            "description": "A concise page summary.",
            "og_type": "website",
        },
        "output/article/index.html": {
            "canonical": "https://example.com/article/",
            "description": "A concise article summary.",
            "og_type": "article",
        },
        "output/index.html": {
            "canonical": "https://example.com/",
            "description": "An example site description.",
            "og_type": "website",
        },
        "output/search/index.html": {
            "canonical": "https://example.com/search/",
            "description": "An example site description.",
            "og_type": "website",
        },
    }

    for path, metadata in expected.items():
        html = shell.run("cat", path, cwd=tmpdir).stdout
        document = BeautifulSoup(html, "html.parser")

        assert (
            document.select_one('link[rel="canonical"]')["href"]
            == metadata["canonical"]
        )
        assert document.select_one('meta[property="og:url"]')["content"] == (
            metadata["canonical"]
        )
        assert (
            document.select_one('meta[name="description"]')["content"].replace(
                "\xa0", " "
            )
            == metadata["description"]
        )
        assert (
            document.select_one('meta[property="og:description"]')[
                "content"
            ].replace("\xa0", " ")
            == metadata["description"]
        )
        assert document.select_one('meta[property="og:type"]')["content"] == (
            metadata["og_type"]
        )
        assert document.select_one('meta[property="og:image"]')["content"] == (
            "https://example.com/images/social.jpg"
        )
        assert len(document.select('meta[name="description"]')) == 1
        assert len(document.select('meta[property="og:description"]')) == 1

    search_html = shell.run(
        "cat", "output/search/index.html", cwd=tmpdir
    ).stdout
    search = BeautifulSoup(search_html, "html.parser")
    assert search.title.string == "Search | Example Site"
    assert search.select_one('meta[name="robots"]')["content"] == (
        "noindex, follow"
    )
