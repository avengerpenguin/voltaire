from invoke import Collection, Task, task

from . import tasks

__ALL__ = ["site"]
TASKS = Collection("tasks")


def add_task(t: Task, **project_args):
    @task(name=t.name, optional=t.optional)
    def wrapped_task(c, **task_args):
        return t(c, **project_args, **task_args)

    wrapped_task.__doc__ = t.__doc__
    TASKS.add_task(wrapped_task, name=t.__name__)


def site(host="localhost", port=8000, domain=None):
    add_task(tasks.build)
    add_task(tasks.livereload, host=host, port=port)
    add_task(tasks.publish, domain=domain)
    add_task(tasks.stage, domain=domain)
    add_task(tasks.verify, domain=domain)
    return TASKS
