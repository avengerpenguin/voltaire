from invoke import task


@task
def docs(c):
    c.run("sphinx-autobuild -v -b html ./docs _build")


@task
def build_docs(c):
    c.run("sphinx-build -b html ./docs _build")
