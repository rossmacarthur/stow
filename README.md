# stow

A Flask app to securely PUT and GET data.

- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [Deploying](#deploying)
  - [Prerequisites](#prerequisites-1)
  - [Updating](#updating)
  - [Installing](#installing-1)
- [API](#api)
- [License](#License)
- [Acknowledgments](#acknowledgments)

## Getting started

### Prerequisites

For development you will need [Python 3](https://www.python.org/downloads/) and [Virtualenv](https://pypi.python.org/pypi/virtualenv). You can install Virtualenv with:
```
pip install virtualenv
```

### Installing

Clone the repository:
```
git clone git@github.com:rossmacarthur/stow.git && cd stow
```

Build app and run development server:
```
make build
export ROLE=DEV
export SECRET_KEY=$(./bin/secret_key)
make run
```

The API will then be available at [http://localhost:5001](http://localhost:5001).

## Deploying

### Prerequisites

For production you will need [Nginx](https://www.nginx.com/) or equivalent, [Python 2](https://www.python.org/downloads/), [Python 3](https://www.python.org/downloads/), [Supervisor](https://pypi.python.org/pypi/supervisor), and [Virtualenv](https://pypi.python.org/pypi/virtualenv). You can install Supervisor and Virtualenv with:
```
pip install supervisor virtualenv
```

Note: Supervisor only works under Python 2.

### Updating

To update an install to the latest version:
```
cd /var/www/stow
git pull
venv/bin/pip install -e .
supervisorctl restart stow
```

### Installing

First clone the repository:
```
git clone git@github.com:rossmacarthur/stow.git /var/www/stow && cd /var/www/stow
```

Then build and add to supervisor:
```
make build
rsync -c etc/supervisor/stow.conf /etc/supervisor/conf.d/stow.conf
echo "    SECRET_KEY=\"$(./bin/secret_key)\"" >> /etc/supervisor/conf.d/stow.conf
supervisorctl reread
supervisorctl update
```

You can then `proxy_pass http://localhost:5001;` in your Nginx config.

## API

To store `<value>` under the key `<key>` you must PUT to `/api/stow/<key>` with:
```
{"value": "some interesting secret data"}
```

You can then GET from `/api/stow/<key>` to retrieve:
```
{"value": "some interesting secret data",
 "modified": "2018-03-10T10:25:35.576296",
 "created": "2018-03-10T10:25:35.576296"}
```

Of course to do the above you need to provide authorization. You must first register a user by POST to `/api/user` with:
```
{"name": "John Smith",
 "password": "secret1234"}
```

You can then use HTTP Basic Auth with the name and password. Or if you prefer you can request a token from `/api/token` and use this as the HTTP Basic Auth username (in this case the password can be left blank or set to an arbitrary value). The token will last for an hour.

## License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file.

## Acknowledgments

I found Miguel Grinberg's HTTP Basic Auth [Flask example app](https://github.com/miguelgrinberg/REST-auth) helpful.
