from . import tasks
from invoke import Collection, task


__ALL__ = ["site"]
TASKS = Collection("tasks")


def add_task(t, **project_args):
    @task(name=t.name, optional=t.optional)
    def wrapped_task(c, **task_args):
        return t(c, **project_args, **task_args)

    wrapped_task.__doc__ = t.__doc__
    TASKS.add_task(wrapped_task, name=t.__name__)


def site(host="localhost", port=8000, domain=None):
    add_task(tasks.build)
    add_task(tasks.livereload, host=host, port=port)
    add_task(tasks.publish, domain=domain)
    return TASKS
