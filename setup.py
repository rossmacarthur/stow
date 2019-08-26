"""
Setup file for Stow.
"""

import io
import os
import re

from setuptools import find_packages, setup


def get_metadata():
    """
    Return metadata for Stow.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    init_path = os.path.join(here, 'src', 'stow', '__init__.py')
    readme_path = os.path.join(here, 'README.md')

    with io.open(init_path, encoding='utf-8') as f:
        about_text = f.read()

    metadata = {
        key: re.search(r'__' + key + r'__ = ["\'](.*?)["\']', about_text).group(1)
        for key in ('title', 'version', 'url', 'author', 'author_email', 'license', 'description')
    }
    metadata['name'] = metadata.pop('title')

    with io.open(readme_path, encoding='utf-8') as f:
        metadata['long_description'] = f.read()
        metadata['long_description_content_type'] = 'text/markdown'

    return metadata


metadata = get_metadata()

# Primary requirements
install_requires = [
    'Flask >=1.0.0,<2.0.0',
    'Flask-Bcrypt >=0.7.0,<0.8.0',
    'Flask-Classful >=0.14.0,<0.15.0',
    'Flask-HTTPAuth >=3.0.0,<4.0.0',
    'Flask-Login >=0.4.0,<0.5.0',
    'Flask-Migrate >=2.0.0,<3.0.0',
    'Flask-SQLAlchemy >=2.0.0,<3.0.0',
    'Flask-WTF >=0.14.0,<0.15.0',
    'gunicorn >=19.0.0,<20.0.0',
    'itsdangerous >=1.0.0,<2.0.0',
    'WTForms >=2.0.0,<3.0.0'
]

# Development requirements
lint_requires = [
    'flake8',
    'flake8-isort',
    'flake8-quotes',
    'pep8-naming'
]
test_requires = [
    'pytest',
    'pytest-cov',
]

setup(
    # Options
    install_requires=install_requires,
    extras_require={
        'dev.lint': lint_requires,
        'dev.test': test_requires
    },
    python_requires='>=3.4',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # Metadata
    download_url='{url}/archive/{version}.tar.gz'.format(**metadata),
    project_urls={
        'Issue Tracker': '{url}/issues'.format(**metadata)
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    **metadata
)
