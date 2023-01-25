from doctrine import add_task
from invoke import Collection

from . import tasks

__ALL__ = ["site"]
TASKS = Collection("tasks")


def site(host="localhost", port=8000, domain=None):
    add_task(TASKS, tasks.build)
    add_task(TASKS, tasks.livereload, host=host, port=port)
    add_task(TASKS, tasks.publish, domain=domain)
    add_task(TASKS, tasks.stage, domain=domain)
    add_task(TASKS, tasks.verify, domain=domain)
    return TASKS
