from setuptools import setup


install_requires = [
    'Flask==0.12.2',
    'Flask-Bcrypt==0.7.1',
    'Flask-Classful==0.14.1',
    'Flask-HTTPAuth==3.2.3',
    'Flask-SQLAlchemy==2.3.2',
    'gunicorn==19.7.1',
    'itsdangerous==0.24',
    'python-dateutil==2.6.1'
]

setup(
    name='stow',
    packages=['stow'],
    version='1.0.0',
    install_requires=install_requires,
    python_requires='>=3.3',
    description='A simple flask app to securely PUT and GET data.',
    author='Ross MacArthur',
    author_email='macarthur.ross@gmail.com',
    license='MIT',
    url='https://github.com/rossmacarthur/stow',
)
