# -*- coding: utf-8 -*-
from invoke import task
from pelican import main as pelican_main


@task
def build(c):
    """Build local version of site"""
    pelican_main("-s pelicanconf.py".split())
