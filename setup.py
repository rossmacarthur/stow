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
    'bcrypt==3.1.5',
    'cffi==1.11.5',
    'Click==7.0',
    'Flask==1.0.2',
    'Flask-Bcrypt==0.7.1',
    'Flask-Classful==0.14.1',
    'Flask-HTTPAuth==3.2.4',
    'Flask-Login==0.4.1',
    'Flask-SQLAlchemy==2.3.2',
    'Flask-WTF==0.14.2',
    'gunicorn==19.9.0',
    'itsdangerous==1.1.0',
    'isodate==0.6.0',
    'Jinja2==2.10',
    'MarkupSafe==1.1.0',
    'pycparser==2.19',
    'six==1.12.0',
    'SQLAlchemy==1.2.16',
    'Werkzeug==0.14.1',
    'WTForms==2.2.1'
]

# Development requirements
lint_requires = [
    'flake8',
    'flake8-docstrings',
    'flake8-isort',
    'flake8-per-file-ignores',
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
