from setuptools import setup
from Cython.Build import cythonize
import numpy

# Setup for compiling traditional .pyx Cython file
setup(
    ext_modules=cythonize("bench_cy.pyx", language_level="3"),
    include_dirs=[numpy.get_include()],
)
