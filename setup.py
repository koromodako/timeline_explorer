from pathlib import Path
from setuptools import setup, find_packages
from timeline_explorer import __version__

HERE = Path(__file__).absolute().parent

def requirements():
    with HERE.joinpath('requirements.txt').open() as reqs:
        return list([req.strip() for req in reqs if req.strip()])

setup(
    # main information
    name='timeline_explorer',
    version=__version__,
    description='',
    author='koromodako',
    author_email='koromodako@gmail.com',
    url='https://github.com/koromodako/mkctf',
    # package files
    packages=find_packages(str(HERE)),
    install_requires=requirements(),
    # configuration files
    entry_points={
        'console_scripts': [
            'timeline-explorer = timeline_explorer.main:app',
        ]
    }
)
