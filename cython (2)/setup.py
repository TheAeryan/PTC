#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:10:11 2019

@author: jose
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("ejemplosCython.pyx"),
)
