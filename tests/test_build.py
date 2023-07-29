from pytest_shell.fs import create_files

TASKS_PY = """import voltaire

namespace = voltaire.site()
"""

PAGE_MD = """title: My Page

This is my page.
"""

PELICAN_CONF = """from voltaire.pelican import *
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
