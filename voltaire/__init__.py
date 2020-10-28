from . import tasks
from invoke import Collection


def site():
    c = Collection("tasks")
    c.add_task(tasks.build)
    return c


__ALL__ = ["site"]
