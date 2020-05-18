"""

"""

from setuptools import setup, find_packages

setup(
    name='panda-3d-tactica',
    package_data={'': ['*.md', '*.txt']},
    author='Alistair Broomhead',
    version='0.0.0',
    author_email='alistair.broomhead@gmail.com',
    description='A simple Turn-Based Tactics game built using Panda3D',
    license='BSD 3-clause',
    url='https://github.com/alistair-broomhead/panda-3d-tactics',
    long_description=__doc__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'panda3d==1.10.6',
    ]
)