import os

from pytest_shell.fs import create_files
from pytest_shell.shell import LocalBashSession

TASKS_PY = """import voltaire

namespace = voltaire.site()
"""

PAGE_MD = """title: My Page

This is my page.
"""

PELICAN_CONF = """from voltaire.pelican import *
"""


def test_single_page(bash: LocalBashSession, tmpdir):
    create_files(
        structure=[
            {"tasks.py": {"content": TASKS_PY}},
            {"pelicanconf.py": {"content": PELICAN_CONF}},
            {"content/page.md": {"content": PAGE_MD}},
        ],
        root=tmpdir,
    )

    with bash(pwd=str(tmpdir), envvars={"PYTHONPATH": os.getcwd()}):
        pelican_output = bash.run_script("invoke", args=["build"])
        assert "ERROR" not in pelican_output
        assert "WARNING" not in pelican_output

        page_html = bash.run_script("cat", args=["output/page/index.html"])
        assert "<!DOCTYPE html>" in page_html
        assert "common.min.css" in page_html
