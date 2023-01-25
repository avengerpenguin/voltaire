from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="voltaire",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "voltaire/_version.py",
        "fallback_version": "0.0.0",
    },
    description="Tools for prolific writers (or more accurately, those that want to be).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    url="https://github.com/avengerpenguin/voltaire",
    packages=["voltaire"],
    include_package_data=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/avengerpenguin/voltaire/issues",
    },
    keywords=["pelican", "invoke"],
    install_requires=[
        "invoke",
        "pelican",
        "markdown",
        "pelican-webassets",
        "pelican-sitemap",
        "plantuml-markdown",
        "pyScss",
        "cssmin",
        "livereload",
        "ghp-import",
        "beautifulsoup4",
        "typogrify",
        "webassets",
        "sh",
        "doctrine",
    ],
    setup_requires=[
        "pytest-runner",
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-shell",
            "pytest-pikachu",
            "pytest-mypy",
            "xmldiff",
            "types-markdown",
        ],
    },
)
