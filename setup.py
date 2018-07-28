from setuptools import setup


install_requires = [
    'Flask==1.0.2',
    'Flask-Bcrypt==0.7.1',
    'Flask-Classful==0.14.1',
    'Flask-HTTPAuth==3.2.4',
    'Flask-Login==0.4.1',
    'Flask-SQLAlchemy==2.3.2',
    'Flask-WTF==0.14.2',
    'gunicorn==19.9.0',
    'itsdangerous==0.24',
    'python-dateutil==2.7.3'
]

extras_require = {
    'linting': [
        'flake8'
    ]
}

setup(
    name='stow',
    packages=['stow'],
    version='1.0.0',
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.3',
    description='A simple flask app to securely PUT and GET data.',
    author='Ross MacArthur',
    author_email='macarthur.ross@gmail.com',
    license='MIT',
    url='https://github.com/rossmacarthur/stow',
)
