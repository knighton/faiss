from distutils.command.install import install as DistutilsInstall
from distutils.sysconfig import get_python_inc
import numpy
import os
from setuptools import setup


def find_openblas_so(root_dir):
    for parent, dirs, files in os.walk(root_dir):
        for f in files:
            if f == 'libopenblas.so.0':
                return os.path.join(root_dir, parent, f)


def fill_in_vars():
    numpy_include = numpy.get_include()
    openblas_so = find_openblas_so('/usr')
    python_include = get_python_inc()
    d = {
        'numpy_include': numpy_include,
        'openblas_so': openblas_so,
        'python_include': python_include,
    }
    text = open('makefile.inc.template').read()
    text = text.format(**d)
    open('makefile.inc', 'wb').write(text.encode('utf-8'))


class MyInstall(DistutilsInstall):
    def run(self):
        fill_in_vars()
        os.system('make -j')
        os.system('make -j py')
        os.system('mkdir -p faiss')
        os.system('mv *.py *.so faiss/')
        os.system('cp faiss/faiss.py .')
        os.system('mv faiss/setup.py .')
        open('faiss/__init__.py', 'w').write('from .faiss import *\n')
        text = open('faiss/faiss.py').read()
        text = text.replace('swigfaiss', '.swigfaiss')
        open('faiss/faiss.py', 'w').write(text)
        DistutilsInstall.run(self)


setup(
    name='faiss',
    version='0.0.1',
    cmdclass={
        'install': MyInstall,
    },
)
