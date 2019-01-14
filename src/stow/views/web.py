from urllib.parse import urljoin, urlparse

from flask import Blueprint, abort, flash, redirect, render_template, request
from flask_classful import FlaskView, route
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from stow.config import Config
from stow.forms import ChangeCredentialsForm, LoginForm, RegisterForm, StowForm
from stow.models import Stow, User
from stow.patches import url_for, url_with_host


bp = Blueprint('web', __name__)
login_manager = LoginManager()


def render(*args, **kwargs):
    kwargs['meta'] = Config.META
    return render_template(*args, **kwargs)


def is_safe_url(target):
    """
    Check that the target url is safe.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_next(target, *args, **kwargs):
    """
    Redirect to the the next argument else the target.
    """
    next = request.args.get('next')
    if not is_safe_url(next):
        return abort(400)
    return redirect(next or target)


def flash_form_errors(form):
    """
    Display all form errors nicely.
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash('{}: {}'.format(getattr(form, field).label.text, error), 'danger')


@bp.errorhandler(Exception)
def error_handler(error):
    """
    Handle errors in views.
    """
    return render('error.html'), 500


@login_manager.unauthorized_handler
def unauthorized_handler():
    """
    If a user is not logged in, redirect to the login page.
    """
    return redirect(url_for('web.LoginView:index', next=url_with_host(request.path)))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class UnprotectedTemplateView(FlaskView):
    trailing_slash = False
    excluded_methods = ['render']

    def render(self, *args, **kwargs):
        template_name = kwargs.pop('template_name', self.template_name)
        kwargs['meta'] = Config.META
        return render(template_name, *args, **kwargs)


class TemplateView(UnprotectedTemplateView):
    decorators = [login_required]


class RegisterView(UnprotectedTemplateView):
    template_name = 'credentials.html'

    def before_request(self, *args, **kwargs):
        if User.query.count() >= Config.MAX_USERS:
            flash('Unfortunately the maximum number of users have been registered.', 'danger')
            form = RegisterForm(request.form)
            return self.render(form=form)

    def index(self):
        form = RegisterForm(request.form)
        return self.render(form=form)

    def post(self):
        form = RegisterForm(request.form)

        if not form.validate():
            flash_form_errors(form)
            return self.render(form=form)

        user = User.query.filter(User.name.ilike(form.name.data)).first()

        if user:
            flash('The name \'{}\' is not available.'.format(form.name.data), 'danger')
            return self.render(form=form)

        user = User(name=form.name.data, password=form.password.data)
        user.save()
        flash('Welcome {}! You are now registered!'.format(user.name), 'success')
        login_user(user)
        return redirect_next(url_for('web.IndexView:index'))


class LoginView(UnprotectedTemplateView):
    template_name = 'credentials.html'

    def index(self):
        if current_user:
            redirect(url_for('web.IndexView:index'))
        form = LoginForm(request.form)
        return self.render(form=form)

    def post(self):
        form = LoginForm(request.form)

        if not form.validate():
            flash_form_errors(form)
            return self.render(form=form)

        user = User.query.filter(User.name.ilike(form.name.data)).first()

        if not user or not user.verify_password(form.password.data):
            flash('Incorrect login credentials.', 'danger')
            return self.render(form=form)

        login_user(user)
        return redirect_next(url_for('web.IndexView:index'))


class LogoutView(TemplateView):

    def index(self):
        logout_user()
        return redirect(url_for('web.LoginView:index'))


class AccountView(TemplateView):
    template_name = 'account.html'

    def render(self, *args, **kwargs):
        kwargs['stow_count'] = Stow.query.filter_by(user_id=current_user.id).count()
        return super().render(*args, **kwargs)

    def index(self):
        form = ChangeCredentialsForm(request.form)
        return self.render(form=form)

    def post(self):
        form = ChangeCredentialsForm(request.form)

        if not form.validate():
            flash_form_errors(form)
            return self.render(form=form)

        if current_user.name.lower() != form.name.data.lower():
            user = User.query.filter(User.name.ilike(form.name.data)).first()
            if user:
                flash('The name \'{}\' is not available.'.format(form.name.data), 'danger')
                return self.render(form=form)

        if not current_user.verify_password(form.old_password.data):
            flash('Incorrect password.', 'danger')
            return self.render(form=form)

        current_user.name = form.name.data
        current_user.hash_password(form.new_password.data)
        current_user.save()
        flash('Updated account credentials.', 'success')
        return redirect(url_for('web.AccountView:index'))


class IndexView(TemplateView):
    template_name = 'index.html'
    route_base = '/'

    def index(self):
        stows = Stow.query.filter_by(user_id=current_user.id).order_by('key').all()
        return self.render(stows=stows)


class StowView(TemplateView):
    template_name = 'stow.html'

    def index(self):
        form = StowForm()
        return self.render(form=form)

    def get(self, key):
        stow = Stow.query.filter_by(user_id=current_user.id, key=key).first()
        form = StowForm(obj=stow)
        return self.render(form=form)

    @route('/', methods=['POST'], strict_slashes=False)
    @route('/<key>', methods=['POST'], strict_slashes=False)
    def post(self, key=None):
        form = StowForm(request.form)

        stow = None
        if key:
            stow = Stow.query.filter_by(user_id=current_user.id, key=key).first()
            if form.delete.data is True:
                stow.destroy()
                flash('Deleted stow \'{}\'.'.format(stow.key), 'info')
                return redirect(url_for('web.IndexView:index'))

        if not form.validate():
            flash_form_errors(form)
            return self.render(form=form)

        if not stow:
            stow = Stow()
            stow.user_id = current_user.id
        stow.key = form.key.data
        stow.value = form.value.data

        try:
            stow.save()
        except IntegrityError:
            flash('Key: This field must be unique.', 'danger')
            return self.render(form=form)

        if key:
            flash('Updated stow \'{}\'.'.format(stow.key), 'info')
        else:
            flash('Created stow \'{}\'.'.format(stow.key), 'info')

        return redirect(url_for('web.IndexView:index'))


for cls in [RegisterView, LoginView, LogoutView, AccountView, IndexView, StowView]:
    cls.register(bp, strict_slashes=False)
