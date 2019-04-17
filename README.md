# stow

A Flask app to securely PUT and GET data.

This app was developed as a learning endeavor, in order to learn about Flask and
various other packages in the Flask ecosystem.

In this example the following packages are used:

- [Flask][flask].
- [Flask-Bcrypt][flask-bcrypt] provides bcrypt hashing utilities.
- [Flask-Classful][flask-classful] adds class based views.
- [Flask-HTTPAuth][flask-httpauth] provides Basic, Digest and Token HTTP authentication.
- [Flask-Login][flask-login] provides user session management.
- [Flask-Migrate][flask-migrate] provides migration support using [Alembic][alembic].
- [Flask-SQLAlchemy][flask-sqlalchemy] adds support for [SQLAlchemy][sqlalchemy].
- [Flask-WTF][flask-wtf] provides integration with [WTForms][wtforms].

## Getting started

Clone the repository
```
git clone git@github.com:rossmacarthur/stow.git && cd stow
```

Create a virtualenv using [pyenv][pyenv] or similar, you will need to use Python
3.6 or later
```
pyenv virtualenv stow
pyenv local stow
```

Then inside the virtual environment install the app
```
make install-dev
```

To run the development server you will need to export the following
```
export FLASK_APP="stow.server"
export FLASK_ENV="development"
export FLASK_SECRET_KEY="$(./bin/secret_key)"
```

Create the database and run all migrations
```
make migrate
```

Finally run the development server
```
make run
```

Stow will then be available at http://localhost:5001! :tada:

## API

To store `<value>` under the key `<key>` you must PUT to `/api/stow/<key>` with:
```json
{
    "value": "some interesting secret data"
}
```

You can then GET from `/api/stow/<key>` to retrieve:
```json
{
    "value": "some interesting secret data",
    "modified": "2018-03-10T10:25:35.576296",
    "created": "2018-03-10T10:25:35.576296"
}
```

Of course to do the above you need to provide authorization. You must first
register a user by POST to `/api/user` with:
```json
{
    "name": "John Smith",
    "password": "secret1234"
}
```

You can then use HTTP Basic Auth with the name and password. Or if you prefer
you can request a token from `/api/token` and use this as the HTTP Basic Auth
username (in this case the password can be left blank or set to an arbitrary
value). The token will last for an hour.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file.


[alembic]: https://alembic.sqlalchemy.org
[flask]: https://palletsprojects.com/p/flask/
[flask-bcrypt]: https://flask-bcrypt.readthedocs.io
[flask-classful]: http://flask-classful.teracy.org/
[flask-httpauth]:https://flask-httpauth.readthedocs.io
[flask-login]: https://flask-login.readthedocs.io
[flask-migrate]: https://flask-migrate.readthedocs.io
[flask-sqlalchemy]: http://flask-sqlalchemy.pocoo.org
[flask-wtf]: https://flask-wtf.readthedocs.io
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[sqlalchemy]: https://www.sqlalchemy.org/
[wtforms]: https://wtforms.readthedocs.io
