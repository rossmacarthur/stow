from setuptools import setup


install_requires = [
    'click==6.7',
    'Flask==0.12.2',
    'Flask-SQLAlchemy==2.3.2',
    'gunicorn==19.7.1',
    'PyJWT==1.5.3'
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
