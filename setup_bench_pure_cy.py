from setuptools import setup, Extension
from Cython.Build import cythonize

# Setup for compiling pure Python mode Cython (.py file)
extensions = [
    Extension(
        "bench_pure_cy",
        ["bench_pure_cy.py"],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
        },
        annotate=True
    )
)
