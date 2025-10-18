from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("parallel_cy.pyx", language_level="3", annotate=True)
)
