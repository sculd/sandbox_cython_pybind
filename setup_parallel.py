from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "parallel_cy",
        ["parallel_cy.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp']
    )
]

setup(
    ext_modules=cythonize(extensions, language_level="3", annotate=True)
)
