from flask import url_for as _url_for


def url_for(*args, **kwargs):
    """
    Set external True on all URL's.
    """
    kwargs['_external'] = True
    return _url_for(*args, **kwargs)


def contains(value, substring):
    """
    Because in Jinja templates you can't use the 'in' operator.
    """
    return substring in value


def register_patches(app):
    # Update global url_for
    app.jinja_env.globals['url_for'] = url_for

    # Register Jinja filters
    for func in [contains]:
        app.jinja_env.filters[func.__name__] = func
