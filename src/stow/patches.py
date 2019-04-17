from urllib.parse import urlparse

from flask import request
from flask import url_for as _url_for


def url_with_host(path):
    """
    Prepend the host URL excluding the domain name to a path.
    """
    return '/'.join((urlparse(request.host_url).path.rstrip('/'), path.lstrip('/')))


def url_for(*args, **kwargs):
    """
    Prepend the host URL excluding the domain name to all non external URLs.
    """
    if kwargs.get('_external') is True:
        return _url_for(*args, **kwargs)
    else:
        return url_with_host(_url_for(*args, **kwargs))


def contains(value, substring):
    """
    Because in Jinja templates you can't use the 'in' operator.
    """
    return substring in value


def register_patches(app):
    # Update global url_for
    app.jinja_env.globals['url_for'] = url_for

    # Register Jinja filters
    app.jinja_env.filters['contains'] = contains
