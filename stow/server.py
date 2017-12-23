from . import app
from .views import error_handler_view, UserView, TokenView, StowView


def register(url, view):
    view_name = '{} => {}.{}'.format(url, view.__module__, view.__name__)
    view_function = view.as_view(view_name)
    app.add_url_rule(url, view_func=view_function)


app.register_error_handler(Exception, error_handler_view)

register('/user', UserView)
register('/token', TokenView)
register('/stow', StowView)
