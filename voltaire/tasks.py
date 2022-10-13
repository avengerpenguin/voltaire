import datetime
import os
import threading
from textwrap import dedent

from invoke import task
from pelican import main as pelican_main
from pelican.settings import DEFAULT_CONFIG, get_settings_from_file

SETTINGS_FILE_BASE = "pelicanconf.py"


PUBLISH_FILE_BASE = "publishconf.py"
COMPOSE_YAML = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "docker-compose.verify.yml"
)
DOCKERFILE_VERIFY = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "Dockerfile.verify"
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
                    """
                User-agent: *
                Disallow: /drafts/
                Sitemap: /sitemap.xml
            """
                )
            )
    c.run("ghp-import -b gh-pages " f"-m {commit_message} " "dist -p -f")


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
def verify(c, domain=None, opengraph=False, disqus=False):
    """
    Run checks locally on candidate site to publish.
    """
    pelican_main(["-s", PUBLISH_FILE_BASE, "--output", "dist"])
    if domain:
        with open("dist/CNAME", "w") as f:
            f.write(domain)
        with open("dist/robots.txt", "w") as f:
            f.write(
                dedent(
                    """
                User-agent: *
                Disallow: /drafts/
                Sitemap: /sitemap.xml
            """
                )
            )

    weblint_options = f"--set=OPENGRAPH={opengraph} --set=DISQUS={disqus}"
    try:
        c.run(
            f"""
            export DOMAIN={domain}
            export WEBLINT_OPTS='{weblint_options}'
            export DOCKERFILE_VERIFY='{DOCKERFILE_VERIFY}'
            docker-compose -f {COMPOSE_YAML} up --build --abort-on-container-exit --exit-code-from verify --renew-anon-volumes
            """
        )
    finally:
        c.run(
            f"""
            export DOMAIN={domain}
            export WEBLINT_OPTS='{weblint_options}'
            export DOCKERFILE_VERIFY='{DOCKERFILE_VERIFY}'
            docker-compose -f {COMPOSE_YAML} down --rmi local --remove-orphans
            """
        )


@task
def livereload(
    c, host="localhost", port=8000, test=True, opengraph=False, disqus=False
):
    """Automatically reload browser tab upon file modification."""
    from livereload import Server

    SETTINGS = {}
    SETTINGS.update(DEFAULT_CONFIG)
    LOCAL_SETTINGS = get_settings_from_file(SETTINGS_FILE_BASE)
    SETTINGS.update(LOCAL_SETTINGS)

    def run_weblint():
        c.run(
            f"scrapy weblint --set=OPENGRAPH={opengraph} --set=DISQUS={disqus} http://{host}:{port}/ &"
        )

    def build_test():
        build(c)
        if test:
            threading.Thread(target=run_weblint).start()

    build(c)
    server = Server()
    # Watch the base settings file
    server.watch(SETTINGS_FILE_BASE, build_test)
    # Watch content source files
    content_file_extensions = [".md", ".rst"]
    for extension in content_file_extensions:
        content_blob = "{}/**/*{}".format(SETTINGS["PATH"], extension)
        server.watch(
            content_blob,
            build_test,
            ignore=lambda f: f.endswith("cv.md"),
        )
    # Watch the theme's templates and static assets
    theme_path = SETTINGS["THEME"]
    server.watch(f"{theme_path}/templates/*.html", build_test)
    static_file_extensions = [".css", ".js"]
    for extension in static_file_extensions:
        static_file = f"{theme_path}/static/**/*{extension}"
        server.watch(static_file, build_test)
    # Serve output path on configured host and port
    server.serve(host=host, port=port, root=SETTINGS["OUTPUT_PATH"])
