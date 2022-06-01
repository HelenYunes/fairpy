from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("cy_undercut.pyx")
)

# python setup.py build_ext --inplace