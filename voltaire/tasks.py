# -*- coding: utf-8 -*-
import datetime
import os
from textwrap import dedent

from invoke import task
from pelican import main as pelican_main
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

SETTINGS_FILE_BASE = "pelicanconf.py"
SETTINGS = {}
SETTINGS.update(DEFAULT_CONFIG)
LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
SETTINGS.update(LOCAL_SETTINGS)


PUBLISH_FILE_BASE = "publishconf.py"
COMPOSE_YAML = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "docker-compose.verify.yml"
)


@task
def build(c):
    """Build local version of site"""
    pelican_main(["-s", SETTINGS_FILE_BASE])


@task
def publish(c, domain=None):
    """Build local version of site"""
    pelican_main(["-s", PUBLISH_FILE_BASE, "--output", "dist"])
    commit_message = "'Publish site on {}'".format(
        datetime.date.today().isoformat()
    )
    if domain:
        with open("dist/CNAME", "w") as f:
            f.write(domain)
        with open("dist/robots.txt", "w") as f:
            f.write(
                dedent(
                    f"""
                User-agent: *
                Disallow: /drafts/
                Sitemap: http://{domain}/sitemap.xml
            """
                )
            )
    c.run("ghp-import -b gh-pages " f"-m {commit_message} " "dist -p")


@task
def stage(c, domain=None):
    pelican_main(["-s", PUBLISH_FILE_BASE, "--output", "dist"])
    if domain:
        with open("dist/CNAME", "w") as f:
            f.write(domain)
        with open("dist/robots.txt", "w") as f:
            f.write(
                dedent(
                    f"""
                User-agent: *
                Disallow: /drafts/
                Sitemap: http://{domain}/sitemap.xml
            """
                )
            )
    c.run("docker run -v $PWD/dist:/usr/share/nginx/html -p 80:80 nginx")


@task
def verify(c, domain=None):
    pelican_main(["-s", PUBLISH_FILE_BASE, "--output", "dist"])
    if domain:
        with open("dist/CNAME", "w") as f:
            f.write(domain)
        with open("dist/robots.txt", "w") as f:
            f.write(
                dedent(
                    f"""
                User-agent: *
                Disallow: /drafts/
                Sitemap: http://{domain}/sitemap.xml
            """
                )
            )
    try:
        c.run(
            f"DOMAIN={domain} docker-compose -f {COMPOSE_YAML} up --build --abort-on-container-exit --exit-code-from verify --renew-anon-volumes"
        )
    finally:
        c.run(
            f"docker-compose -f {COMPOSE_YAML} down --rmi local --remove-orphans"
        )


@task
def livereload(c, host="localhost", port=8000):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    build(c)
    server = Server()
    # Watch the base settings file
    server.watch(SETTINGS_FILE_BASE, lambda: build(c))
    # Watch content source files
    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_blob = "{0}/**/*{1}".format(SETTINGS["PATH"], extension)
        server.watch(content_blob, lambda: build(c))
    # Watch the theme's templates and static assets
    theme_path = SETTINGS["THEME"]
    server.watch("{}/templates/*.html".format(theme_path), lambda: build(c))
    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file = "{0}/static/**/*{1}".format(theme_path, extension)
        server.watch(static_file, lambda: build(c))
    # Serve output path on configured host and port
    server.serve(host=host, port=port, root=SETTINGS["OUTPUT_PATH"])
