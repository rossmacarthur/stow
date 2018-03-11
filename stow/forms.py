from wtforms import Form, validators
from wtforms.fields import DateTimeField, PasswordField, SubmitField, TextAreaField, TextField


class LoginForm(Form):
    name = TextField('Name', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    login = SubmitField()


class RegisterForm(Form):
    name = TextField('Name', [validators.DataRequired(), validators.Length(min=3), validators.Length(max=99)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=8)])
    register = SubmitField()


class ChangeCredentialsForm(Form):
    name = TextField('Name', [validators.DataRequired()])
    old_password = PasswordField('Old Password', [validators.DataRequired()])
    new_password = PasswordField('New Password', [validators.DataRequired(), validators.Length(min=8)])
    change_credentials = SubmitField()
    delete_account = SubmitField()


class StowForm(Form):
    key = TextField('Key', [validators.DataRequired()])
    value = TextAreaField('Value')
    created = DateTimeField('Created', render_kw={'readonly': True})
    modified = DateTimeField('Modified', render_kw={'readonly': True})
    submit = SubmitField()
    delete = SubmitField()
