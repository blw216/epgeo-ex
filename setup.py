#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path

from setuptools import setup, find_packages

src_dir = path.abspath(path.dirname(__file__))

setup(use_scm_version=True, packages=find_packages())
