import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mcm-api',
    version='0.1',
    packages=['mcm_api'],
    include_package_data=True,
    install_requires=[
        'lxml',
        'configparser',
    ],
    license='BSD License',  # example license
    description='Api for searching cards from MagicCardMarket',
    long_description=README,
    url='http://www.example.com/',
    author='Toni Haka-Risku',
    author_email='tojuhaka@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
